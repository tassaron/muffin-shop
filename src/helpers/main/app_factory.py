"""
Entrypoint for initial import of the package in any context
Creates routes/blueprints without creating the app
Home to factories for creating the app and its plugins
"""
from muffin_shop.flask import Flask, create_env_file, prettier_url_safe
from flask import request
import os
import datetime
from typing import Optional
from jinja2 import PrefixLoader, FileSystemLoader
from muffin_shop.helpers.main.plugins import db, login_manager, migrate, init_plugins
from muffin_shop.helpers.main.session_interface import TassaronSessionInterface
from muffin_shop.helpers.main.tasks import huey
from muffin_shop.models.main.models import User


try:
    from uwsgi import setprocname
except ModuleNotFoundError:
    # during test execution uWSGI isn't running
    setprocname = lambda _: None


def create_app():
    """
    First check if the environment has absolutely mandatory keys, such as the Flask secret key
    These keys will be inserted into the .env file if they don't exist, for convenience
    Afterwards this function creates the Flask application object, then updates its config
    Then we import the main module's blueprint from routes.py and register it
    The WSGI application is returned with no plugins initialized nor extra modules imported
    """
    mutated_env_file = create_env_file()
    app = Flask("muffin_shop", static_folder=f"{os.getcwd()}/static")
    app.logger.info("Created Flask instance")
    if mutated_env_file:
        app.logger.warning(".env file was modified programmatically")
    instance = os.environ.get("INSTANCE", "")
    app.config.update(
        SECRET_KEY=os.environ["SECRET_KEY"],
        SERVER_NAME=os.environ.get("SERVER_NAME", None),
        ADMIN_URL=os.environ.get("ADMIN_URL", "/admin"),
        UPLOADS_DEFAULT_DEST=os.environ.get(
            "UPLOADS_PATH", f"static/{f'client/{instance}/' if instance else ''}uploads"
        ),
        MAX_CONTENT_LENGTH=int(os.environ.get("FILESIZE_LIMIT_MB", 2)) * 1024 * 1024,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URI", "sqlite:///db/database.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=boolean_from_env_var(app, "LOG_RAW_SQL"),
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=1800,
        SITE_NAME=(website_name := os.environ.get("SITE_NAME", "The Muffin Shop")),
        SITE_DESCRIPTION=os.environ.get(
            "SITE_DESCRIPTION", "metadescription for your website"
        ),
        FOOTER_YEAR=os.environ.get("FOOTER_YEAR", str(datetime.datetime.now().year)),
        CONFIG_PATH=os.environ.get(
            "CONFIG_PATH", f"config{f'/client/{instance}' if instance else ''}"
        ),
        CLIENT_SESSIONS=boolean_from_env_var(app, "CLIENT_SESSIONS"),
    )

    app.unique_name = prettier_url_safe(website_name)

    # Enforce HTTPS and configure email
    app.config.update(
        EMAIL_API_KEY=os.environ.get("EMAIL_API_KEY", ""),
        EMAIL_API_URL=os.environ.get("EMAIL_API_URL", ""),
        EMAIL_SENDER_NAME=os.environ.get("EMAIL_SENDER_NAME", ""),
        EMAIL_SENDER_ADDRESS=os.environ.get("EMAIL_SENDER_ADDRESS", ""),
    )
    if app.config["EMAIL_API_KEY"] == "":
        # Don't queue tasks for emails, execute them immediately
        huey.immediate = True

    
    if boolean_from_env_var(app, "HTTPS_ONLY", default=True):
        app.config.update(
            SESSION_COOKIE_SECURE=True,
            REMEMBER_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            REMEMBER_COOKIE_HTTPONLY=True,
        )

    # TODO: remove hardcoded paths
    app.jinja_loader = PrefixLoader(
        {
            "main": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/main"
            ),
            "about": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/about"
            ),
            "account": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/account"
            ),
            "admin": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/admin"
            ),
            "arcade": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/arcade"
            ),
            "blog": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/blog"
            ),
            "checkout": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/checkout"
            ),
            "gallery": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/gallery"
            ),
            "inventory": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/inventory"
            ),
            "shop": FileSystemLoader(
                f"{os.getcwd()}/{app.config['CONFIG_PATH']}/templates/shop"
            ),
        }
    )

    from muffin_shop.controllers.main.routes import main_routes

    app.register_blueprint(main_routes)
    return app


def init_app(app, modules: Optional[dict] = None):
    """
    Import and create the Flask plugins, and call init_app for each of them.
    Then register the extra template modules as defined in CONFIG_PATH/modules.json
    In production mode the Monitoring Dashboard is bound to the application
    Configure the Flask-Login's LoginManager, then configure Flask-Uploads
    Give the application some global wrappers for logging and Jinja context
    If `modules` is defined, update the modules dictionary after reading json
    """

    init_plugins(app)
    login_manager.login_view = "account.login"
    login_manager.login_message_category = "info"
    app.register_modules(modules)

    app.session_interface = TassaronSessionInterface(app, db)
    migrate.init_app(app, db)

    if boolean_from_env_var(app, "MONITOR_ENABLED"):
        import flask_monitoringdashboard as monitor

        monitor.config.init_from(
            file=f"{os.environ.get('CONFIG_PATH', 'config')}/monitor.cfg"
        )
        try:
            monitor.config.username = os.environ["MONITOR_USERNAME"]
            monitor.config.password = os.environ["MONITOR_PASSWORD"]
        except KeyError:
            raise KeyError(
                "MONITOR_USERNAME and MONITOR_PASSWORD must be added to .env"
            )
        monitor.config.security_token = os.urandom(24)
        monitor.bind(app)

    @login_manager.user_loader
    def get_user(user_id):
        return User.query.get(int(user_id))

    login_manager.anonymous_user = lambda: User(
        email=None, password=None, is_admin=False
    )

    from flask_uploads import configure_uploads
    from muffin_shop.helpers.main.images import Images

    configure_uploads(app, Images)

    def inject_vars():
        import flask_login

        return {
            "index_route": app.config["INDEX_ROUTE"],
            "logged_in": flask_login.current_user.is_authenticated,
            "site_name": app.config["SITE_NAME"],
            "site_author": os.environ.get("SITE_AUTHOR", app.config["SITE_NAME"]),
            "site_description": app.config["SITE_DESCRIPTION"],
            "footer_year": app.config["FOOTER_YEAR"],
        }

    def set_worker_name():
        setprocname(request.url)

    def log_response(response):
        if response.is_sequence:
            # this line borrowed from werkzeug's Response.__repr__ method
            body_info = f"{(sum(map(len, response.iter_encoded())) / 1024):.2f} kb"
        else:
            body_info = "streamed" if response.is_streamed else "likely-streamed"
        app.logger.info(
            f"{response.status} -> {request.method} {request.url} ({body_info})"
        )
        return response

    app.context_processor(inject_vars)
    app.before_request(set_worker_name)
    app.after_request(log_response)

    return app


def boolean_from_env_var(app, varname, default=False):
    try:
        return bool(int(os.environ.get(varname, default)))
    except ValueError:
        app.logger.error(f"{varname} must be a number (0 is False, otherwise True)")
        return default
