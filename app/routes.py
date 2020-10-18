from .__main__ import app, login_manager
from .models import User

# now load each blueprint
from .blueprints import inventory, storefront, account

app.register_blueprint(storefront.blueprint)
for blueprint in (
    account.blueprint,
    inventory.blueprint,
):
    app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")


@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))


login_manager.anonymous_user = lambda: User(email=None, password=None, is_admin=False)
