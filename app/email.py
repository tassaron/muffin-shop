import requests
from flask import current_app


def send_email(subject, body, send_to):
    if current_app.env != "production":
        return
    return requests.post(
        current_app.config["EMAIL_API_URL"],
        auth=("api", current_app.config["EMAIL_API_KEY"]),
        data={
            "from": f"{current_app.config['EMAIL_SENDER_NAME']} <{current_app.config['EMAIL_SENDER_ADDRESS']}>",
            "to": [str(send_to)],
            "subject": str(subject),
            "text": str(body),
        },
    )


def send_password_reset_email(user):
    if current_app.env != "production":
        return
    token = user.get_reset_token()
    send_email(
        "Password Reset Request",
        f"To reset your password, visit this link: {url_for('.change_password', token=token, _external=True)}",
        user.email,
    )
