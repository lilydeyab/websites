from flask import g


def get_current_company():
    return getattr(g, "current_company", None)


def require_tenant():
    company = get_current_company()

    if company is None:
        raise PermissionError("Company context is required.")

    return company