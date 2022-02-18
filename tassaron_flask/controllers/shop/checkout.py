from tassaron_flask.blueprint import Blueprint
from flask import (
    session,
    request,
    current_app,
    render_template,
    abort,
    redirect,
    url_for,
)
from tassaron_flask.helpers.shop.util import convert_raw_cart_data_to_products
from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.models.shop.inventory_models import Product
from sqlalchemy.exc import IntegrityError


blueprint = Blueprint(
    "checkout",
    __name__,
)


@blueprint.route("/success")
def successful_checkout():
    try:
        session_id = request.args["session_id"]
        transaction_id = session["transaction_id"]
    except KeyError:
        current_app.logger.info("no transaction session")
        return render_template("success.html", products=[])

    if session_id != transaction_id:
        current_app.logger.error("broken transaction session")
        abort(400)

    products = convert_raw_cart_data_to_products(session["transaction_cart"])
    del session["transaction_id"]
    # Remove products from the inventory (i.e., lower stock by quantity purchased)
    try:
        for product_id, purchased_amount in session["transaction_cart"].items():
            db_product = Product.query.get(product_id)
            db_product.stock = db_product.stock - purchased_amount
            db.session.add(db_product)
            db.session.commit()
    except IntegrityError:
        current_app.logger.critical(
            "A severe error was encountered while trying to adjust inventory in response to a transaction."
        )
        db.session.rollback()
    del session["transaction_cart"]
    return render_template(
        "success.html",
        products=[(product, product["images"][0]) for product in products],
    )


@blueprint.route("/cancel")
def cancel_checkout():
    # we could restore the abandoned cart or something else here
    return render_template("cancel.html")
