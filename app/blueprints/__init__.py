from . import account
import json
import importlib
import os
import logging


LOG = logging.getLogger(__package__)


class ConfigurationError(KeyError):
    pass


def import_modules(app):
    """
    Returns a tuple (blueprint for root route /, [blueprints to be prefixed by name])
    Sets INDEX_ROUTE according to the main module's index value
    Ensures that all required env variables have been set
    """
    with open("modules.json", 'r') as f:
        data = json.load(f)
    main_module = data["main"]["module"]

    blueprints = {}
    for blueprint in data[main_module]["blueprints"]:
        module_name, blueprint_name = blueprint.split(":")
        module = importlib.import_module(f".{module_name}", "tassaron_flask_template.blueprints")
        blueprints[module_name] = module.__dict__[blueprint_name]

    root_blueprint = blueprints.pop(data[main_module]["root"])
    app.config["INDEX_ROUTE"] = data[main_module]["index"]

    # ensure env vars are set
    def ensure_env_var(token):
        if token not in os.environ:
            if app.config["FLASK_ENV"] == "production":
                raise ConfigurationError(f"Missing {token} from environment vars")
            else:
                LOG.warning(f"Missing {token} from environment vars")

    data.pop("main")
    for module in data.values():
        for env_var in module["env"]:
            ensure_env_var(env_var)

    app.modules = data

    return (root_blueprint, blueprints)


def register_blueprints(app):
    root_blueprint, others = import_modules(app)
    app.register_blueprint(root_blueprint)
    for blueprint in (
        account.blueprint,
        *list(others.values()),
    ):
        app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")
