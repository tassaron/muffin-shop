from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from werkzeug.exceptions import NotFound, Forbidden, InternalServerError, RequestEntityTooLarge


main_routes = Blueprint("main", __name__)


@main_routes.route("/about")
def about_page():
    return render_template("about.html")


@main_routes.app_errorhandler(NotFound)
def page_not_found(error):
    flash("Sorry, that page doesn't exist", "danger")
    return render_template("index.html"), 404


@main_routes.app_errorhandler(Forbidden)
def page_forbidden(error):
    flash("Unauthorized", "danger")
    return render_template("index.html"), 403


@main_routes.app_errorhandler(RequestEntityTooLarge)
def too_large_upload_error(error):
    flash(f"That file was rejected because it is more than {current_app.config['MAX_CONTENT_LENGTH']} bytes", "danger")
    return render_template("index.html"), 413


@main_routes.app_errorhandler(InternalServerError)
def critical_error(error):
    flash("The server experienced an error", "danger")
    return render_template("index.html"), 500
