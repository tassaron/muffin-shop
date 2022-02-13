from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


def create_plugins():
    return SQLAlchemy(), Migrate(), Bcrypt(), LoginManager()


plugins = create_plugins()
db, migrate, bcrypt, login_manager = plugins
