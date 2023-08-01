from muffin_shop.helpers.main.app_factory import init_app
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.main.models import User
from muffin_shop.helpers.main.email import *
from huey.api import Result


def test_email_verification(markdown_index_client):
    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    markdown_index_client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
    )
    # email_verified is false after initial registration
    assert user.email_verified == False

    # sending email to user should fail
    try:
        result = send_password_reset_email(user)
    except Unverified:
        pass
    else:
        assert "Didn't raise Unverified" == True

    # verify email
    result = send_email_verification_email(user)
    markdown_index_client.get(f"/account/verify_email/{result().split('/')[-1]}")
    assert user.email_verified == True

    # sending email should now succeed!
    # client.get("/account/logout", follow_redirects=True)
    result = send_password_reset_email(user)
    assert type(result) == Result

    # updating the email will unverify it again
    user.update_email("")
    assert user.email_verified == False
