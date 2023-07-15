import flask
import os
from muffin_shop.flask import parse_pkg, admin_required


ADMIN_URL = os.environ.get("ADMIN_URL", "/admin")


class Blueprint(flask.Blueprint):
    def __init__(self, *args, **kwargs):
        self.__index_route = None
        self.__admin_routes = []
        self.is_registered_index = False
        super().__init__(*args, **kwargs)

    def admin_route(self, rule, **options):
        """
        Copy of flask.Blueprint.route but for admin routes. This prepends the admin_url
        and ensures that the route is protected by the @admin_required decorator
        """

        def decorator(f):
            new_rule = (
                f"{ADMIN_URL}{'' if self.name == 'main' else f'/{self.name}'}{rule}"
            )
            endpoint = options.pop("endpoint", f"{self.name}.{f.__name__}")

            def add_admin_url_rule(app):
                app.add_url_rule(new_rule, endpoint, admin_required(f), **options)

            self.__admin_routes.append(add_admin_url_rule)
            return f

        return decorator

    def index_route(self, **options):
        """
        Copy of flask.Blueprint.route but it withholds endpoints with a rule of "/"
        The exact rule of these endpoints won't be known until registration
        """
        rule = "/"

        def decorator(f):
            endpoint = options.pop("endpoint", None)
            self.__index_route = (endpoint, f, options)
            return f

        return decorator

    def register(self, app, options):
        """
        Called when the Flask instance does register_blueprint
        """
        if self.__index_route is not None:
            endpoint, f, options = self.__index_route
            if parse_pkg(app.modules["main"]["module"])[-1] == self.name:
                # this will be the true index of our site!
                try:
                    self.add_url_rule("/", None, f, **options)
                except AssertionError as e:
                    if not app.config["TESTING"]:
                        raise
                    app.logger.warning(
                        "Failed attempt to re-register the index blueprint. This is a known bug during testing."
                    )
                self.is_registered_index = True
            else:
                app.blueprint_index[self.name] = (endpoint, f, options)

        app.admin_routes.extend(self.__admin_routes)
        super().register(app, options)
