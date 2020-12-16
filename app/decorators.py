from functools import wraps
from flask_login import current_user
from flask import current_app, abort


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin_authenticated:
            # pretend it doesn't exist
            abort(404)
        return func(*args, **kwargs)

    return decorated_view


def hidden_route(func):
    """
    Allow a Flask route without arguments in the URL to accept arguments nonetheless;
    thus it's not really an endpoint anymore but we can still use Flask's routing rules
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if len(args) == 0:
            abort(404)
        return func(*args, **kwargs)

    return decorated_view