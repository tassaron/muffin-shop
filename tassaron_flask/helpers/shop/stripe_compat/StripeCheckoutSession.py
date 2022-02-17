import stripe


class StripeCheckoutSession:
    """
    Start a Stripe Checkout session.

    The StripeAdapter must be used first to convert our data format into Stripe's.
    Specifically we need a `line_items` containing the quantities of prices of products.
    The client should get a session ID at the end that can redirect them to Stripe Checkout


    Stripe Documentation: https://stripe.com/docs/api/checkout/sessions
    """

    def __init__(self, success_url, cancel_url, line_items, mode):
        self.session = stripe.checkout.Session.create(
            success_url="%s?session_id={CHECKOUT_SESSION_ID}" % success_url,
            cancel_url=cancel_url,
            line_items=line_items,
            mode=mode,
            payment_method_types=["card"],
        )
