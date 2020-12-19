from flask import render_template
from tassaron_flask_template.blueprint import Blueprint


blueprint = Blueprint(
    "about",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)


@blueprint.index_route("/")
def about_page():
    return render_template("about.html")