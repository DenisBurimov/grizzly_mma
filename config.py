import os
import json
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Hit Portal"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
    ADMIN_PASS = os.environ.get("ADMIN_PASS", "admin")

    ALPHABET_FULL = os.environ.get(
        "ALPHABET_FULL", "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
    )

    ALPHABET_UP_DIGITS = os.environ.get(
        "ALPHABET_UP_DIGITS", "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
    )

    AUTH_OTP_ENABLED = json.loads(os.environ.get("AUTH_OTP_ENABLED", "true"))

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVEL_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-devel.sqlite3"),
    )

    # AUTH_OTP_ENABLED = False


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
