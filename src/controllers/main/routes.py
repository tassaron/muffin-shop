from flask import render_template, flash, session, url_for, current_app, flash, request
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
from muffin_shop.helpers.main.plugins import db
from datetime import datetime
import os


main_routes = Blueprint("main", __name__)


# import the rest of the main blueprints
import muffin_shop.controllers.main.images
import muffin_shop.controllers.main.markdown


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


@main_routes.app_template_filter("basename")
def basename(path):
    return os.path.basename(path)


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
                if "transaction_id" in session:
                    current_app.logger.warning("Deleting in-progress transaction from an orphaned session (%s)", local_sid)
                    del session["transaction_id"]

            if "arcade_tokens" in upstream_data:
                session["arcade_tokens"] = upstream_data["arcade_tokens"]
            if "arcade_prizes" in upstream_data:
                session["arcade_prizes"] = upstream_data["arcade_prizes"]
            session["cart"] = upstream_data["cart"]


@main_routes.admin_route("")
def admin_index():
    root_dir = os.environ.get('ROOT_DIR', '')
    admin_url = f"{root_dir}{current_app.config['ADMIN_URL']}"
    endpoints = [
        url
        for url in all_base_urls()
        if url.startswith(admin_url)
    ]
    endpoints.remove(admin_url)
    endpoint_names = [
        ' '.join(url[len(root_dir):].split('/')[2:]).title()
        for url in all_base_urls()
        if url.startswith(admin_url)
    ]
    return render_template(
        "main/admin.html",
        endpoints=zip(endpoints, endpoint_names),
        user_name=flask_login.current_user.email
    )


if os.environ.get("CLIENT_SESSIONS", "1") == "0":
    @main_routes.admin_route("/sessions")
    def admin_sessions():
        all_sessions = current_app.session_interface.sql_session_model.query.all()
        data = { sss.id: current_app.session_interface.decrypt(sss.data) for sss in all_sessions }
        kv = {
            sss.session_id: f"USER: {sss.user_id} - EXPIRY: {sss.expiry} - DATA: {data[sss.id]}" for sss in all_sessions
        }
        statuses = {
            sss.session_id: f"{'expired' if sss.expiry <= datetime.utcnow() and sss.user_id is None else 'zombie' if '_user_id' in data[sss.id] and sss.user_id is None else 'deleted' if 'csrf_token' not in data[sss.id] else 'active' if ('arcade_tokens' in data[sss.id] and data[sss.id]['arcade_tokens'] > 0) or ('arcade_prizes' in data[sss.id] and data[sss.id]['arcade_prizes']) or ('cart' in data[sss.id] and data[sss.id]['cart']) else ''}" for sss in all_sessions
        }

        empty_count = 0
        zombie_count = 0
        expired_count = 0
        for sss in all_sessions:
            if statuses[sss.session_id] == "deleted":
                db.session.delete(sss)
                empty_count += 1
            elif statuses[sss.session_id] == "zombie":
                db.session.delete(sss)
                zombie_count += 1
            elif statuses[sss.session_id] == "expired":
                db.session.delete(sss)
                expired_count += 1
        if (sum([empty_count, zombie_count, expired_count]) > 0 ):
            db.session.commit()
            flash(f"Deleted {empty_count} empty sessions, {zombie_count} zombies, {expired_count} expired", "primary")
        return render_template("admin/admin_kv_table.html", title="Sessions", kv=list(kv.items()), statuses=statuses)


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
