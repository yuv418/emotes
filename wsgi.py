from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from peewee import *
from playhouse.flask_utils import FlaskDB
from celery import Celery
import os


app = Flask(__name__)
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
	TWITCH_CLIENT_ID = os.environ["EMOTES_TWITCH_CLIENT_ID"],
	API_PREFIX = "/api",
	CACHE_TYPE = "simple",
        CELERY_BROKER_URL='redis://localhost:6379/0',
        CELERY_RESULT_BACKEND='redis://localhost:6379/0', # TODO figure out what the /0 means.
        ALLOWED_EXT = ['gif', 'png', 'jpeg', 'jpg', 'webp']
))

CORS(app)
db = FlaskDB(app)
cache = Cache(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

api_prefix = app.config["API_PREFIX"]

from emotes.app.routes import *
from emotes.app.models import *
from emotes.install import *

install()

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000)
