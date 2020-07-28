from emotes.wsgi import app 
from flask import request, jsonify
from emotes.app.models import *
from emotes.app.routes.security import *
from slugify import slugify
import secrets
import string
import os

alphanumeric = string.ascii_letters + string.digits

api_prefix = "/api"
allowed_ext = ['gif', 'png', 'jpeg', 'jpg']

@app.route(f"{api_prefix}/emotes", methods=["POST"])
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

@app.route(f"{api_prefix}/emotes", methods=["POST"])
@apikey_required
def api_delete_emote(user):
    path = request.values.get("path")
    name = request.values.get("name")
    emote_name = request.values.get("emote")
    
    namespace = Namespace.from_path(path)
    if not namespace:
        return jsonify({"msg": "Your namespace path is invalid"}), 400
    
    emote = namespace.emotes.select().where(Emote.slug == emote_name)
    if not emote:
        return jsonify({"msg": "Your emote is invalid"}), 400

    emote.delete_instance()
    return jsonify({"msg": "Emote deleted."})

@app.route(f"{api_prefix}/user", methods=["POST"])
@apikey_required
@admin_required
def api_new_user(user):
    new_user = User(name=request.values.get("name"))
    new_user.save()
    return jsonify({"id": new_user.id})

@app.route(f"{api_prefix}/user/<id>/api_key", methods=["POST"])
@apikey_required
@admin_required
def api_user_apikey(id, user):
    api_key = ApiKey(user=User[id])
    api_key.save()
    return jsonify({"key": api_key.value, "user_id": id})
    

@app.route(f"{api_prefix}/namespaces", methods=["POST"])
@apikey_required
def api_new_namespace(user):
    """
    Create a namespace. It takes two params:
    path: path
    name: string

    Eg. path could be /test or /test/subtest
    If /test does not exist but you create /subtest then it creates just /test and returns that id.
    If /test does exist it creates /test/subtest and returns /test/subtest's id.
    """

    path = request.values.get("path")
    name = request.values.get("name")

    root_path = path.split("/")[0]
    nmsp = Namespace.select().where(Namespace.slug == root_path).first()
    if nmsp:
        if user != nmsp.user:
            return jsonify({"msg": "You do not own the parent namespace, and as such cannot modify it."}), 403
        for i, nmsp_str in enumerate(path.split("/")[1:]): # Make the new namespace in the parent
            nmsp_children = nmsp.children
            print(f"children len: {len(nmsp_children)}")

            if len(nmsp_children) == 0:
                # No children. Create first child.
                new_namespace = Namespace(name=name, slug=nmsp_str, users=user, parent=nmsp)
                new_namespace.save()
                return jsonify({"id": new_namespace.id})
            elif nmsp_children: 
                child = nmsp_children.select().where(Namespace.slug == path.split("/")[i+1]).first()
                print(child, nmsp_str)
                if not child:
                    # Child exists, create
                    new_namespace = Namespace(name=name, slug=nmsp_str, user=user, parent=nmsp)
                    new_namespace.save()
                    return jsonify({"id": new_namespace.id})

            # Advance one child down the namespace "tree"
            nmsp = nmsp.children.select().where(Namespace.slug == nmsp_str).first()
            print(f"nmsp now {nmsp} str {nmsp_str}")
    else:
        # Create root-level namespace
        new_namespace = Namespace(name=name, slug=root_path, user=user)
        new_namespace.save()
        return jsonify({"id": new_namespace.id})

    return jsonify({"path": path, "name": name})
