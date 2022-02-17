from tassaron_flask.helpers.shop.stripe_compat import StripeAdapter
from tassaron_flask.helpers.shop.util import convert_raw_cart_data_to_products
from test_cart_api import client
from flask import session, json, current_app


def test_payment_adapter_stripe(client):
    with client:
        resp = client.post(
            "/cart/add",
            data=json.dumps({"id": 1, "quantity": 1}),
            content_type="application/json",
        )
        data = session["cart"]
    assert StripeAdapter(convert_raw_cart_data_to_products(data)).convert() == [
        {
            "price_data": {
                "currency": "cad",
                "product_data": {
                    "name": "Potato",
                    "description": "Tuber from the ground",
                    "images": ["http://0.0.0.0:5000/static/uploads/images/potato.jpg"],
                },
                "unit_amount": 100,
            },
            "quantity": 1,
            "description": "Tuber from the ground",
        }
    ]
