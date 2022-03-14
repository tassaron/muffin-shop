import os

payment_processor = os.environ.get("PAYMENT_PROCESSOR", "stripe")

if payment_processor == "stripe":
    import stripe

    stripe.api_key = os.environ.get("STRIPE_API_KEY", "")
