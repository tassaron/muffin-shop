"""
Utilities for managing the contact page email buffer which goes in a json file
"""
from flask import current_app
import os
import json
import datetime


contact_buffer_path = os.environ.get("CONTACT_BUFFER_PATH", "db")
queued_email_path = f"{contact_buffer_path}/contact.json"
banned_words_path = f"{contact_buffer_path}/banned.json"
spam_path = f"{contact_buffer_path}/spam.json"


def pop_email_from_buffer(index=-1) -> dict:
    if os.path.exists(queued_email_path):
        with open(queued_email_path, "r") as f:
            emails = json.load(f)
    emails = get_all_emails_from_buffer()
    removed_email = emails.pop(index)
    with open(queued_email_path, "w") as f:
        json.dump(emails, f)
    return removed_email


def push_email_into_buffer(ip, subj, body, contact) -> bool:
    if has_banned_word(body):
        return False

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
    with open(queued_email_path, "w") as f:
        json.dump(emails, f)
    return True


def get_all_emails_from_buffer() -> list:
    emails = []
    if os.path.exists(queued_email_path):
        with open(queued_email_path, "r") as f:
            emails = json.load(f)
    return emails


def add_banned_word(word: str) -> bool:
    if not os.path.exists(banned_words_path):
        with open(banned_words_path, "w") as f:
            f.write("[]")
    with open(banned_words_path, "r") as f:
        all_words = json.load(f)
    if word in all_words:
        return False
    all_words.append(word)
    with open(banned_words_path, "w") as f:
        json.dump(all_words, f)
    return True


def has_banned_word(string) -> bool:
    with open(banned_words_path, "r") as f:
        banned_words = json.load(f)
    for word in banned_words:
        if word in string:
            return True
    return False