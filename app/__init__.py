"""
Home to Flask subclass
"""
import flask
from dotenv import load_dotenv
import os
import logging
import json
import importlib


load_dotenv(".env")
logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.environ.get("LOG_FILE", "debug.log")),
    ],
    format="%(asctime)s %(name)-8.8s [%(levelname)s] %(message)s",
    level=logging.getLevelName(os.environ.get("LOG_LEVEL", "WARNING"))
)


class ConfigurationError(ValueError):
    pass


class Flask(flask.Flask):
    def __init__(app, *args, **kwargs):
        app.blueprint_index = {}
        app.admin_routes = []
        super().__init__(*args, **kwargs)

    def register_modules(app, modules):
        root_blueprint, others = app.import_modules(modules)
        app.register_blueprint(root_blueprint)
        for blueprint in (
            *list(others.values()),
        ):
            app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")
        for blueprint_index, tup in app.blueprint_index.items():
            endpoint, f, options = tup
            app.add_url_rule(f"/{blueprint_index}", endpoint, f, **options)
        app.blueprint_index = {}
        for admin_route in app.admin_routes:
            admin_route(app)

    def import_modules(app, modules):
        """
        Returns a tuple (blueprint for root route /, [blueprints to be prefixed by name])
        Sets INDEX_ROUTE according to the main module's index value
        Ensures that all required env variables have been set
        If arg modules is a dict, it will combine with the modules dict defined in json file
        """
        with open(app.config["MODULES_CONFIG"], "r") as f:
            data = json.load(f)
        if modules is not None:
            data.update(modules)
        main_module = data["main"]["module"]

        def import_python_modules(pkg, lst):
            nonlocal blueprints
            for blueprint in lst:
                pymodule_name, blueprint_name = blueprint.split(":")
                module = importlib.import_module(
                    f".{pymodule_name}", f"tassaron_flask_template.{pkg}"
                )
                blueprints[pymodule_name] = module.__dict__[blueprint_name]

        blueprints = {}
        blueprints["account"] = importlib.import_module(
            f".account", "tassaron_flask_template.main"
        ).__dict__["blueprint"]
        import_python_modules(main_module, data[main_module]["blueprints"])
        for module_name in data["main"]["navigation"]:
            import_python_modules(module_name, data[module_name]["blueprints"])
        root_blueprint = blueprints.pop(data[main_module]["root"])
        app.config["INDEX_ROUTE"] = data[main_module]["index"]

        # ensure env vars are set
        def ensure_env_var(token):
            if token not in os.environ:
                if app.env == "production":
                    raise ConfigurationError(f"Missing {token} from environment vars")
                else:
                    app.logger.warning(f"Missing {token} from environment vars")

        for module in data.values():
            for env_var in module.get("env", []):
                ensure_env_var(env_var)

        app.modules = data

        return (root_blueprint, blueprints)

