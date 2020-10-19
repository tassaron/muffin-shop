"""
Entrypoint for initial import of the package in any context
Creates routes/blueprints without creating the app
Home to factories for creating the app and its plugins
"""
from flask import Flask
import os


def create_app():
    app = Flask("rainbow_shop")
    app.config.update(
        SECRET_KEY=os.urandom(16),
        UPLOAD_FOLDER="static/uploads",
        ALLOWED_EXTENSIONS={"jpeg", "jpg", "png", "gif"},
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,  # 2MB
        SQLALCHEMY_DATABASE_URI="sqlite+pysqlite:///db/database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    return app


def create_plugins():
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_bcrypt import Bcrypt

    return SQLAlchemy(), Bcrypt(), LoginManager()
