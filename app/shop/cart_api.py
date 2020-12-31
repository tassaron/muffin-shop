"""
POST to these Cart endpoints in order to manipulate the Cart Session Cookie
Each endpoint returns a response of success or not, to update the client-side record
"""
from flask import Blueprint, request, abort
from tassaron_flask_template.main.plugins import db
from .inventory_models import Product


blueprint = Blueprint(
    "cart",
    __name__
)


@blueprint.route("/add", methods=["POST"])
def add_product_to_cart():      
    try:
        item = request.get_json()
        id = int(item["id"])
        product = Product.query.get(id)
        if product is None or product.stock < 1:
            return {"success": False}
        else:
            return {"success": True}
    except:
        return {"success": False}, 400