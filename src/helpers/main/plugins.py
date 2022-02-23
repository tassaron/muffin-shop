"""WSGI middleware needed for this module"""
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect


def create_plugins():
    return (
        SQLAlchemy(),
        Migrate(),
        Bcrypt(),
        LoginManager(),
        Limiter(key_func=get_remote_address),
        CSRFProtect(),
    )


db, migrate, bcrypt, login_manager, rate_limiter, anti_csrf = create_plugins()


def init_plugins(app):
    for plugin in (db, bcrypt, login_manager, rate_limiter, anti_csrf):
        plugin.init_app(app)
