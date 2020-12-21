from functools import wraps
from flask_login import current_user
from flask import current_app, abort


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
