"""
PaymentAdapter objects are meant to abstract away differences between payment processors
The only payment processor right now is Stripe of course :)
In the future this file could select amongst different payment backends, maybe
"""

from tassaron_flask.helpers.shop.stripe_compat import StripeAdapter as PaymentAdapter
