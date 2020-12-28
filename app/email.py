from flask import current_app, url_for
from .tasks import huey_send_email
from .main.models import User
from .main.plugins import db


def send_email(subj, body, send_to, force=False):
    """
    If `force` is False, do not allow sending emails to unverified addresses
    Injects the current API credentials from current_app.config
    Call this function from within app context to queue an email with Huey
    Returns a Huey Results object only if successfully queued
    During tests, it will return the token it generates instead of a true result
    """
    if not force:
        user = User.query.filter_by(email=send_to).first()
        if user.email_verified == False:
            current_app.logger.warning("Could not send email to %s because the address isn't verified", send_to)
            return
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
    return huey_send_email(
        email_config,
        subj,
        body,
        send_to,
    )


def send_email_verification_email(user):
    """Generate JWT for new user and email it to them so they can verify their address"""
    token = user.create_json_web_token()
    return send_email(
        f"Verify Your Email on {current_app.config['SITE_NAME']}",
        f"To verify your email address, visit this link: {url_for('account.verify_email', token=token, _external=True)}",
        user.email,
        force=True,
    )


def send_password_reset_email(user):
    """Generate JWT for user and send an email linking them to the change_password view"""
    token = user.create_json_web_token()
    return send_email(
        "Password Reset Request",
        f"To reset your password, visit this link: {url_for('account.change_password', token=token, _external=True)}",
        user.email,
    )
