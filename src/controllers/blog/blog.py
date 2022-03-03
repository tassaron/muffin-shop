"""
Root blueprint of the blog module
"""
from flask import render_template, abort
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
        "blog/blog_page.html",
        posts=posts,
    )


@blueprint.route("/blog/<int:page_num>")
def blog_page(page_num):
    try:
        path = f"{os.environ['BLOG_PATH']}/pages/{'{:0>6d}'.format(page_num)}/posts.json"
    except Exception as e:
        abort(400)
    if not os.path.exists(path):
        abort(404)
    with open(path, "r") as f:
        posts = json.load(f)
    if not posts:
        abort(404)
    return render_template(
        "blog/blog_page.html",
        posts=posts,
    )