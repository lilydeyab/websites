import uuid

from flask import g, request


def register_request_id(app):

    @app.before_request
    def attach_request_id():
        request_id = request.headers.get("X-Request-ID")

        if not request_id:
            request_id = str(uuid.uuid4())

        g.request_id = request_id

    @app.after_request
    def add_request_id(response):
        response.headers["X-Request-ID"] = g.request_id
        return response