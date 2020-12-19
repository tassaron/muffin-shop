from flask import Blueprint, current_app, render_template, flash
from flask_login import current_user
from tassaron_flask_template.decorators import admin_required
from .inventory_forms import CreateProductForm
import os


blueprint = Blueprint("inventory", __name__, template_folder="../templates/inventory")


@blueprint.route("/create")
@admin_required
def create_product():
    def allowed_file(filename):
        return os.path.splitext(filename) in current_app.config["ALLOWED_EXTENSIONS"]

    return ""


@blueprint.route("/delete/<int:id>")
@admin_required
def delete_product():
    pass


@blueprint.route("/edit/<int:id>")
@admin_required
def edit_product():
    pass
