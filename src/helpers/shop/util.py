from flask import url_for
from typing import List, Tuple
from muffin_shop.models.shop.inventory_models import Product


def convert_raw_cart_data_to_products(products: dict) -> List[dict]:
    """
    Raw cart data is in the format { product_id: quantity }
    This function converts that into a list of dictionaries
    with full product info from the database
    """
    db_products = [
        Product.query.get(product_id) for product_id, quantity in products.items()
    ]
    products = {str(key): value for key, value in products.items()}

    return [
        {
            "id": db_product.id,
            "payment_uuid": db_product.payment_uuid,
            "name": db_product.name,
            "description": db_product.description,
            "images": [
                url_for("static", filename=p, _external=True)
                for p in db_product.image.split(",")
            ],
            "quantity": products[str(db_product.id)],
            "price": db_product.price,
            "stock": db_product.stock,
        }
        for db_product in db_products
        if products[str(db_product.id)] > 0
    ]


def verify_stock_before_checkout(products: List[dict]) -> dict:
    """Returns a dictionary of products whose quantities are higher than the inventory allows"""
    return {
        product["id"]: product["stock"]
        for product in filter(lambda prod: prod["stock"] < prod["quantity"], products)
    }


def obfuscate_number(x):
    return int(
        (x / 2) * 9038 if ((x / 7) * 7890 if x % 7 == 0 else x % 2) == 0 else x * 3770
    )


def deobfuscate_number(x):
    return int(
        (x / 9038) * 2
        if ((x / 7890) * 7 if x % 7890 == 0 else x % 9038) == 0
        else x / 3770
    )
