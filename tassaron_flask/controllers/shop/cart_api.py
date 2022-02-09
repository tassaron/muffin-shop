"""
POST to these Cart endpoints in order to manipulate the Cart Session Cookie
Each endpoint returns a response of success or not, to update the client-side record
"""
from flask import Blueprint, request, session
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
        if product is None or quantity < 1 or product.stock < quantity:
            return {"success": False}
        else:
            if id not in session["cart"]:
                session["cart"][id] = quantity
            else:
                session["cart"][id] += quantity
            print(session["cart"])
            return {
                "success": True,
                "count": len(session["cart"]),
            }
    except:
        return {"success": False}, 400