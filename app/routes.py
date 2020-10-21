from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.exceptions import NotFound, Forbidden


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
