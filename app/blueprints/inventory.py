from functools import wraps
from flask import Blueprint, current_app
from flask_login import current_user
from mistune import create_markdown


blueprint = Blueprint("inventory", __name__, template_folder="../templates/inventory")


md_to_html = create_markdown(escape=True, renderer="html", plugins=["strikethrough"])


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin_authenticated:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view


@blueprint.route("/add")
@admin_required
def add_inventory_item():
    def allowed_file(filename):
        return os.path.splitext(filename) in current_app.config["ALLOWED_EXTENSIONS"]

    pass


@blueprint.route("/remove")
@admin_required
def remove_inventory_item():
    pass
