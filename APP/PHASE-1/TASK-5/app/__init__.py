from flask import Flask, app
from .config.logging import configure_logging
import logging


from .config import Settings
from .extensions import db
from .middleware.request_id import register_request_id
from .api.errors.handlers import register_error_handlers


def create_app():
    app = Flask(__name__)
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Application initialized")
    settings = Settings()

    app.config["APP_ENV"] = settings.APP_ENV
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_REQUEST_SIZE

    db.init_app(app)
    register_request_id(app)
    register_error_handlers(app)

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "ai-revenue-recovery-backend",
            "environment": app.config["APP_ENV"],
        }, 200

    return app