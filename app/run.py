"""
Entrypoint for uWSGI
Simply initializes the app
"""
from .app import app
from .plugins import plugins

for plugin in plugins:
    plugin.init_app(app)
