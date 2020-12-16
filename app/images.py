import os
import uuid
import flask_uploads
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from .routes import main_routes
from .decorators import admin_required


Images = flask_uploads.UploadSet("images", flask_uploads.IMAGES)


class UploadForm(FlaskForm):
    image = FileField(validators=[FileAllowed(Images, 'Image files only'), FileRequired('Must be an image file')])
    submit = SubmitField('Upload')


@main_routes.route('/images/upload', methods=['GET', 'POST'])
@admin_required
def upload_images():
    form = UploadForm()
    if form.validate_on_submit():
        name = uuid.uuid4().hex
        Images.save(form.image.data, name=f"{name}.")
        success = True
    else:
        success = False
    return render_template('upload_images.html', form=form, success=success)


@main_routes.route('/images')
def manage_images():
    files_list = os.listdir(f"{current_app.config['UPLOADS_DEFAULT_DEST']}/images")
    return render_template('manage_images.html', files_list=files_list)


@main_routes.route('/images/<filename>')
def view_image(filename):
    return render_template('view_image.html', file_url=url_for("static", filename=f"uploads/images/{filename}"))


@main_routes.route('/images/<filename>/delete')
def delete_image(filename):
    file_path = Images.path(filename)
    os.remove(file_path)
    return redirect(url_for('main.manage_images'))
