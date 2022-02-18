from tassaron_flask.blueprint import Blueprint
from flask import session, request, current_app, render_template, abort
from tassaron_flask.helpers.shop.util import convert_raw_cart_data_to_products


blueprint = Blueprint(
    "checkout",
    __name__,
)


@blueprint.route("/success")
def successful_checkout():
    try:
        session_id = request.args["session_id"]
    except KeyError:
        current_app.logger.error("no session")
        abort(400)

    products = convert_raw_cart_data_to_products(session["cart"])
    session["cart"] = {}

    return render_template(
        "success.html",
        products=[(product, product["images"][0]) for product in products],
    )


@blueprint.route("/cancel")
def cancel_checkout():
    return render_template("cancel.html")
