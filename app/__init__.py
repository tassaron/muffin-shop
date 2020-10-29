"""
Entrypoint for initial import of the package in any context
Creates routes/blueprints without creating the app
Home to factories for creating the app and its plugins
"""
from flask import Flask
from dotenv import load_dotenv
import os
import logging
from .routes import main_routes


load_dotenv(".env")
LOG = logging.getLogger(__package__)
logging.basicConfig(filename=os.environ.get("LOG_FILE", "debug.log"))
LOG.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "WARNING")))


def create_app():
    LOG.info("Creating app")
    if "SECRET_KEY" not in os.environ:
        LOG.warning("Creating new SECRET_KEY")
        with open(".env", "a") as f:
            f.write(f"\nFLASK_APP=tassaron_flask_template.run:app\nSECRET_KEY={os.urandom(24)}\n")
    app = Flask("tassaron_flask_template")
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", os.urandom(24)),
        UPLOAD_FOLDER="static/uploads",
        ALLOWED_EXTENSIONS={"jpeg", "jpg", "png", "gif"},
        MAX_CONTENT_LENGTH=int(os.environ.get("FILESIZE_LIMIT_MB", 2)) * 1024 * 1024,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URI", "sqlite+pysqlite:///db/database.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=1800,
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
    )
    app.register_blueprint(main_routes)
    return app


def create_plugins():
    LOG.info("Creating plugins")
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_bcrypt import Bcrypt
    from flask_migrate import Migrate

    return SQLAlchemy(), Migrate(), Bcrypt(), LoginManager()
