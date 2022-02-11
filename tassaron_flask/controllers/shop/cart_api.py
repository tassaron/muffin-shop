"""
POST to these Cart endpoints in order to manipulate the Cart Session Cookie
Each endpoint returns a response of success or not, to update the client-side record
"""
from flask import Blueprint, request, session, current_app
from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.models.shop.inventory_models import Product


blueprint = Blueprint(
    "cart",
    __name__
)


@blueprint.route("/add", methods=["POST"])
def add_product_to_cart():      
    try:
        item = request.get_json()
        id = int(item["id"])
        quantity = int(item["quantity"])
        product = Product.query.get(id)
        if (product is None or
            quantity < 1 or
            product.stock < quantity or
            session["cart"].get(id, 0) == product.stock
            ):
            return {"success": False}
        else:
            if id not in session["cart"]:
                change = quantity
                session["cart"][id] = quantity
            else:
                new_value = min(product.stock, session["cart"][id] + quantity)
                change = new_value - session["cart"][id]
                session["cart"][id] = new_value
            current_app.logger.debug(session["cart"])
            return {
                "success": True,
                "count": len(session["cart"]),
                "change": change
            }
    except Exception:
        if current_app.env == "production":
            return {"success": False}, 400
        raise