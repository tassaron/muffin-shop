import pytest
from flask import url_for
from muffin_shop.helpers.main.app_factory import create_app, init_app
from muffin_shop.helpers.main.plugins import db, bcrypt, login_manager
from muffin_shop.models.main.models import User


@pytest.fixture
def client(shop_index_client):
    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    shop_index_client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    yield shop_index_client


def test_reset_password_button_exists_on_profile(client):
    resp = client.get("/account/profile")
    assert (
        bytes(
            f'<a href="{url_for("account.reset_password")}" class="btn btn-outline-primary">Reset Password</a>',
            "utf-8",
        )
        in resp.data
    )
