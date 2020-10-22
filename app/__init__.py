"""
Entrypoint for initial import of the package in any context
Creates routes/blueprints without creating the app
Home to factories for creating the app and its plugins
"""
from flask import Flask
from dotenv import load_dotenv
import os
from .routes import main_routes

if not os.path.exists(".env"):
    with open(".env", "w") as f:
        f.write(f"SECRET_KEY={os.urandom(16)}\n")

load_dotenv()


def create_app():
    app = Flask("rainbow_shop")
    app.config.update(
        SECRET_KEY=os.environ["SECRET_KEY"],
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
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_bcrypt import Bcrypt

    return SQLAlchemy(), Bcrypt(), LoginManager()
