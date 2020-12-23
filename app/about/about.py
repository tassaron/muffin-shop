from flask import render_template
from tassaron_flask_template.blueprint import Blueprint
from tassaron_flask_template.markdown import render_markdown


blueprint = Blueprint(
    "about",
    __name__,
    static_folder="../static",
    template_folder="../templates",
)


@blueprint.index_route()
def about_page():
    return render_template("about.html", about=render_markdown("about.md"))
