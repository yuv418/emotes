from emotes.wsgi import app
from emotes.app.emote import EmoteWrapper
from flask import jsonify, request, send_file, send_from_directory
import os

# can namespace be a path somehow
# like /twitch/scarra/emote and namespace is "/twitch/scarra"
#where
# where is assets make it

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'assets'), 'favicon.ico')

@app.route('/<path:namespace>/<emote>') 
def namespaced_emote(namespace, emote):	
	return jsonify((namespace, emote))

@app.route('/<emote>') 
def priority_emote(emote):
	size = request.args.get('size')
	if size == None:
		size = 32
	#TODO: Implement optional query: [size=[INT|INTxINT|Original]]
	emote_wrapper = EmoteWrapper(None, emote, 32, 32)
	return send_file(emote_wrapper.fetch(), mimetype="image/png")
	#?size=64x
	#?size=64x48
	#?size=original
