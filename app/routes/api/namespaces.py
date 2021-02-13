from emotes.wsgi import app, api_prefix
from flask import request, jsonify
from emotes.app.models import *
from emotes.app.routes.security import *
from slugify import slugify
import secrets
import string
from playhouse.shortcuts import model_to_dict
import os

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

    if not path:
        return jsonify({"msg": "New namespace path not provided."}), 400
    else:
        if Namespace.from_path(path):
            return jsonify({"msg": "That namespace already exists."}), 400

    if not name: 
        return jsonify({"msg": "New namespace name not provided."}), 400

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


@app.route(f"{api_prefix}/namespaces/<path:namespace>")
@apikey_required
def api_namespace(namespace, user):
    nmsp = Namespace.from_path(namespace)
    if not nmsp:
        return jsonify({"msg": "Namespace not found."}), 404

    nmsp_dict = model_to_dict(nmsp, backrefs=True, exclude=[User.admin, User.api_keys, ResizedImage.path, Image.original])
    return jsonify(nmsp_dict)

@app.route(f"{api_prefix}/namespaces/<path:namespace>", methods=["DELETE"])
@apikey_required
def api_delete_namespace(namespace, user):
    nmsp = Namespace.from_path(namespace)
    if not nmsp:
        return jsonify({"msg": "Namespace not found."}), 404

    if user != nmsp.user:
        if not user.admin:
            return jsonify({"msg": "You do not have sufficient permissions to do this."}), 403

    nmsp.delete_instance(recursive=True)
    return jsonify({"msg": "Namespace deleted successfully."})
