from flask import url_for
from typing import List, Tuple
from tassaron_flask.models.shop.inventory_models import Product


def convert_raw_cart_data_to_products(products: dict) -> List[dict]:
    """
    Raw cart data is in the format { product_id: quantity }
    This function converts that into a list of dictionaries
    with full product info from the database
    """
    db_products = [
        Product.query.filter(
            Product.id == product_id, Product.stock >= quantity
        ).first()
        for product_id, quantity in products.items()
    ]

    return [
        {
            "id": db_product.id,
            "payment_id": db_product.payment_id,
            "name": db_product.name,
            "description": db_product.description,
            "images": [
                url_for("static", filename=p, _external=True)
                for p in db_product.image.split(",")
            ],
            "quantity": products.get(int(db_product.id), 0),
            "price": db_product.price,
        }
        for db_product in db_products
    ]


def verify_stock_before_checkout(products: List[dict]) -> Tuple[List[dict], List[int]]:
    changed_quantities = []
    # TODO: check if stock has changed

    return products, changed_quantities