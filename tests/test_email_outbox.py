"""
Ensure that a user cannot receive a second email until they've taken action
on the previous one, or until enough time has passed
"""
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.main.models import User
from muffin_shop.helpers.main.email import *
from huey.api import Result


def test_email_outbox_for_reset_password(markdown_index_client):
    user = User(
        email="test@example.com",
        email_verified=True,
        password="password",
        is_admin=False,
    )
    db.session.add(user)
    db.session.commit()
    # sending email to user should first succeed
    result = send_password_reset_email(user)
    assert type(result) == Result

    # sending email to user should now fail
    try:
        send_password_reset_email(user)
    except OutboxFull:
        pass
    else:
        assert "Didn't raise OutboxFull" == True

    # visiting the reset_password view won't clear the outbox
    markdown_index_client.get(f"/account/reset_password/{result().split('/')[-1]}")
    try:
        send_password_reset_email(user)
    except OutboxFull:
        pass
    else:
        assert "Didn't raise OutboxFull" == True

    # confirming a new password will actually clear the outbox
    markdown_index_client.post(
        f"/account/reset_password/{result().split('/')[-1]}",
        data={"password": "password", "confirm_password": "password"},
    )
    # sending email should now succeed!
    result = send_password_reset_email(user)
    assert type(result) == Result


def test_email_outbox_isolated_per_user(markdown_index_client):
    user1 = User(
        email="1@example.com", email_verified=True, password="password", is_admin=False
    )
    user2 = User(
        email="2@example.com", email_verified=True, password="password", is_admin=False
    )
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
    send_password_reset_email(user1)
    # sending email to user2 should not be affected
    result = send_password_reset_email(user2)
    assert type(result) == Result
