from emotes.wsgi import app, cache
from emotes.app.emote import EmoteWrapper
from flask import jsonify, request, send_file, send_from_directory
import os
import re

def normalize_size(size):
	size = request.args.get('size')
	if size == None:
		size = 48
	size = re.split('x|,|-', str(size))
	if len(size) == 1:
		size.append(size[0])
	for index, i in enumerate(size):
		size[index] = int(i)
	return size

@app.route('/<path:namespace>/<emote>') 
def namespaced_emote(namespace, emote):
	if emote.endswith(".gif"):
		emote = emote.split(".gif")[0]
	size = request.args.get('size')
	size = normalize_size(size)

	emote_wrapper = EmoteWrapper(namespace, emote, size[0], size[1])
	emote_bytesio = emote_wrapper.fetch()

	if emote_bytesio == 'processing':
		return jsonify({"msg": "Image processing"}), 202

	if emote_bytesio:
		return send_file(emote_bytesio[0], mimetype=f"image/{emote_bytesio[1]}")

	return jsonify({"msg": "Emote not found"}), 404

@app.route('/<emote>') 
def priority_emote(emote):
	if emote.endswith(".gif"):
		emote = emote.split(".gif")[0]
	size = request.args.get('size')
	size = normalize_size(size)

	emote_wrapper = EmoteWrapper(None, emote, size[0], size[1])
	emote_bytesio = emote_wrapper.fetch()
	if emote_bytesio == 'processing':
		return jsonify({"msg": "Image processing"}), 202

	if emote_bytesio:
		return send_file(emote_bytesio[0], mimetype=f"image/{emote_bytesio[1]}")

	return jsonify({"msg": "Emote not found"}), 404
