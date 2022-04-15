from flask import *
from muffin_shop.blueprint import Blueprint
from muffin_shop.models.shop.inventory_models import Product, ProductCategory
from muffin_shop.helpers.shop.util import obfuscate_number, deobfuscate_number
import logging
import time


LOG = logging.getLogger(__package__)


blueprint = Blueprint(
    "shop",
    __name__,
)


@blueprint.app_template_filter("obfuscate")
def obfuscate_number_template_filter(x):
    return obfuscate_number(x)


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


@blueprint.index_route(endpoint="shop.shop_index")
def shop_index():
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
        "shop/shop_products.html",
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


@blueprint.route("/products")
def all_products():
    products = Product.query.filter(Product.stock > 0).all()
    for product in products:
        product.cart_quantity = session["cart"].get(product.id, 0)
    return render_template(
        "shop/shop_products.html",
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
