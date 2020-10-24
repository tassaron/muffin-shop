from .__init__ import create_plugins

plugins = create_plugins()
db, migrate, bcrypt, login_manager = plugins
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"
