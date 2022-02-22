from flask import current_app
import flask_uploads
import os
import imghdr


Images = flask_uploads.UploadSet("images", flask_uploads.IMAGES)


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


def get_files():
    """Returns list of files in the uploads/images directory"""
    return os.listdir(f"{current_app.config['UPLOADS_DEFAULT_DEST']}/images")
