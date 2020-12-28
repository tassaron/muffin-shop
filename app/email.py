from flask import current_app, url_for
from .tasks import send_email


def send_password_reset_email(user):
    token = user.create_password_reset_token()
    email_config = {
        "ENV": current_app.env
    }
    if current_app.env == "production":
        email_config |= {
            "API_URL": current_app.config["EMAIL_API_URL"],
            "API_KEY": current_app.config["EMAIL_API_KEY"],
            "SENDER_NAME": current_app.config['EMAIL_SENDER_NAME'],
            "SENDER_ADDRESS": current_app.config['EMAIL_SENDER_ADDRESS'],
        }
    send_email(
        email_config,
        "Password Reset Request",
        f"To reset your password, visit this link: {url_for('.change_password', token=token, _external=True)}",
        user.email,
    )
