"""
Root blueprint of the blog module
"""
from flask import render_template, abort, request, current_app
from muffin_shop.blueprint import Blueprint
import os
import json


blueprint = Blueprint(
    "blog",
    __name__,
)


@blueprint.index_route()
def blog_index():
    with open(f"{os.environ['BLOG_PATH']}/posts.json", "r") as f:
        posts = json.load(f)
    return render_template(
        "blog/blog_newest_posts.html",
        posts=posts,
    )
