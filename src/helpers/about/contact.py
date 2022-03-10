"""
Utilities for managing the contact page email buffer which goes in a json file
"""
from flask import current_app
import os
import json
import datetime


contact_data_path = os.environ.get("CONTACT_BUFFER_PATH", "db/contact.json")


def pop_email_from_buffer(index=-1) -> dict:
    if os.path.exists(contact_data_path):
        with open(contact_data_path, "r") as f:
            emails = json.load(f)
    emails = get_all_emails_from_buffer()
    removed_email = emails.pop(index)
    with open(contact_data_path, "w") as f:
        json.dump(emails, f)
    return removed_email


def push_email_into_buffer(ip, subj, body, contact) -> bool:
    emails = get_all_emails_from_buffer()
    if len(list(filter(lambda email: email["ip"] == ip and datetime.datetime.strptime(email["time"], "%Y-%m-%d %H:%M:%S.%f") > datetime.datetime.utcnow(), emails))):
        # this ip is already in the buffer
        return False

    emails.insert(
        0, {
        "time": str(datetime.datetime.utcnow() + datetime.timedelta(hours=12)),
        "ip": ip,
        "subj": subj,
        "body": body,
        "contact": contact,
    })
    with open(contact_data_path, "w") as f:
        json.dump(emails, f)
    return True


def get_all_emails_from_buffer() -> list:
    emails = []
    if os.path.exists(contact_data_path):
        with open(contact_data_path, "r") as f:
            emails = json.load(f)
    return emails