from flask import *
import flask_login
from werkzeug.utils import secure_filename
from rainbow_shop.plugins import bcrypt, db
from rainbow_shop.models import Product


blueprint = Blueprint(
    "storefront",
    __name__,
    static_folder="../static",
    template_folder="../templates/storefront",
)


@blueprint.app_template_filter("currency")
def float_to_str_currency(num):
    maj, min = str(num).split(".")
    return str(num) if len(min) == 2 else ".".join((maj, f"{min}0"))


@blueprint.route("/")
def index():
    return render_template(
        "storefront_index.html",
        logged_in=flask_login.current_user.is_authenticated,
        no_of_items=0,
        products=[]
        if not db.engine.dialect.has_table(db.engine, "Product")
        else Product.query.all(),
    )


@blueprint.route("/product/<product_id>")
def product_description(product_id):
    return Product.get(product_id)


@blueprint.route("/product/addtocart", methods=["POST"])
def add_to_cart():
    pass


@blueprint.route("/product/removefromcart", methods=["POST"])
def remove_from_cart():
    pass


@blueprint.route("/shoppingcart")
def view_cart():
    pass


@blueprint.route("/category/<category_id>")
def category_index():
    pass
