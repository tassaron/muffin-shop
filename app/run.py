"""
Entrypoint for uWSGI or __main__, where a WSGI application is actually created
"""
from tassaron_flask_template.main import create_app, init_app
from tassaron_flask_template.main.plugins import login_manager

application = create_app()
application = init_app(application)
