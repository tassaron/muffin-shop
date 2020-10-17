from .__init__ import app, login_manager
from .models import User

# now load each blueprint
from .blueprints import inventory, storefront, account

for blueprint in (
    account.blueprint,
    inventory.blueprint,
    storefront.blueprint,
):
    app.register_blueprint(blueprint, url_prefix=f"/{blueprint.name}")


@login_manager.user_loader
def get_user(user_id):
    return User.get(int(user_id))
