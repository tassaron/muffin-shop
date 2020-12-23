from flask import *
from tassaron_flask_template.blueprint import Blueprint
import flask_login
from werkzeug.utils import secure_filename
from tassaron_flask_template.main.plugins import bcrypt, db
from tassaron_flask_template.main.models import ShippingAddress
from tassaron_flask_template.decorators import hidden_route
from .inventory_models import Product, ProductCategory
import logging


LOG = logging.getLogger(__package__)


blueprint = Blueprint(
    "shop",
    __name__,
    static_folder="../static",
    template_folder="../templates/shop",
)


@blueprint.app_template_filter("currency")
def float_to_str_currency(num):
    maj, min = str(num).split(".")
    return str(num) if len(min) == 2 else ".".join((maj, f"{min}0"))


@blueprint.index_route()
def index():
    return render_template(
        "shop_index.html",
        no_of_items=0,
        products=[]
        if not db.engine.dialect.has_table(db.engine, "Product")
        else Product.query.all(),
    )


@blueprint.route("/product/<int:product_id>")
def product_description(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    return render_template("view_product.html", product=product, title=product.name)


@blueprint.route("/product/addtocart", methods=["POST"])
def add_to_cart():
    return ""


@blueprint.route("/product/removefromcart", methods=["POST"])
def remove_from_cart():
    return ""


@blueprint.route("/view_cart")
@hidden_route
def view_cart(cart):
    return render_template(
        "view_cart.html",
        cart=cart,
    )


@blueprint.route("/view_shipping_address")
@hidden_route
def view_shipping_address(address):
    field_names = ShippingAddress.names()
    if address is None:
        data = ShippingAddress.default()
    else:
        data_ = {}
        for prop in address.__dict__:
            if prop in field_names:
                data_[prop] = address.__dict__[prop]
        data = {}
        desired_order = list(field_names.keys())
        for prop_id in desired_order:
            data[prop_id] = data_[prop_id]

    return render_template(
        "view_profile_section.html",
        items={
            field_names[prop_id]: prop_value for prop_id, prop_value in data.items()
        },
    )


@blueprint.route("/category/<category_id>")
def category_index():
    return ""
