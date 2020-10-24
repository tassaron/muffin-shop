"""
Simply initializes the app and registers all blueprints
"""
from .blueprints import register_blueprints
from .plugins import plugins


def init_app(app):
    db, migrate, bcrypt, login_manager = plugins
    for plugin in (db, bcrypt, login_manager):
        plugin.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
    return app
