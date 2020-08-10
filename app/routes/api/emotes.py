from emotes.wsgi import app, api_prefix
from flask import request, jsonify
from emotes.app.models import *
from emotes.app.routes.security import *
from slugify import slugify
import secrets
import string
import os
import json

allowed_ext = ['gif', 'png', 'jpeg', 'jpg']
alphanumeric = string.ascii_letters + string.digits

# GET emotes from namespace API

@app.route(f"{api_prefix}/emotes", methods=["POST"]) # C
@apikey_required
def api_create_emote(user):
    path = request.values.get("path")
    name = request.values.get("name")
    namespace = Namespace.from_path(path)
    if not namespace:
        return jsonify({"msg": "Your namespace path is invalid"}), 400

    file = request.files.get("emotes_file")
    if not file:
        return jsonify({"msg": "Your file is invalid"}), 400

    if slugify(name).lower() in [emote.slug for emote in namespace.emotes]:
        return jsonify({"msg": "The emote already exists."}), 400

    info = dict(request.values)

    del info['path']
    del info['name']
    del info['api_key']

    file_ext = file.filename.rsplit(".", 1)[1]
    if file_ext in allowed_ext:
        filename = ''.join([secrets.choice(alphanumeric) for i in range(64)]) + f".{file_ext}"
        file.save(os.path.join(app.config["UPLOADS_PATH"], filename))

        new_emote = Emote(path=filename, name=name, info=info, namespace=namespace, slug=slugify(name).lower())
        new_emote.save()
        return jsonify({"msg": "Uploaded", "path": f"{namespace.path()}{new_emote.slug}"})

    return jsonify({"msg": "Invalid file."}), 400

@app.route(f"{api_prefix}/emotes", methods=["DELETE"]) # D
@apikey_required
def api_delete_emote(user):
    path = request.values.get("path")
    emote_name = request.values.get("name")
    scope = request.values.get("scope")


    
    namespace = Namespace.from_path(path)
    if not namespace:
        return jsonify({"msg": "Your namespace path is invalid"}), 400
    
    emote = namespace.emotes.select().where(Emote.slug == emote_name).first()
    if not emote:
        return jsonify({"msg": "Your emote is invalid"}), 400

    emote.delete_instance()
    return jsonify({"msg": "Emote deleted."})

@app.route(f"{api_prefix}/emotes")
@apikey_required
def api_global_emotes(user):
    """Get a list of local/priority/global emotes."""
    name = request.values.get("name")
    slug = request.values.get("slug")

    local_name =  Emote.local_emote(name=name)
    if local_name:
        return local_name

    local_slug = Emote.local_emote(slug=slug)
    if local_slug:
        return local_slug

    if name and slug and not local_slug and not local_name:
        return jsonify({"msg": "Emote not found"}), 404


    return jsonify(Emote.local_emotes())
