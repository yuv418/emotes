from flask import Flask
from peewee import *
import peeweedbevolve
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
	UPLOADS_PATH = "uploads/",
))

db = FlaskDB(app)

from emotes.app.routes import *
from emotes.app.models import *

db.database.create_tables([
	User,
	Namespace,
	ApiKey,
	Emote
])

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)