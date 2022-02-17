class StripeCheckoutSession:
    """
    Start a Stripe Checkout session.

    The StripeAdapter must be used first to convert our data format into Stripe's.
    Specifically we need a `line_items` containing the quantities of prices of products.
    The client should get a session ID at the end that can redirect them to Stripe Checkout


    Stripe Documentation: https://stripe.com/docs/api/checkout/sessions
    """

    def __init__(self):
        pass
