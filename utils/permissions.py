from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt

def role_required(*roles_autorises):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            claims = get_jwt()
            role = claims.get("role")

            if role not in roles_autorises:

                return jsonify({
                    "status": "error",
                    "message": "Accès refusé."
                }), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator