from flask import Flask
from pony.flask import Pony
from pony.orm import Database
import os

app = Flask(__name__)
app.config.update(dict(
	SECRET_KEY = os.environ["EMOTES_SECRET_KEY"],
	PONY =  {
		'provider':  'mysql',
		'host': os.environ["EMOTES_DB_HOST"],
		'user': os.environ["EMOTES_DB_USER"],
		'password': os.environ["EMOTES_DB_PASSWORD"],
		'database': os.environ["EMOTES_DB_DATABASE"],
	},
	DISCORD_ID = os.environ["EMOTES_DISCORD_ID"],
	DISCORD_SECRET = os.environ["EMOTES_DISCORD_SECRET"],
	DISCORD_ENDPOINT = "https://discord.com/api/v6",
	REDIRECT_URI = "https://emotes.ml"
))

db = Database()
db.bind(**app.config['PONY'])

from emotes.app.models import *

# db.generate_mapping(create_tables=True)

Pony(app)

from emotes.app.routes import *

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)