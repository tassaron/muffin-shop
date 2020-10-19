"""
Entrypoint for uWSGI
"""
from .__init__ import create_app
from .app import init_app

app = create_app()
app = init_app(app)
