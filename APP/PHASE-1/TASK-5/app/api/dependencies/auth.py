from functools import wraps

from flask import g, jsonify


def get_current_user():
    return getattr(g, "current_user", None)


def require_auth(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        user = get_current_user()

        if user is None:
            return jsonify({
                "error": {
                    "code": "UNAUTHORIZED",
                    "message": "Authentication is required.",
                    "request_id": g.get("request_id"),
                }
            }), 401

        return view_function(*args, **kwargs)

    return wrapper