from .__init__ import create_app, create_plugins, init_plugins

app = create_app()
db, bcrypt, login_manager = create_plugins()
init_plugins((db, bcrypt, login_manager), app)
login_manager.login_view = "account.login"
login_manager.login_message_category = "info"
