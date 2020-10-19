"""
Simply initializes the app and registers all blueprints
"""
from .blueprints import register_blueprints
from .plugins import plugins


def init_app(app):
    for plugin in plugins:
        plugin.init_app(app)
    register_blueprints(app)
    return app
