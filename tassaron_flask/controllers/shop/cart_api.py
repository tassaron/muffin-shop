"""
POST to these Cart endpoints in order to manipulate the Cart Session Cookie
Each endpoint returns a response of success or not, to update the client-side record
"""
from flask import Blueprint, request, session, current_app, url_for
from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.helpers.shop.payment import PaymentAdapter, PaymentSession
from tassaron_flask.helpers.shop.util import (
    convert_raw_cart_data_to_products,
    verify_stock_before_checkout,
)
from tassaron_flask.models.shop.inventory_models import Product


blueprint = Blueprint("cart", __name__)


@blueprint.route("/add", methods=["POST"])
def add_product_to_cart():
    try:
        jsonData = request.get_json()
        id, quantity = (int(jsonData["id"]), int(jsonData["quantity"]))
        product = Product.query.get(id)
        if (
            product is None
            or quantity < 1
            or product.stock < quantity
            or session["cart"].get(id, 0) == product.stock
        ):
            return {"success": False}

        if id not in session["cart"]:
            change = quantity
            session["cart"][id] = quantity
        else:
            new_value = min(product.stock, session["cart"][id] + quantity)
            change = new_value - session["cart"][id]
            session["cart"][id] = new_value
        current_app.logger.debug(session["cart"])
        return {"success": True, "count": len(session["cart"]), "change": change}

    except Exception as e:
        current_app.logger.info("Invalid cart request: %s" % e)
        return {"success": False}, 400


@blueprint.route("/del", methods=["POST"])
def remove_product_from_cart():
    try:
        id = int(request.get_json()["id"])
        product = Product.query.get(id)
        if product is None or id not in session["cart"]:
            return {"success": False}

        session["cart"].pop(id)
        return {"success": True}

    except Exception as e:
        current_app.logger.info("Invalid cart request: %s" % e)
        return {"success": False}, 400


@blueprint.route("/submit", methods=["POST"])
def submit_cart():
    products = request.get_json()
    products = convert_raw_cart_data_to_products(products)
    products, changed_quantities = verify_stock_before_checkout(products)
    if not products or changed_quantities:
        # Either the cart was empty or stock changed
        # Alert the customer so they can decide how to proceed
        return {
            "success": False,
            "changed_quantities": changed_quantities,
        }

    # Adapt our data format into the payment processor's
    products = PaymentAdapter(products).convert()
    print(list(products))
    session = PaymentSession(
        url_for("checkout.successful_checkout", _external=True),
        url_for("checkout.cancel_checkout", _external=True),
        products,
        "payment",
    ).session

    # Begin a session with the payment processor and redirect the client
    return {
        "success": True,
        "session_url": session.url,
    }
