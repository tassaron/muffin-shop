"""
PaymentAdapter converts our internal system's data into the payment processor's data format
PaymentSession starts and ends the checkout flow wiht a payment processor
The payment processor is Stripe of course :)
In the future this file could select amongst different payment backends, maybe
"""

from tassaron_flask.helpers.shop.stripe_compat import (
    StripeAdapter as PaymentAdapter,
    StripeCheckoutSession as PaymentSession,
)
