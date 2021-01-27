from emotes.wsgi import app, cache
from emotes.app.emote import EmoteWrapper
from flask import jsonify, request, send_file, send_from_directory
import os
import re

def normalize_size(size, tg=False):
	size = request.args.get('size')
	if size == None and not tg:
		size = 48
	if size == None and tg:
		size = 256
	size = re.split('x|,|-', str(size))
	if len(size) == 1:
		size.append(size[0])
	for index, i in enumerate(size):
		size[index] = int(i)
	return size

@app.route('/<path:namespace>/<emote>')
@app.route("/<emote>", subdomain="<namespace>")
def namespaced_emote(namespace, emote):
	tg = True if request.args.get('tg') == '1' else False

	if emote.endswith(".gif"):
		emote = emote.split(".gif")[0]
	size = request.args.get('size')
	size = normalize_size(size, tg=tg)

	emote_wrapper = EmoteWrapper(namespace, emote, size[0], size[1], tg=tg)
	emote_bytesio = emote_wrapper.fetch()

	if emote_bytesio == 'processing':
		return jsonify({"msg": "Image processing"}), 202

	if emote_bytesio:
		print(emote_bytesio[1])
		return send_file(emote_bytesio[0], mimetype=f"image/{emote_bytesio[1]}")

	return jsonify({"msg": "Emote not found"}), 404

@app.route('/<emote>') 
def priority_emote(emote):
	tg = True if request.args.get('tg') == '1' else False

	if emote.endswith(".gif"):
		emote = emote.split(".gif")[0]
	size = request.args.get('size')
	size = normalize_size(size, tg=tg)

	emote_wrapper = EmoteWrapper(None, emote, size[0], size[1], tg=tg)
	emote_bytesio = emote_wrapper.fetch()
	if emote_bytesio == 'processing':
		return jsonify({"msg": "Image processing"}), 202

	if emote_bytesio:
		print(emote_bytesio[1])
		return send_file(emote_bytesio[0], mimetype=f"image/{emote_bytesio[1]}")

	return jsonify({"msg": "Emote not found"}), 404
