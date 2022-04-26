import os
import json
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Wiper Portal"
    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
    ADMIN_PASS = os.environ.get("ADMIN_PASS", "pass")

    ALPHABET_FULL = os.environ.get(
        "ALPHABET_FULL", "ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789"
    )

    ALPHABET_UP_DIGITS = os.environ.get(
        "ALPHABET_UP_DIGITS", "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
    )

    AUTH_OTP_ENABLED = json.loads(os.environ.get("AUTH_OTP_ENABLED", "true"))

    PAGE_SIZE = int(os.environ.get("PAGE_SIZE", 17))
    LDAP_SERVER = os.environ.get("LDAP_SERVER", None)
    LDAP_USER = os.environ.get("LDAP_USER", None)
    LDAP_PASS = os.environ.get("LDAP_PASS", None)
    AD_NAME = os.environ.get("AD_NAME", "DC=wiper,DC=tel")

    REMOTE_SHELL_SERVER: str = os.environ.get("REMOTE_SHELL_SERVER", None)
    REMOTE_SHELL_USER: str = os.environ.get("REMOTE_SHELL_USER", None)
    REMOTE_SHELL_PASS: str = os.environ.get("REMOTE_SHELL_PASS", None)
    REMOTE_SHELL_PORT: int = int(os.environ.get("REMOTE_SHELL_PORT", 0))

    BASE_MDM_API_URL = os.environ.get("BASE_MDM_API_URL", None)
    MDM_API_KEY = os.environ.get("MDM_API_KEY", None)

    JAVA_SERVER_KEY = os.environ.get("JAVA_SERVER_KEY", "unknown key value")

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

    URL_JAVA_SRV = os.environ.get("DEV_URL_JAVA_SRV", None)


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3"),
    )

    URL_JAVA_SRV = os.environ.get("DEV_URL_JAVA_SRV", None)


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True

    URL_JAVA_SRV = os.environ.get("URL_JAVA_SRV", None)


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
