"""
Simply initializes the app and registers all blueprints
"""
from .blueprints import register_blueprints
from .plugins import plugins


def init_app(app):
    db, migrate, bcrypt, login_manager = plugins
    for plugin in (db, bcrypt, login_manager):
        plugin.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)

    from .models import User

    @login_manager.user_loader
    def get_user(user_id):
        return User.query.get(int(user_id))

    login_manager.anonymous_user = lambda: User(
        email=None, password=None, is_admin=False
    )
    return app
