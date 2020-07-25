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
		'user': os.environ["EMOTES_DB_PASSWORD"],
		'password': os.environ["EMOTES_DB_PASSWORD"],
		'database': os.environ["EMOTES_DB_DATABASE"],
	}
))
db = Database()

Pony(app)

from app.routes import *

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8000, debug=True)