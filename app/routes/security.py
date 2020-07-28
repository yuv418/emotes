from functools import wraps
from flask import request, jsonify
from emotes.app.models import *

def apikey_required(f):
    @wraps(f)
    def decorated_f(*args, **kwargs):
        if request.values.get('api_key'):
            try:
                key = ApiKey.get(ApiKey.value == request.values.get('api_key'))
            except Exception:
                key = None

            if key == None:
                return jsonify({"msg": "Invalid apikey"}), 403

            args = list(args)
            args.append(key.user)

            return f(*args, **kwargs)

        return jsonify({"msg": "Missing apikey"}), 403
    return decorated_f



def admin_required(f):
    @wraps(f)
    def decorated_f(*args, **kwargs):
        user = ApiKey.get(ApiKey.value == request.values.get('api_key')).user
        if user.admin:
            return f(*args, **kwargs)
        return jsonify({"msg": "You are not an admin and as such have insufficient permissions to perform this action."});
    return decorated_f