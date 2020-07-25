from wsgi import app 
from flask import request, jsonify

api_prefix = "/api"

@app.route(f"{api_prefix}/upload", methods=["POST"])
def api_upload():
    return jsonify(request.values)
