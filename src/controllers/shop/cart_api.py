"""
POST to these Cart endpoints in order to manipulate the Cart Session Cookie
Each endpoint returns a response of success or not, to update the client-side record
"""
from flask import Blueprint, request, session, current_app, url_for, session
import flask_login
from muffin_shop.helpers.main.plugins import db
from muffin_shop.helpers.shop.payment import PaymentAdapter
from muffin_shop.helpers.shop.util import (
    convert_raw_cart_data_to_products,
    verify_stock_before_checkout,
)
from muffin_shop.models.shop.inventory_models import Product
from muffin_shop.models.shop.checkout_models import Transaction
import time


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
    if "transaction_id" in session:
        current_app.logger.info(
            "Failed cart submission because a transaction is still in progress"
        )
        return {
            "success": False,
            "changed_quantities": {},
        }

    products = request.get_json()
    products = convert_raw_cart_data_to_products(products)
    changed_quantities = verify_stock_before_checkout(products)
    if not products or changed_quantities:
        # Either the cart was empty or stock changed
        # Alert the customer so they can decide how to proceed
        return {
            "success": False,
            "changed_quantities": changed_quantities,
        }

    # Start a session with the payment processor
    payment_session = PaymentAdapter(products).start_session(
        url_for("checkout.successful_checkout", _external=True),
        url_for("checkout.cancel_checkout", _external=True),
        "payment",
        None
        if not flask_login.current_user.is_authenticated
        else flask_login.current_user.email,
    )

    # Record beginning of the transaction for our internal records
    new_transaction = Transaction(
        uuid=payment_session.id,
        products=str(products),
        user_id=None
        if not flask_login.current_user.is_authenticated
        else int(flask_login.current_user.get_id()),
    )
    try:
        db.session.add(new_transaction)
        db.session.commit()
    except IntegrityError as e:
        current_app.logger.critical(
            "Critical error occurred while trying to create a new transaction record: %s",
            e,
        )
        db.session.rollback()

    session["transaction_id"] = payment_session.id
    session["transaction_expiration"] = int(time.time() + 3600)
    session["transaction_cart"] = dict(session["cart"])
    session["cart"] = {}

    # Redirect the client to complete the checkout session
    return {
        "success": True,
        "session_url": payment_session.url,
    }
