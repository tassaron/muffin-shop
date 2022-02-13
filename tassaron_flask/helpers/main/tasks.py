"""
Huey tasks that we can launch asynchronously from web requests
"""
import os
import requests
from huey import SqliteHuey


huey = SqliteHuey(
    filename=os.environ.get("HUEY_DB", "db/huey.db"), immediate_use_memory=False
)


@huey.task()
def huey_send_email(email_config, subject, body, send_to):
    """
    email_config = {
        "ENV": current_app.env,
        "API_URL": current_app.config["EMAIL_API_URL"],
        "API_KEY": current_app.config["EMAIL_API_KEY"],
        "SENDER_NAME": current_app.config['EMAIL_SENDER_NAME'],
        "SENDER_ADDRESS": current_app.config['EMAIL_SENDER_ADDRESS'],
    }
    """
    if email_config["ENV"] != "production":
        print(body)
        return body.split("/")[-1]

    return requests.post(
        email_config["API_URL"],
        auth=("api", email_config["API_KEY"]),
        data={
            "from": f"{email_config['SENDER_NAME']} <{email_config['SENDER_ADDRESS']}>",
            "to": [str(send_to)],
            "subject": str(subject),
            "text": str(body),
        },
    ).json()
