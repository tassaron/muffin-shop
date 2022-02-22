"""
Huey tasks that we can launch asynchronously from web requests
"""
import os
import requests
from huey import SqliteHuey
from sqlite3 import OperationalError


def init_huey():
    huey_db_path = os.environ.get("HUEY_DB", "db/huey.db")
    try:
        huey = SqliteHuey(
            filename=huey_db_path, immediate_use_memory=False
        )
    except OperationalError as e:
        raise FileNotFoundError(f"{e}: {huey_db_path} does not exist. Is the directory writable?") from OperationalError
    return huey


huey = init_huey()


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
