"""
PaymentAdapter objects are meant to abstract away differences between payment processors
The only payment processor right now is Stripe of course :)
In the future this file could select amongst different payment backends, maybe
"""
import os

payment_processor = os.environ.get("PAYMENT_PROCESSOR", "stripe")

if payment_processor == "stripe":
    from muffin_shop.helpers.shop.stripe_compat import StripeAdapter as PaymentAdapter
elif payment_processor == "arcade":
    from muffin_shop.helpers.shop.arcade_compat import ArcadeAdapter as PaymentAdapter
else:
    raise NotImplementedError(f"Unsupported payment processor: {payment_processor}")
