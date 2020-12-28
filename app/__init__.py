"""
Home to Flask subclass
"""
from tassaron_flask_template.tasks import huey
import flask
from dotenv import load_dotenv
import os
import logging.config
from flask.logging import default_handler
import json
import importlib


load_dotenv(".env")


class ConfigurationError(ValueError):
    pass


class Flask(flask.Flask):
    def __init__(app, *args, **kwargs):
        with open(os.environ.get("LOGGING_CONFIG", "config/logging.json"), "r") as f:
            logging.config.dictConfig(json.load(f))
        app.blueprint_index = {}
        app.admin_routes = []
        super().__init__(*args, **kwargs)
        app.logger.removeHandler(default_handler)
        if app.env == "development":
            huey.immediate = True

    def register_modules(app, modules):
        root_blueprint, others = app.import_modules(modules)
        app.register_blueprint(root_blueprint)
        if not root_blueprint.is_registered_index:
            raise ConfigurationError("The root blueprint failed to register. It must have the same name as its Python module.")
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

        def import_python_modules(pkg, mod_list):
            nonlocal blueprints
            pkg, subpkg = pkg
            for blueprint in mod_list:
                pymodule_name, blueprint_name = blueprint.split(":")
                module = importlib.import_module(
                    f".{pymodule_name}",
                    f"{pkg}.{subpkg}"
                )
                blueprints[pymodule_name] = module.__dict__[blueprint_name]
        
        blueprints = {}
        blueprints["account"] = importlib.import_module(
            f".account", "tassaron_flask_template.main"
        ).__dict__["blueprint"]
        import_python_modules(parse_pkg(main_module), data[main_module]["blueprints"])
        for module_name in data["main"]["navigation"]:
            if module_name not in data:
                raise ConfigurationError(f"Non-existent '{module_name}' module in main module's 'navigation' entry")
            import_python_modules(parse_pkg(module_name), data[module_name]["blueprints"])
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
        app.logger.info("Found root blueprint: %s", root_blueprint.name)
        app.logger.info("Found other blueprints: %s", ", ".join([blueprint for blueprint in blueprints]))
        return (root_blueprint, blueprints)

def parse_pkg(string) -> tuple:
    p = string.split(".", 1)
    if len(p) != 2:
        raise ConfigurationError(f"'{string}' does not specify a parent package")
    if p[0] == "":
        p[0] = "tassaron_flask_template"
    return tuple(p)