"""
Gallery module shows all images uploaded to the site + the newest blog posts
Currently it depends on the blog module existing but that could change in future
"""
from flask import render_template, url_for
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.markdown import render_markdown
from muffin_shop.helpers.main.images import get_files, get_image_data_path
import json
import os


blueprint = Blueprint(
    "gallery",
    __name__,
)


@blueprint.index_route()
def gallery_index():
    with open(f"{os.environ['BLOG_PATH']}/posts.json", "r") as f:
        posts = json.load(f)
    with open(get_image_data_path("titles"), "r") as f:
        titles = json.load(f)
    return render_template(
        "gallery/gallery_index.html",
        images=[(titles.get(os.path.basename(os.path.splitext(image)[0]), ""), image) for image in get_files(fullpath=True)],
        header=render_markdown("gallery/header.md"),
        footer=render_markdown("gallery/footer.md"),
        posts=reversed(posts),
    )
