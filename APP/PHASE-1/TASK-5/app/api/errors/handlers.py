from flask import jsonify, g


def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "The request is invalid.",
                "request_id": g.get("request_id"),
            }
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Authentication is required.",
                "request_id": g.get("request_id"),
            }
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "error": {
                "code": "FORBIDDEN",
                "message": "You do not have permission to perform this action.",
                "request_id": g.get("request_id"),
            }
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "The requested resource was not found.",
                "request_id": g.get("request_id"),
            }
        }), 404

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            "error": {
                "code": "CONFLICT",
                "message": "The request conflicts with the current state.",
                "request_id": g.get("request_id"),
            }
        }), 409

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "error": {
                "code": "UNPROCESSABLE_ENTITY",
                "message": "The request could not be processed.",
                "request_id": g.get("request_id"),
            }
        }), 422

    @app.errorhandler(429)
    def too_many_requests(error):
        return jsonify({
            "error": {
                "code": "TOO_MANY_REQUESTS",
                "message": "Too many requests.",
                "request_id": g.get("request_id"),
            }
        }), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred.",
                "request_id": g.get("request_id"),
            }
        }), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({
            "error": {
                "code": "SERVICE_UNAVAILABLE",
                "message": "The service is temporarily unavailable.",
                "request_id": g.get("request_id"),
            }
        }), 503