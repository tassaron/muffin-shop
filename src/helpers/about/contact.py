"""
Utilities for managing the contact page email buffer which goes in a json file
"""
import os
import json
import datetime
from difflib import SequenceMatcher


contact_buffer_path = os.environ.get("CONTACT_BUFFER_PATH", "db")
queued_email_path = f"{contact_buffer_path}/contact.json"
banned_words_path = f"{contact_buffer_path}/banned.json"
spam_path = f"{contact_buffer_path}/spam.json"
spam_specimen_path = f"{contact_buffer_path}/specimens.json"


def pop_email_from_buffer(index=-1, buffer=None) -> dict:
    buffer = queued_email_path if buffer is None else buffer
    if os.path.exists(buffer):
        with open(buffer, "r") as f:
            emails = json.load(f)
    emails = get_all_emails_from_buffer(buffer)
    removed_email = emails.pop(index)
    with open(buffer, "w") as f:
        json.dump(emails, f)
    return removed_email


def push_email_into_buffer(ip, subj, body, contact) -> bool:
    if has_banned_word(body):
        return False

    def ip_already_in_buffer(emails):
        return bool(
            len(
                list(
                    filter(
                        lambda email: email["ip"] == ip
                        and datetime.datetime.strptime(
                            email["time"], "%Y-%m-%d %H:%M:%S.%f"
                        )
                        > datetime.datetime.utcnow(),
                        emails,
                    )
                )
            )
        )

    def push(buffer):
        buffer.insert(
            0,
            {
                "time": str(datetime.datetime.utcnow() + datetime.timedelta(hours=12)),
                "ip": ip,
                "subj": subj,
                "body": body,
                "contact": contact,
            },
        )

    if seems_like_spam(body):
        spam = get_all_emails_from_buffer(spam_path)
        if ip_already_in_buffer(spam):
            return False
        push(spam)
        with open(spam_path, "w") as f:
            json.dump(spam, f)
        return True

    emails = get_all_emails_from_buffer()
    if ip_already_in_buffer(emails):
        return False
    push(emails)
    with open(queued_email_path, "w") as f:
        json.dump(emails, f)
    return True


def get_all_emails_from_buffer(buffer=None) -> list:
    buffer = queued_email_path if buffer is None else buffer
    emails = []
    if os.path.exists(buffer):
        with open(buffer, "r") as f:
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


def add_spam_specimen(email: dict):
    specimens = get_all_emails_from_buffer(spam_specimen_path)
    specimens.append(email)
    with open(spam_specimen_path, "w") as f:
        json.dump(specimens, f)


def seems_like_spam(string) -> bool:
    specimens = get_all_emails_from_buffer(spam_specimen_path)
    for specimen in specimens:
        diff = SequenceMatcher(None, string, specimen["body"])
        if diff.real_quick_ratio() > 0.6:
            if diff.ratio() > 0.26:
                return True

    return False
