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

    def __init__(self, products):
        self.line_items = [
            {
                "price_data": {
                    "currency": "cad",
                    "product_data": {
                        "name": product["name"],
                        "description": product["description"],
                        "images": product["images"],
                    },
                    "unit_amount": int(product["price"] * 100),
                },
                "quantity": product["quantity"],
                "description": product["description"],
            }
            for product in products
        ]

    def convert(self):
        return self.line_items
