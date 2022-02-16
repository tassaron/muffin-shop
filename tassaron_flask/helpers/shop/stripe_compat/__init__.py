class StripeAdapter:
    """
    Turn our data format into Stripe's line_items API.
    Stripe Documentation: https://stripe.com/docs/api/checkout/sessions/create#create_checkout_session-line_items
    """

    def __init__(self, products):
        self.line_items = (
            [
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
            ]
            for product in products
        )

    def convert(self):
        return self.line_items


class StripeCheckoutSession:
    """
    Start and end a Stripe Checkout session.
    Stripe Documentation: https://stripe.com/docs/api/checkout/sessions
    """

    def __init__(self):
        pass
