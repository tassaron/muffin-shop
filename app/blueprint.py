import flask


class Blueprint(flask.Blueprint):
    def __init__(self, *args, **kwargs):
        self.__index_route = None
        super().__init__(*args, **kwargs)

    def index_route(self, rule, **options):
        """
        Copy of flask.Blueprint.route but it withholds endpoints with a rule of "/"
        The exact rule of these endpoints won't be known until registration
        """
        def decorator(f):
            endpoint = options.pop("endpoint", None)
            if rule == "/":
                # a potential index rule can't be known until the blueprint is registered
                self.__index_route = (endpoint, f, options)
            else:
                self.add_url_rule(rule, endpoint, f, **options)
            return f

        return decorator

    def register(self, app, options, first_registration=False):
        """
        Called when the Flask instance does register_blueprint in the __init__.py of .blueprints
        """
        if self.__index_route is not None:
            endpoint, f, options = self.__index_route
            if app.modules["main"]["module"] == self.name:
                # this will be the true index of our site!
                self.add_url_rule("/", endpoint, f, **options)
            else:
                app.blueprint_index[self.name] = (endpoint, f, options)

        super().register(app, options, first_registration)