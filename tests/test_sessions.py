import pytest
import json
from muffin_shop.helpers.main.app_factory import init_app
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.main.models import User
from muffin_shop.models.shop.inventory_models import *
from flask import current_app, session


@pytest.fixture
def client(app):
    app = init_app(app)
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            db.session.add(
                User(email="test@example.com", password="password", is_admin=False)
            )
            db.session.add(
                ProductCategory(
                    name="Food",
                    image="potato.jpg",
                )
            )
            db.session.add(
                Product(
                    name="Potato",
                    price=100,
                    description="Tuber from the ground",
                    image="potato.jpg",
                    stock=1,
                    category_id=1,
                )
            )
            db.session.commit()
            yield test_client


def test_session_is_restored(client):
    client.get("/")
    assert session["cart"] == {}
    client.post(
        "/cart/add",
        data=json.dumps({"id": 1, "quantity": 1}),
        content_type="application/json",
    )
    assert session["cart"] == {1: 1}
    client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    client.get("/account/logout")
    assert session["cart"] == {}
    client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert session["cart"] == {1: 1}


def test_session_doesnt_overwrite(client):
    db.session.add(
        Product(
            name="Potato",
            price=100,
            description="Tuber from the ground",
            image="potato.jpg",
            stock=1,
            category_id=1,
        )
    )
    db.session.commit()
    client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    client.post(
        "/cart/add",
        data=json.dumps({"id": 1, "quantity": 1}),
        content_type="application/json",
    )
    assert session["cart"] == {1: 1}
    client.get("/account/logout")
    client.post(
        "/cart/add",
        data=json.dumps({"id": 2, "quantity": 1}),
        content_type="application/json",
    )
    client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert session["cart"] == {2: 1}
