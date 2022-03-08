"""
Root blueprint of the blog module
"""
from flask import render_template, abort
from muffin_shop.blueprint import Blueprint
import os
import json
import datetime


blueprint = Blueprint(
    "blog",
    __name__,
)


@blueprint.app_template_filter("pretty_time")
def pretty_time_formatter(timestamp):
    timestamp = datetime.datetime.strptime(timestamp.split(".", 1)[0], "%Y-%m-%d %H:%M:%S")
    return timestamp.strftime("%-I:%M%p")


@blueprint.app_template_filter("pretty_date")
def pretty_date_formatter(timestamp):
    timestamp = datetime.datetime.strptime(timestamp.split(".", 1)[0], "%Y-%m-%d %H:%M:%S")
    return timestamp.strftime("%b&nbsp;%-d %Y")


def get_json_path(page_num):
    return f"{os.environ['BLOG_PATH']}/pages/{'{:0>6d}'.format(page_num)}/posts.json"


@blueprint.index_route()
def blog_index():
    with open(f"{os.environ['BLOG_PATH']}/posts.json", "r") as f:
        posts = json.load(f)
    last_page = len(os.listdir(f"{os.environ['BLOG_PATH']}/pages"))

    if last_page == 1 and len(posts) < 5:
        # less than 1 page of posts
        last_page = 0
    else:
        with open(get_json_path(last_page)) as f:
            if not json.load(f):
                last_page -= 1

    return render_template(
        "blog/blog_page.html",
        posts=reversed(posts),
        # page_range is a range of 12 clamped by the total number of pages
        page_range=[] if last_page == 0 else reversed(range(max(last_page - 11, 1), last_page + 1)),
        # page_num is the current page which is currently irrelevant for the index
        page_num=last_page + 1,
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
    with open(get_json_path(end-1)) as f:
        if not json.load(f):
            end -= 1
    return render_template(
        "blog/blog_page.html",
        posts=reversed(posts),
        page_range=reversed(range(start, end)),
        page_num=page_num,
    )
