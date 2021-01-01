import os
import tempfile
import pytest
import flask_login
from flask import url_for
from tassaron_flask_template.main import create_app, init_app
from tassaron_flask_template.main.plugins import db, bcrypt, login_manager
from tassaron_flask_template.main.models import User, ShippingAddress


@pytest.fixture
def client():
    global app, db, bcrypt, login_manager
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    app.config["CLIENT_SESSIONS"] = True
    app = init_app(app)
    client = app.test_client()
    with app.app_context():
        with client:
            db.create_all()
            user = User(email="test@example.com", password="password", is_admin=False)
            db.session.add(user)
            db.session.commit()
            client.post(
                "/account/login",
                data={"email": "test@example.com", "password": "password"},
                follow_redirects=True,
            )
            yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_reset_password_button_exists_on_profile(client):
    resp = client.get("/account/profile")
    assert bytes(
        f'<a href=\"{url_for("account.reset_password")}\" class="btn btn-outline-primary">Reset Password</a>',
        "utf-8"
    ) in resp.data


def test_blank_shipping_address(client):
    resp = client.get("/account/profile")
    for text in ShippingAddress.names().values():
        assert bytes(text, "utf-8") in resp.data


def test_existent_shipping_address(client):
    db.session.add(
        ShippingAddress(
            user_id=1,
            first_name="Bri",
            last_name="Rainey",
            phone="5550005555",
            address1="123 Fake St",
            address2="Apt 9",
            postal_code="A0B1C2",
            city="Anytown",
            province="ON",
        )
    )
    db.session.commit()
    resp = client.get("/account/profile")
    assert bytes("123 Fake St", "utf-8") in resp.data