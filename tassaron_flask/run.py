"""
Entrypoint for uWSGI or __main__, where a WSGI application is actually created
"""
from tassaron_flask.helpers.main.app_factory import create_app, init_app

application = create_app()
application = init_app(application)
