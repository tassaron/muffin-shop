from flask import *
from muffin_shop.blueprint import Blueprint
from muffin_shop.helpers.main.plugins import db
from muffin_shop.decorators import hidden_route
from muffin_shop.models.shop.inventory_models import Product, ProductCategory
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
def int_cents_to_str_currency(cents):
    return "%.2f" % (cents / 100)


@blueprint.index_route()
def index():
    return render_template(
        "shop/shop_index.html",
        product_categories=[
            category[1]
            for category in sorted(
                {
                    db_category.sorting_order: db_category
                    for db_category in ProductCategory.query.all()
                }.items()
            )
        ],
    )


@blueprint.route("/<title>/category/<int:category_id>")
def shop_category_index(title, category_id):
    products = Product.query.filter(
        Product.category_id == deobfuscate_number(category_id), Product.stock > 0
    ).all()
    for product in products:
        product.cart_quantity = session["cart"].get(product.id, 0)
    return render_template(
        "shop/shop_product_list.html",
        products=products,
    )


@blueprint.route("/<title>/<int:product_id>")
def product_description(title, product_id):
    product_id = deobfuscate_number(product_id)
    product = Product.query.filter(
        Product.id == product_id, Product.stock > 0
    ).first_or_404()
    product.cart_quantity = session["cart"].get(product_id, 0)
    return render_template(
        "shop/view_product.html", product=product, title=product.name
    )


@blueprint.route("/all")
def all_products():
    products = Product.query.filter(Product.stock > 0).all()
    for product in products:
        product.cart_quantity = session["cart"].get(product.id, 0)
    return render_template(
        "shop/shop_product_list.html",
        products=products,
    )


@blueprint.route("/view_cart")
def view_cart():
    return render_template(
        "shop/view_cart.html",
        cart=[
            (Product.query.get(id), quantity)
            for id, quantity in session["cart"].items()
        ],
    )
