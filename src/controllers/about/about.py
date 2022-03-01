from flask import render_template
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown


blueprint = Blueprint(
    "about",
    __name__,
)


@blueprint.index_route()
def about_page():
    return render_template("about/about.html", about=render_markdown("about.md"))


@blueprint.route("/bio")
def bio_page():
    return render_template("about/bio.html", content=render_markdown("bio.md"))