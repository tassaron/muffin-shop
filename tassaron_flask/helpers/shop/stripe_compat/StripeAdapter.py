import stripe
from flask import current_app
from tassaron_flask.models.shop.inventory_models import Product
from tassaron_flask.helpers.main.plugins import db
from typing import List


class StripeAdapter:
    """
    Turn our data format into Stripe's line_items API.

    To accomplish this we must locate any existing Products or Prices registered on Stripe,
    or create them if they do not exist already.

    A Stripe Price is an object on Stripe that contains the price of 1 product;
    the Price object itself contains the Product object.
    The `line_items` output is a bundling of Prices, Products, and quantities
    for one specific checkout session.

    Stripe Documentation: https://stripe.com/docs/api/checkout/sessions/create#create_checkout_session-line_items
    """

    def __init__(self, products: List[dict]):
        if not stripe.api_key:
            current_app.logger.info("Failed to initialize StripeAdapter (no API key)")
            return

        # Register/update product/price combos that don't exist on Stripe yet
        for product in products:
            if not product["payment_id"]:
                product["payment_id"] = create_or_update_product_on_stripe(product)

        self.line_items = [
            {
                "price": product["payment_id"],
                "quantity": product["quantity"],
            }
            for product in products
        ]

    def convert(self):
        return self.line_items


def create_or_update_product_on_stripe(my_product):
    """
    Create a Product+Price using Stripe
    https://stripe.com/docs/products-prices/getting-started#import-products-prices
    """

    def create_product():
        """This function is called first.
        Throws an exception if Stripe already has this product in their system"""
        stripe_product = stripe.Product.create(
            id=my_product["id"],
            name=my_product["name"],
            description=my_product["description"],
            images=my_product["images"],
        )
        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=int(my_product["price"] * 100),
            currency="cad",
        )
        return stripe_price

    def update_product():
        """If the payment_id is blank but we fail to create the product
        then it means we need to update the Product, potentially creating a new Price"""
        stripe.Product.modify(
            str(my_product["id"]),
            name=my_product["name"],
            description=my_product["description"],
            images=my_product["images"],
        )
        # Find the existing price; there should be exactly one active price
        existing_prices = stripe.Price.list(
            product=my_product["id"],
            active=True,
        )
        assert len(existing_prices.data) == 1
        existing_price = existing_prices.data[0]
        # Check whether price has changed, in which case existing_price needs to be replaced
        if existing_price.unit_amount != int(my_product["price"] * 100):
            new_price = stripe.Price.create(
                product=my_product["id"],
                unit_amount=int(my_product["price"] * 100),
                currency="cad",
            )
            stripe.Price.modify(existing_price.id, active=False)
            return new_price
        return existing_price

    try:
        stripe_price = create_product()
    except stripe.error.StripeError as e:
        if e.code == "resource_already_exists":
            stripe_price = update_product()
        else:
            raise e

    # Put new payment_id in the database for next time
    db_product = Product.query.get(my_product["id"])
    db_product.payment_id = stripe_price.id
    db.session.add(db_product)
    db.session.commit()
    return stripe_price.id
