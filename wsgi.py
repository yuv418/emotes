from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from peewee import *
from playhouse.flask_utils import FlaskDB
from celery import Celery
from celery.bin import worker
from dotenv import load_dotenv
from Cheetah.Template import Template
from Cheetah.CheetahWrapper import CheetahWrapper
import urllib
import logging
import os
import sys

load_dotenv(verbose=True, dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".flaskenv"))

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/templates"),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/static"),
    subdomain_matching=True
)
app.url_map.strict_slashes = False # People using subdomains may find this easier if they inadvertently put a trailing slash (slash regular users as well)


# TODO slack
app.config.update(dict(
	SECRET_KEY = os.environ["EMOTES_SECRET_KEY"],
	DATABASE = 'mysql://{}:{}@{}:3306/{}'.format(
		os.environ["EMOTES_DB_USER"],
        os.environ["EMOTES_DB_PASSWORD"],
        os.environ["EMOTES_DB_HOST"],
        os.environ["EMOTES_DB_DATABASE"],
	),
	UPLOADS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads/"),
	EMOTES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emotes/"),
        MIGRATIONS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrator", "migrations"),
	TWITCH_CLIENT_ID = os.environ["EMOTES_TWITCH_CLIENT_ID"],
	API_PREFIX = "/api",
	CACHE_TYPE = "simple",
    CELERY_BROKER_URL=os.environ["EMOTES_CELERY_BROKER_URL"],
    CELERY_RESULT_BACKEND=os.environ["EMOTES_CELERY_RESULT_BACKEND"],
    ALLOWED_EXT = ['gif', 'png', 'jpeg', 'jpg', 'webp'],
    DOMAIN = os.environ.get("EMOTES_DOMAIN"),
    SERVER_NAME=urllib.parse.urlparse(os.environ.get("EMOTES_DOMAIN")).hostname if not app.config["DEBUG"] else None
))

def make_celery(app): # Thanks https://flask.palletsprojects.com/en/0.12.x/patterns/celery/
    celery = Celery(app.import_name, backend=app.config["CELERY_RESULT_BACKEND"],
                    broker=app.config["CELERY_BROKER_URL"], loglevel=logging.DEBUG)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
          abstract = True
          def __call__(self, *args, **kwargs):
              with app.app_context():
                  return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def compile_templates():
    """Compile all the Cheetah templates"""
    import copy
    old_argv = copy.deepcopy(sys.argv) # Cheetah messes with sys.argv, so we can restore it at the end
    extra_files = []
    for dirs, subdirs, files in os.walk(app.template_folder):
        # Thanks https://stackoverflow.com/questions/1120707/using-python-to-execute-a-command-on-every-file-in-a-folder
        wrapper = CheetahWrapper()
        if "__pycache__" not in dirs:
            for f in files:
                if f.endswith('.tmpl'):
                    full_path = os.path.join(dirs, f)
                    extra_files.append(full_path)
                    wrapper.main(argv=["cheetah", "compile", "--nobackup", full_path])
    if app.debug: # Only hot reload with debug mode, but this doesn't work at the moment. TODO Fix
        extra_file_env_str = ":".join(extra_files) # If you use flask run, you need to set an environment variable, so we use this
        os.environ["FLASK_RUN_EXTRA_FILES"] = extra_file_env_str # TODO windows uses semicolons

    sys.argv = old_argv
    return extra_files


CORS(app)
db = FlaskDB(app)
cache = Cache(app)
celery = make_celery(app)
celery.conf.update(app.config)

api_prefix = app.config["API_PREFIX"]
extra_files = compile_templates()

from emotes.app.routes import *
from emotes.app.models import *
from emotes.migrator import *

migrate()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, extra_files=extra_files)
