"""
Root blueprint of the blog module
"""
from werkzeug.datastructures import MultiDict
from flask import render_template, abort, flash, redirect, url_for
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.json import get_json_archive_path, insert_to_json_archive, remove_from_json_archive
from muffin_shop.forms.blog.post_forms import BlogPostForm
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


@blueprint.index_route(endpoint="blog.blog_index")
def blog_index():
    with open(f"{os.environ['BLOG_PATH']}/posts.json", "r") as f:
        posts = json.load(f)
    last_page = len(os.listdir(f"{os.environ['BLOG_PATH']}/pages"))

    if last_page == 1 and len(posts) < 5:
        # less than 1 page of posts
        last_page = 0
    else:
        with open(get_json_archive_path(os.environ['BLOG_PATH'], last_page)) as f:
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
        path = get_json_archive_path(os.environ['BLOG_PATH'], page_num)
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
    with open(get_json_archive_path(os.environ['BLOG_PATH'], end-1)) as f:
        if not json.load(f):
            end -= 1
    return render_template(
        "blog/blog_page.html",
        posts=reversed(posts),
        page_range=reversed(range(start, end)),
        page_num=page_num,
    )


@blueprint.admin_route("")
def admin_blog_index():
    with open(f"{os.environ['BLOG_PATH']}/posts.json", "r") as f:
        posts = json.load(f)
    return render_template("admin/admin_blog_index.html", posts=reversed(posts))


@blueprint.admin_route('/post', methods=["GET", "POST"])
def blog_new_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        new_post = {
            "url": "",
            "created_at": f"{str(datetime.datetime.utcnow())}+00:00",
            "images": [],            
            "content": form.content.data,
        }
        success = insert_to_json_archive(f"{os.environ['BLOG_PATH']}/posts.json", new_post)
        flash("Created new post! ✔️" if success else "Error", "success" if success else "danger")
        return redirect(url_for("main.admin_index"))
    return render_template("admin/edit_form.html", title="New Blog Post", form=form)


@blueprint.admin_route('/post/delete/<int:post_id>')
def blog_delete_post(post_id):
    if not remove_from_json_archive(f"{os.environ['BLOG_PATH']}/posts.json", post_id):
        abort(404)
    flash("Post deleted", "danger")
    return redirect(url_for("blog.admin_blog_index"))


@blueprint.admin_route('/post/edit/<int:post_id>', methods=["GET", "POST"])
def blog_edit_post(post_id):
    with open(f"{os.environ['BLOG_PATH']}/posts.json", "r") as f:
        posts = json.load(f)
    form = BlogPostForm()
    if form.validate_on_submit():
        posts[post_id]["content"] = form.content.data
        try:
            with open(f"{os.environ['BLOG_PATH']}/posts.json", "w") as f:
                json.dump(posts, f)
            flash("Edited that post! ✔️", "success")
        except Exception:
            flash("Error", "danger")
        return redirect(url_for("blog.admin_blog_index"))

    filled_form = {
        "content": posts[post_id]["content"]
    }
    form = BlogPostForm(formdata=MultiDict(filled_form))
    return render_template("admin/edit_form.html", title="Edit Blog Post", form=form)

