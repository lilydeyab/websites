from functools import wraps

from flask import g, jsonify


ROLE_PERMISSIONS = {
    "OWNER": {
        "manage_company",
        "manage_users",
        "manage_leads",
        "manage_appointments",
        "manage_revenue",
        "view_analytics",
        "manage_integrations",
    },
    "ADMIN": {
        "manage_users",
        "manage_leads",
        "manage_appointments",
        "manage_revenue",
        "view_analytics",
        "manage_integrations",
    },
    "MANAGER": {
        "manage_leads",
        "manage_appointments",
        "manage_revenue",
        "view_analytics",
    },
    "STAFF": {
        "manage_leads",
        "manage_appointments",
    },
}


def has_permission(permission):
    user = getattr(g, "current_user", None)

    if user is None:
        return False

    role = getattr(user, "role", None)

    return permission in ROLE_PERMISSIONS.get(role, set())


def require_permission(permission):
    def decorator(view_function):
        @wraps(view_function)
        def wrapper(*args, **kwargs):
            if getattr(g, "current_user", None) is None:
                return jsonify({
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Authentication is required.",
                        "request_id": g.get("request_id"),
                    }
                }), 401

            if not has_permission(permission):
                return jsonify({
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "You do not have permission to perform this action.",
                        "request_id": g.get("request_id"),
                    }
                }), 403

            return view_function(*args, **kwargs)

        return wrapper

    return decorator