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

def get_json_path(page_num):
    return f"{os.environ['BLOG_PATH']}/pages/{'{:0>6d}'.format(page_num)}/posts.json"


@blueprint.index_route()
def blog_index():
    with open(f"{os.environ['BLOG_PATH']}/posts.json", "r") as f:
        posts = json.load(f)
    last_page = len(os.listdir(f"{os.environ['BLOG_PATH']}/pages")) + 1
    return render_template(
        "blog/blog_page.html",
        posts=posts,
        page_range=reversed(range(max(last_page - 12, 1), last_page)),
        page_num=last_page + 1,
        last_page=0 if last_page == 2 and (len(posts) < 5 or not os.path.exists(get_json_path(1))) else last_page,
    )


@blueprint.route("/blog/<int:page_num>")
def blog_page(page_num):
    try:
        path = get_json_path(page_num)
    except Exception as e:
        abort(400)
    if not os.path.exists(path):
        abort(404)
    with open(path, "r") as f:
        posts = json.load(f)
    if not posts:
        abort(404)
    last_page = len(os.listdir(f"{os.environ['BLOG_PATH']}/pages")) + 1
    start = page_num - 6
    end = page_num + 6
    if start < 1:
        end = min(end + abs(start) + 1, last_page)
        start = 1
    elif end > last_page:
        start = max((start - abs(last_page - end)), 1)
        end = last_page
    return render_template(
        "blog/blog_page.html",
        posts=reversed(posts),
        page_range=reversed(range(start, end)),
        page_num=page_num,
        last_page=last_page,
    )
