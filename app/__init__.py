from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
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
    return SQLAlchemy(), Bcrypt(), LoginManager()


def init_plugins(plugins, app):
    for plugin in plugins:
        plugin.init_app(app)


from . import routes
