from wsgi import app
from flask import jsonify, request

# can namespace be a path somehow
# like /twitch/scarra/emote and namespace is "/twitch/scarra"

@app.route('/<path:namespace>/<emote>') 
def namespacedEmote(namespace, emote):	
	return jsonify((namespace, emote))

@app.route('/<emote>') 
def priorityEmote(emote):
	return jsonify(emote)
	#?size=64x
	#?size=64x48
	#?size=original
	#Resize image or specified with params blyat by 32/largestSide
	# yeah
