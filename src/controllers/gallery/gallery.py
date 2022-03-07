from flask import render_template, url_for
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown
from muffin_shop.helpers.main.images import get_files


blueprint = Blueprint(
    "gallery",
    __name__,
)


@blueprint.index_route()
def gallery_page():
    return render_template(
        "gallery/gallery_index.html",
        images=[url_for('static', filename=f'uploads/images/{image}') for image in get_files()],
        header=render_markdown("gallery/header.md"),
        footer=render_markdown("gallery/footer.md")
    )
