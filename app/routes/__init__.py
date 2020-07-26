from emotes.wsgi import app
from flask import send_from_directory

#@app.route('/favicon.ico')
#def favicon():
#	print(send_from_directory('/assets', 'thonk.png'))
#	return send_from_directory('/assets', 'thonk.png')

from emotes.app.routes.api import *
from emotes.app.routes.show import *
