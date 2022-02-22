"""WSGI middleware needed for this module"""
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_plugins():
    return (
        SQLAlchemy(),
        Migrate(),
        Bcrypt(),
        LoginManager(),
        Limiter(key_func=get_remote_address),
    )


db, migrate, bcrypt, login_manager, rate_limiter = create_plugins()
