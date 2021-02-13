from emotes.wsgi import app, api_prefix
from flask import request, jsonify
from emotes.app.models import *
from emotes.app.routes.security import *
from slugify import slugify
import secrets
import string
import os
from playhouse.shortcuts import model_to_dict


@app.route(f"{api_prefix}/users", methods=["POST"])
@apikey_required
@admin_required
def api_new_user(user):
    new_user = User(name=request.values.get("name"))
    new_user.save()
    return jsonify({"id": new_user.id})


@app.route(f"{api_prefix}/users", methods=["DELETE"])
@apikey_required
def api_delete_user(user):
    """
    Delete a user.
    Provide an api key for which your user will be deleted.
    If you are an admin, provide a user id.

    WARNING: This deletes all namespaces and emotes associated with the user.
    """
    if user.admin:
        if request.values.get("id"):
            try:
                delete_user = User[request.values.get("id")]
            except Exception:
                return jsonify({"msg": "Invalid user to delete."}), 400
        if request.values.get("delete") == user.name:
            delete_user = user
        else:
            return jsonify({"msg": "Administrators have an extra level of security to delete."}), 400

    else:
        delete_user = user
    
    delete_user.delete_instance(recursive=True)
    return jsonify({"msg": "User deleted."}) 
    

@app.route(f"{api_prefix}/users", methods=["GET"])
@apikey_required
def api_get_user(user):
    name = request.values.get("name")
    id = request.values.get("id") # Prefers id

    d_user = None
    allowed = [User.admin, User.id, User.name, User.namespaces, Namespace.id, Namespace.name, Namespace.slug]

    if user.admin:
        if not id and not name:
            return jsonify({"msg": "Insufficient information to find user."}), 400
        elif id or name:
            try:
                d_user = User[id]
            except Exception:
                try:
                    d_user = User.select().where(User.name == name).first()
                except Exception:
                    return jsonify({"msg": "Couldn't find user"})
                return jsonify({"msg": "Couldn't find user"})

        elif request.values.get("get") == user.name:
            d_user = user
    else:
        d_user = user

    return jsonify(model_to_dict(d_user, backrefs=True, only=allowed))

# APIKEY
@app.route(f"{api_prefix}/users/<int:id>/api_key", methods=["POST"])
@apikey_required
@admin_required
def api_user_apikey_by_id(id, user):
    return gen_apikey(User[id])

@app.route(f"{api_prefix}/users/<name>/api_key", methods=["POST"])
@apikey_required
@admin_required
def api_user_apikey_by_username(name, user):
    try:
        user = User.get(User.name == name)
    except Exception: # UserDoesNotExist?
        return jsonify({"msg": "The user you are trying to create an API key for does not exist."})

    return gen_apikey(user)

# TODO allow users to generate their own API keys
def gen_apikey(user):
    """
    User: User object
    returns ApiKey.
    """

    api_key = ApiKey(user=user)
    api_key_value = api_key.gen_unhashed_api_key() # Unhashed value
    api_key.save()

    return jsonify({"key": api_key_value, "user_id": user.id})
