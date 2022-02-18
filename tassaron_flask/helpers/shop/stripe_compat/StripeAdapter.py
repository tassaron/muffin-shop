import stripe
from flask import current_app
from tassaron_flask.models.shop.inventory_models import Product
from tassaron_flask.helpers.main.plugins import db
from typing import List
import time


class StripeAdapter:
    """
    Should be an abstraction for the Stripe API, although it's currently a pretty leaky abstraction :)
    """

    def __init__(self, products: List[dict]):
        if not stripe.api_key:
            current_app.logger.critical(
                "Failed to initialize StripeAdapter (no API key)"
            )
            return

        # Register/update product/price combos that don't exist on Stripe yet
        for product in products:
            if not product["payment_id"]:
                product["payment_id"] = create_or_update_product_on_stripe(product)

        # Convert our data format to Stripe's line_items format
        self.products = convert_to_line_items(products)

    def start_session(
        self, success_url: str, cancel_url: str, mode: str
    ) -> stripe.checkout.Session:
        """
        Start a Stripe Checkout session.
        Documentation: https://stripe.com/docs/api/checkout/sessions
        """
        self.session = stripe.checkout.Session.create(
            success_url="%s?session_id={CHECKOUT_SESSION_ID}" % success_url,
            cancel_url="%s?session_id={CHECKOUT_SESSION_ID}" % cancel_url,
            line_items=self.products,
            mode=mode,
            expires_at=int(time.time() + 3600),
            payment_method_types=["card"],
        )
        return self.session


def create_or_update_product_on_stripe(my_product) -> str:
    """
    Create a Product+Price using Stripe
    https://stripe.com/docs/products-prices/getting-started#import-products-prices
    """

    def create_product() -> stripe.Price:
        """
        This function is called first.
        Throws an exception if Stripe already has this product in their system
        """
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

    def update_product() -> stripe.Price:
        """
        If the payment_id is blank but we fail to create the product
        then it means we need to update the Product, potentially creating a new Price
        """
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


def convert_to_line_items(my_products: List[dict]) -> List[dict]:
    """
    Turn our data format into Stripe's line_items API.

    To accomplish this we must locate any existing Products or Prices registered on Stripe,
    or create them if they do not exist already.

    A Stripe Price is an object on Stripe that contains the price of 1 product;
    the Price object itself contains the Product object.
    The `line_items` output is a bundling of Prices, Products, and quantities
    for one specific checkout session.

    Documentation: https://stripe.com/docs/api/checkout/sessions/create#create_checkout_session-line_items
    """
    return [
        {
            "price": product["payment_id"],
            "quantity": product["quantity"],
        }
        for product in my_products
    ]
