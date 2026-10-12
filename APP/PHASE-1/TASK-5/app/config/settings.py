import os


class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-only-secret"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///development.db"
    )

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    AI_API_KEY = os.getenv("AI_API_KEY")

    SMS_API_KEY = os.getenv("SMS_API_KEY")

    EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")

    CALENDAR_API_KEY = os.getenv("CALENDAR_API_KEY")

    PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")

    REQUEST_TIMEOUT = int(
        os.getenv("REQUEST_TIMEOUT", "30")
    )

    MAX_REQUEST_SIZE = int(
        os.getenv("MAX_REQUEST_SIZE", str(5 * 1024 * 1024))
    )