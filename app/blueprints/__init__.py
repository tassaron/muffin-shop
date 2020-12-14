from . import account
import json
import importlib


def import_modules():
    """Returns a tuple (blueprint for route /, blueprints prefixed by name/)"""
    with open("modules.json", 'r') as f:
        data = json.load(f)
    main_module = data["main"]["module"]

    blueprints = {}
    for blueprint in data[main_module]["blueprints"]:
        module_name, blueprint_name = blueprint.split(":")
        module = importlib.import_module(f".{module_name}", "tassaron_flask_template.blueprints")
        blueprints[module_name] = module.__dict__[blueprint_name]

    root_blueprint = blueprints.pop(data[main_module]["root"])
    return (root_blueprint, blueprints)


def register_blueprints(app):
    root_blueprint, others = import_modules()
    app.register_blueprint(root_blueprint)
    for blueprint in (
        account.blueprint,
        *list(others.values()),
    ):
        app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")
