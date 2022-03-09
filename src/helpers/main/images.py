from flask import current_app
import flask_uploads
import os
import imghdr

images_str = "images"
Images = flask_uploads.UploadSet(images_str, flask_uploads.IMAGES)


def validate_image(stream):
    """
    Useful function borrowed from blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
    Checks to see if header of a bytestream claims that the file is an image
    """
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


def get_files(asset="images", fullpath=False):
    """Returns list of files in the uploads/images directory"""
    path = f"{current_app.config['UPLOADS_DEFAULT_DEST']}/{asset}"
    if not os.path.exists(path):
        os.makedirs(path)
    files_list = os.listdir(path)
    try:
        files_list.remove("data")
    except ValueError:
        pass
    if fullpath:
        return [f"/{path}/{file}" for file in files_list]
    return files_list


def get_image_data_path(value):
    _path = f"{current_app.config['UPLOADS_DEFAULT_DEST']}/{images_str}/data/{value}.json"
    if not os.path.exists(_path):
        if not os.path.exists(os.path.dirname(_path)):
            os.makedirs(os.path.dirname(_path))
        with open(_path, "w") as f:
            f.write("{}")
    return _path