from flask import *
import flask_login
from werkzeug.utils import secure_filename
from rainbow_shop.__init__ import bcrypt, db
from rainbow_shop.models import Product


blueprint = Blueprint(
    "", __name__, static_folder="../static", template_folder="../templates/storefront"
)


@blueprint.route("")
def index():
    return render_template("storefront_index.html")


@blueprint.route("/product/<product_id>")
def product_description(product_id):
    return Product.get(product_id)


@blueprint.route("/product/addtocart", methods=["POST"])
def add_to_cart():
    pass


@blueprint.route("/product/removefromcart", methods=["POST"])
def remove_from_cart():
    pass


@blueprint.route("/category/<category_id>")
def category_index():
    pass
