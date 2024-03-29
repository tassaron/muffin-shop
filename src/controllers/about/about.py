from flask import render_template
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown


blueprint = Blueprint(
    "about",
    __name__,
)


@blueprint.index_route(endpoint="about.about_page")
def about_page():
    return render_template("about/about.html", about=render_markdown("about/about.md"))


@blueprint.route("/bio")
def bio_page():
    return render_template("about/bio.html", content=render_markdown("about/bio.md"))


@blueprint.route("/resume")
def resume_page():
    return render_template(
        "about/resume.html", content=render_markdown("about/resume.md")
    )
