from flask import Blueprint, current_app
from mistune import create_markdown


blueprint = Blueprint("inventory", __name__, template_folder="../templates/inventory")


md_to_html = create_markdown(escape=True, renderer="html", plugins=["strikethrough"])


@blueprint.route("/add")
def add_inventory_item():
    def allowed_file(filename):
        return os.path.splitext(filename) in current_app.config["ALLOWED_EXTENSIONS"]

    pass


@blueprint.route("/remove")
def remove_inventory_item():
    pass
