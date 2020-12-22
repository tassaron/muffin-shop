"""
Home to Flask subclass
"""
import flask
from dotenv import load_dotenv
import os
import logging


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

    def register_modules(self):
        from tassaron_flask_template.blueprints import register_blueprints
        register_blueprints(self)
