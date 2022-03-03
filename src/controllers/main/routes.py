from flask import render_template, flash, session, url_for, current_app
import flask_login
from itsdangerous import BadSignature
from werkzeug.exceptions import (
    BadRequest,
    Unauthorized,
    Forbidden,
    NotFound,
    MethodNotAllowed,
    RequestEntityTooLarge,
    UnsupportedMediaType,
    InternalServerError,
    TooManyRequests,
)
from werkzeug.routing import BuildError
from functools import lru_cache
from muffin_shop.blueprint import Blueprint


main_routes = Blueprint("main", __name__)


# import images at this point to ensure that all of main_routes is defined
from muffin_shop.controllers.main.images import *


def generic_url_for(rule):
    try:
        generic_url = url_for(
            rule.endpoint, **{arg_name: 1 for arg_name in rule.arguments}
        )
    except BuildError:
        generic_url = rule.endpoint
    return generic_url


@lru_cache
def all_urls():
    return [
        generic_url_for(rule)
        for rule in current_app.url_map.iter_rules()
        if "static" not in rule.endpoint and "GET" in rule.methods
    ]


@lru_cache
def all_base_urls():
    return [
        url_for(rule.endpoint)
        for rule in current_app.url_map.iter_rules()
        if len(rule.arguments) == 0 and "GET" in rule.methods
    ]


@main_routes.before_app_request
def synchronize_server_side_sessions():
    # sync logged-in users across devices
    if not current_app.config["CLIENT_SESSIONS"] and flask_login.current_user.is_authenticated:
        restored_data = current_app.session_interface.get_user_session(flask_login.current_user.id)
        if restored_data:
            upstream_sid, upstream_data = restored_data
            try:
                local_sid = current_app.session_interface.unsign_sid(current_app, request.cookies.get(current_app.session_cookie_name))
            except BadSignature:
                local_sid = current_app.session_interface._generate_sid()
            if local_sid != upstream_sid:
                # change session id when saving the session after the request
                session["sync_local_to_upstream_sid"] = upstream_sid

            if "arcade_tokens" in upstream_data:
                session["arcade_tokens"] = upstream_data["arcade_tokens"]
            if "arcade_prizes" in upstream_data:
                session["arcade_prizes"] = upstream_data["arcade_prizes"]
            session["cart"] = upstream_data["cart"]


@main_routes.admin_route("")
def admin_index():
    endpoints = [
        url
        for url in all_base_urls()
        if url.startswith(current_app.config["ADMIN_URL"])
    ]
    endpoints.remove(current_app.config["ADMIN_URL"])
    return render_template("main/admin.html", endpoints=endpoints)


@main_routes.app_errorhandler(BadRequest)
def client_request_error(error):
    flash("Your request was invalid", "danger")
    return render_template("main/error.html", title=error.name), 400


@main_routes.app_errorhandler(Unauthorized)
def page_unauthorized(error):
    flash("Unauthorized", "danger")
    return render_template("main/error.html", title=error.name), 401


@main_routes.app_errorhandler(Forbidden)
def page_forbidden(error):
    flash("Unauthorized", "danger")
    return render_template("main/error.html", title=error.name), 403


@main_routes.app_errorhandler(NotFound)
def page_not_found(error):
    flash("Sorry, that page doesn't exist", "danger")
    return render_template("main/error.html", title=error.name), 404


@main_routes.app_errorhandler(MethodNotAllowed)
def method_not_allowed_error(error):
    flash(error.description, "danger")
    return render_template("main/error.html", title=error.name), 405


@main_routes.app_errorhandler(RequestEntityTooLarge)
def too_large_upload_error(error):
    flash(
        f"That file was rejected because it is more than {current_app.config['MAX_CONTENT_LENGTH']} bytes",
        "danger",
    )
    return render_template("main/error.html", title=error.name), 413


@main_routes.app_errorhandler(UnsupportedMediaType)
def unsupported_filetype_error(error):
    flash(f"Unsupported file format", "danger")
    return render_template("main/error.html", title=error.name), 415


@main_routes.app_errorhandler(TooManyRequests)
def too_many_requests_error(error):
    flash("You're sending too many requests. Come back later.", "danger")
    return render_template("main/error.html", title=error.name), 429


@main_routes.app_errorhandler(InternalServerError)
def critical_error(error):
    flash("The server experienced an error", "danger")
    return render_template("main/error.html", title=error.name), 500
