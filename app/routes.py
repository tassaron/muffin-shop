from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from werkzeug.exceptions import (
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    MethodNotAllowed,
    RequestEntityTooLarge,
    UnsupportedMediaType,
    InternalServerError,
)


main_routes = Blueprint("main", __name__)


# import images at this point to ensure that all of main_routes is defined
from .images import *


@main_routes.app_errorhandler(BadRequest)
def client_request_error(error):
    flash("Your request was invalid", "danger")
    return render_template("error.html", title=error.name), 400


@main_routes.app_errorhandler(Unauthorized)
def page_unauthorized(error):
    flash("Unauthorized", "danger")
    return render_template("error.html", title=error.name), 401


@main_routes.app_errorhandler(Forbidden)
def page_forbidden(error):
    flash("Unauthorized", "danger")
    return render_template("error.html", title=error.name), 403


@main_routes.app_errorhandler(NotFound)
def page_not_found(error):
    flash("Sorry, that page doesn't exist", "danger")
    return render_template("error.html", title=error.name), 404


@main_routes.app_errorhandler(MethodNotAllowed)
def method_not_allowed_error(error):
    flash(error.description, "danger")
    return render_template("error.html", title=error.name), 405


@main_routes.app_errorhandler(RequestEntityTooLarge)
def too_large_upload_error(error):
    flash(
        f"That file was rejected because it is more than {current_app.config['MAX_CONTENT_LENGTH']} bytes",
        "danger",
    )
    return render_template("error.html", title=error.name), 413


@main_routes.app_errorhandler(UnsupportedMediaType)
def unsupported_filetype_error(error):
    flash(f"Unsupported file format", "danger")
    return render_template("error.html", title=error.name), 415


@main_routes.app_errorhandler(InternalServerError)
def critical_error(error):
    flash("The server experienced an error", "danger")
    return render_template("error.html", title=error.name), 500
