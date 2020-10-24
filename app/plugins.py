from .__init__ import create_plugins

plugins = create_plugins()
db, migrate, bcrypt, login_manager = plugins
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"

from .models import User


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


login_manager.anonymous_user = lambda: User(email=None, password=None, is_admin=False)
