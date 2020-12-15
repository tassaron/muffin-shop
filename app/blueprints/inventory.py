from flask import Blueprint, current_app, render_template, flash
from flask_login import current_user
from mistune import create_markdown
from tassaron_flask_template.decorators import admin_required


blueprint = Blueprint("inventory", __name__, template_folder="../templates/inventory")


md_to_html = create_markdown(escape=True, renderer="html", plugins=["strikethrough"])


@blueprint.route("/add")
@admin_required
def add_inventory_item():
    def allowed_file(filename):
        return os.path.splitext(filename) in current_app.config["ALLOWED_EXTENSIONS"]

    return ""


@blueprint.route("/remove")
@admin_required
def remove_inventory_item():
    pass
