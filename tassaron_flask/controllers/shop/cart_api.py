"""
POST to these Cart endpoints in order to manipulate the Cart Session Cookie
Each endpoint returns a response of success or not, to update the client-side record
"""
from flask import Blueprint, request, session, current_app, url_for
from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.helpers.shop.payment import PaymentAdapter, PaymentSession
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
    products = list(filter(lambda p: p["quantity"] > 0, products))
    db_products = [
        Product.query.filter(
            Product.id == product["id"], Product.stock >= product["quantity"]
        ).first()
        for product in products
    ]
    # TODO: check for stock >0 but <quantity, or nonexistent products

    extras = [
        (
            product.description,
            [
                url_for("static", filename=p, _external=True)
                for p in product.image.split(",")
            ],
        )
        for product in db_products
    ]

    for product, extra in zip(products, extras):
        product["description"] = extra[0]
        product["images"] = extra[1]

    products = PaymentAdapter(products).convert()
    print(list(products))
    return {"success": True}
