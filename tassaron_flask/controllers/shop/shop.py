from flask import *
from tassaron_flask.blueprint import Blueprint
from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.models.main.models import ShippingAddress
from tassaron_flask.decorators import hidden_route
from tassaron_flask.models.shop.inventory_models import Product, ProductCategory
import logging
import time


LOG = logging.getLogger(__package__)


blueprint = Blueprint(
    "shop",
    __name__,
)


@blueprint.app_template_filter("obfuscate")
def obfuscate_number(x):
    return int(
        (x / 2) * 9038 if ((x / 7) * 7890 if x % 7 == 0 else x % 2) == 0 else x * 3770
    )


def deobfuscate_number(x):
    return int(
        (x / 9038) * 2
        if ((x / 7890) * 7 if x % 7890 == 0 else x % 9038) == 0
        else x / 3770
    )


@blueprint.app_context_processor
def inject_cart_vars():
    return {
        "no_of_items": len(session["cart"]),
    }


@blueprint.before_app_request
def create_cart_session():
    if "cart" not in session:
        session["cart"] = {
            # int product_id: int quantity
        }

    # Delete any in-progress transaction that expired due to timeout
    if (
        "transaction_expiration" in session
        and session["transaction_expiration"] < time.time()
    ):
        try:
            del session["transaction_id"]
            del session["transaction_cart"]
            del session["transaction_expiration"]
        except KeyError:
            pass


@blueprint.app_template_filter("currency")
def float_to_str_currency(num):
    maj, min = str(num).split(".")
    return str(num) if len(min) == 2 else ".".join((maj, f"{min}0"))


@blueprint.index_route()
def index():
    return render_template(
        "shop_index.html",
        product_categories=ProductCategory.query.all(),
    )


@blueprint.route("/<title>/category/<int:category_id>")
def shop_category_index(title, category_id):
    products = Product.query.filter(
        Product.category_id == deobfuscate_number(category_id), Product.stock > 0
    ).all()
    for product in products:
        product.cart_quantity = session["cart"].get(product.id, 0)
    return render_template(
        "shop_product_list.html",
        products=products,
    )


@blueprint.route("/<title>/<int:product_id>")
def product_description(title, product_id):
    product_id = deobfuscate_number(product_id)
    product = Product.query.filter(
        Product.id == product_id, Product.stock > 0
    ).first_or_404()
    product.cart_quantity = session["cart"].get(product_id, 0)
    return render_template("view_product.html", product=product, title=product.name)


@blueprint.route("/all")
def all_products():
    products = Product.query.filter(Product.stock > 0).all()
    for product in products:
        product.cart_quantity = session["cart"].get(product.id, 0)
    return render_template(
        "shop_product_list.html",
        products=products,
    )


@blueprint.route("/view_cart")
def view_cart():
    return render_template(
        "view_cart.html",
        cart=[
            (Product.query.get(id), quantity)
            for id, quantity in session["cart"].items()
        ],
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
