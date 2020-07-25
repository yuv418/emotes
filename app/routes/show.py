from emotes.wsgi import app
from emotes.app.emote import EmoteWrapper
from flask import jsonify, request, send_file

# can namespace be a path somehow
# like /twitch/scarra/emote and namespace is "/twitch/scarra"

@app.route('/<path:namespace>/<emote>') 
def namespaced_emote(namespace, emote):	
	return jsonify((namespace, emote))

@app.route('/<emote>') 
def priority_emote(emote):
	#TODO: Implement optional query: [size=[INT|INTxINT|Original]]
	emote_wrapper = EmoteWrapper(None, emote, 32, 32)
	return send_file(emote_wrapper.fetch(), mimetype="image/png")
	#?size=64x
	#?size=64x48
	#?size=original
