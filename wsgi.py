from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from peewee import *
from playhouse.flask_utils import FlaskDB
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
        MIGRATIONS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "migrator", "migrations"),
	TWITCH_CLIENT_ID = os.environ["EMOTES_TWITCH_CLIENT_ID"],
	API_PREFIX = "/api",
	CACHE_TYPE = "simple",
))

CORS(app)
db = FlaskDB(app)
cache = Cache(app)

api_prefix = app.config["API_PREFIX"]

from emotes.app.routes import *
from emotes.app.models import *
from emotes.migrator import *

migrate()

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000)
