from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from peewee import *
from playhouse.flask_utils import FlaskDB
from celery import Celery
from celery.bin import worker
from dotenv import load_dotenv
import os

load_dotenv(verbose=True, dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".flaskenv"))

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/templates"),
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "app/static")
)

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
    DOMAIN = os.environ.get("EMOTES_DOMAIN")
))

def make_celery(app): # Thanks https://flask.palletsprojects.com/en/0.12.x/patterns/celery/
    celery = Celery(app.import_name, backend=app.config["CELERY_RESULT_BACKEND"],
                  broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
          abstract = True
          def __call__(self, *args, **kwargs):
              with app.app_context():
                  return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


CORS(app)
db = FlaskDB(app)
cache = Cache(app)
celery = make_celery(app)
celery.conf.update(app.config)

api_prefix = app.config["API_PREFIX"]

from emotes.app.routes import *
from emotes.app.models import *
from emotes.migrator import *

migrate()

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000)
