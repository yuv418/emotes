from emotes.wsgi import app 
from flask import request, jsonify
from emotes.app.models import *
from pony.orm import *

api_prefix = "/api"

@app.route(f"{api_prefix}/upload", methods=["POST"])
def api_upload():
    return jsonify(request.values)

@app.route(f"{api_prefix}/user", methods=["POST"])
@db_session
def api_new_user():
    new_user = User(name=request.values.get("name"))
    return jsonify({"id": new_user.id})

@app.route(f"{api_prefix}/user/<id>/apikey")
def api_user_apikey(id):
    api_key = ApiKey(user=User[id])
    

@app.route(f"{api_prefix}/namespace", methods=["POST"])
@db_session
@api_key
def api_new_namespace():
    pass
