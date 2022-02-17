from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.models.shop.inventory_models import Product
from tassaron_flask.helpers.shop.stripe_compat import StripeAdapter
from tassaron_flask.helpers.shop.util import convert_raw_cart_data_to_products
from test_cart_api import client
from flask import session, json, current_app


def test_payment_adapter_stripe_payment_id(client):
    with client:
        resp = client.post(
            "/cart/add",
            data=json.dumps({"id": 1, "quantity": 1}),
            content_type="application/json",
        )
        data = session["cart"]
    first_line_items = StripeAdapter(convert_raw_cart_data_to_products(data)).convert()
    assert first_line_items[0]["quantity"] == 1
    second_line_items = StripeAdapter(convert_raw_cart_data_to_products(data)).convert()
    assert first_line_items[0] == second_line_items[0]
    first_payment_id = first_line_items[0]["price"]

    # change the product without changing price,
    # which should result in the same payment_id
    product = Product.query.get(1)
    assert product.payment_id is not None
    product.payment_id = None
    db.session.add(product)
    db.session.commit()
    updated_line_items = StripeAdapter(
        convert_raw_cart_data_to_products(data)
    ).convert()
    assert updated_line_items[0]["price"] == first_payment_id
    product = Product.query.get(1)
    assert product.payment_id is not None

    # change the product and change the price
    # which should result in a NEW payment_id
    product = Product.query.get(1)
    product.price = 2.0
    product.payment_id = None
    db.session.add(product)
    db.session.commit()
    updated_line_items = StripeAdapter(
        convert_raw_cart_data_to_products(data)
    ).convert()
    assert updated_line_items[0]["price"] != first_payment_id
