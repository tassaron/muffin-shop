"""Admin routes for editing markdown"""
from flask import render_template, current_app, abort, flash, redirect, url_for
from muffin_shop.blueprint import Blueprint
from muffin_shop.controllers.main.routes import main_routes
from muffin_shop.forms.blog.post_forms import BlogPostForm
from werkzeug.datastructures import MultiDict
import os


@main_routes.admin_route("/markdown")
def admin_list_markdown():
    files = [
        (os.path.basename(dir_), file)
        for dir_, __, file in os.walk(f"{current_app.config['CONFIG_PATH']}/markdown")
    ]
    files = files[1:]
    return render_template("admin/list_markdown.html", files=files)


@main_routes.admin_route("/markdown/edit/<section>/<filename>", methods=["GET", "POST"])
def admin_edit_markdown(section, filename):
    path = f"{current_app.config['CONFIG_PATH']}/markdown/{section}/{filename}"
    if not os.path.exists(path):
        abort(404)

    with open(path, "r") as f:
        lines = [line for line in f]

    form = BlogPostForm()
    if form.validate_on_submit():
        try:
            with open(path, "w") as f:
                f.write(form.content.data)
            flash("Edited that page! ✔️", "success")
        except Exception:
            flash("Error", "danger")
        return redirect(url_for("main.admin_list_markdown"))

    filled_form = {"content": "".join(lines)}
    form = BlogPostForm(formdata=MultiDict(filled_form))
    return render_template(
        "admin/edit_form.html", title=f"Edit {section}/{filename}", form=form
    )
