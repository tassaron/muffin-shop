"""
Entrypoint for initial import of the package in any context
Creates routes/blueprints without creating the app
Home to factories for creating the app and its plugins
"""
import flask
from dotenv import load_dotenv
import os
import datetime
import logging
from .routes import main_routes


logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.environ.get("LOG_FILE", "debug.log")),
    ],
    format="%(asctime)s %(name)-8.8s [%(levelname)s] %(message)s",
    level=logging.getLevelName(os.environ.get("LOG_LEVEL", "WARNING"))
)
load_dotenv(".env")


class Flask(flask.Flask):
    def __init__(self, *args, **kwargs):
        self.blueprint_index = {}
        self.admin_routes = []
        super().__init__(*args, **kwargs)


def create_app():
    mutated_env_file = False
    def create_ensure_env_var_func():
        default_values = {
            "FLASK_APP": "tassaron_flask_template.run:app",
            "FLASK_ENV": "development",
            "SECRET_KEY": os.urandom(24),
        }
        mutation = False
        if os.path.exists(".env"):
            mutation = True
        def ensure_env_var(token):
            nonlocal mutated_env_file
            if token not in os.environ:
                mutated_env_file = mutation
                with open(".env", "a") as f:
                    f.write(f"\n{str(token)}={default_values[token]}")

        return ensure_env_var

    # FLASK_ENV must be set in the environment before the Flask instance is created
    ensure_env_var = create_ensure_env_var_func()
    ensure_env_var("FLASK_APP")
    ensure_env_var("FLASK_ENV")
    ensure_env_var("SECRET_KEY")
    load_dotenv(".env")

    app = Flask("tassaron_flask_template")
    app.logger.info("Created Flask instance")
    if mutated_env_file:
        app.logger.warning(".env file was modified programmatically")
    app.config.update(
        SECRET_KEY=os.environ["SECRET_KEY"],
        SERVER_NAME=os.environ.get("SERVER_NAME", None),
        ADMIN_URL=os.environ.get("ADMIN_URL", "/admin"),
        UPLOADS_DEFAULT_DEST="app/static/uploads",
        MAX_CONTENT_LENGTH=int(os.environ.get("FILESIZE_LIMIT_MB", 2)) * 1024 * 1024,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URI", "sqlite+pysqlite:///db/database.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True,
        WTF_CSRF_TIME_LIMIT=1800,
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SITE_NAME=os.environ.get("SITE_NAME", "Your Website Name Here"),
        FOOTER_YEAR=os.environ.get("FOOTER_YEAR", str(datetime.datetime.now().year)),
    )

    if app.env == "production":
        # Configure email
        try:
            app.config["EMAIL_API_KEY"] = os.environ["EMAIL_API_KEY"]
            app.config["EMAIL_API_URL"] = os.environ["EMAIL_API_URL"]
            app.config["EMAIL_SENDER_NAME"] = os.environ["EMAIL_SENDER_NAME"]
            app.config["EMAIL_SENDER_ADDRESS"] = os.environ["EMAIL_SENDER_ADDRESS"]
        except KeyError as e:
            raise KeyError(f"{e} is missing from .env")
    else:
        app.logger.warning("Email is disabled because FLASK_ENV != production")

    app.register_blueprint(main_routes)
    return app


def create_plugins():
    from flask_login import LoginManager
    from flask_sqlalchemy import SQLAlchemy
    from flask_bcrypt import Bcrypt
    from flask_migrate import Migrate

    return SQLAlchemy(), Migrate(), Bcrypt(), LoginManager()
