import os
import uuid
from flask import (
    render_template,
    redirect,
    url_for,
    request,
    current_app,
    abort,
)

from tassaron_flask.controllers.main.routes import main_routes
from tassaron_flask.forms.main.images import UploadForm
from tassaron_flask.helpers.main.images import Images, validate_image, get_files


@main_routes.admin_route("/images/upload", methods=["GET", "POST"])
def upload_images():
    form = UploadForm()
    if form.validate_on_submit():
        name = uuid.uuid4().hex
        file_ext = os.path.splitext(form.image.data.filename)[1]
        if file_ext.lower() not in (".png", ".jpg", ".gif"):
            abort(415)
        try:
            if file_ext != validate_image(form.image.data.stream):
                abort(415)
        except:
            abort(415)
        Images.save(form.image.data, name=f"{name}.")
        success = True
    else:
        success = False
    return render_template("/upload_images.html", form=form, success=success)


@main_routes.admin_route("/images")
def manage_images():
    files_list = get_files()
    return render_template("/manage_images.html", files_list=files_list)


@main_routes.admin_route("/images/<string:filename>")
def view_image(filename):
    files_list = get_files()
    if filename not in files_list:
        abort(404)
    file_path = Images.path(filename)
    return render_template(
        "/view_image.html",
        file_url=url_for("static", filename=f"uploads/images/{filename}"),
    )


@main_routes.admin_route("/images/<string:filename>/delete")
def delete_image(filename):
    if filename not in get_files():
        abort(404)
    file_path = Images.path(filename)
    try:
        os.remove(file_path)
    except FileNotFoundError:
        abort(404)
    return redirect(url_for("main.manage_images"))
