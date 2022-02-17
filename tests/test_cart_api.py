from tassaron_flask.helpers.main.app_factory import create_app, init_app
from tassaron_flask.helpers.main.plugins import db
from tassaron_flask.models.shop.inventory_models import Product, ProductCategory
import tempfile
import os
from flask import json, session
import pytest


@pytest.fixture
def client():
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["SERVER_NAME"] = "0.0.0.0:5000"
    app = init_app(app)
    with app.app_context():
        db.create_all()
        db.session.add(
            ProductCategory(
                name="Food",
                image="potato.jpg",
            )
        )
        db.session.add(
            Product(
                name="Potato",
                price=1.0,
                description="Tuber from the ground",
                image="potato.jpg",
                stock=1,
                category_id=1,
            )
        )
        db.session.commit()
        client = app.test_client()
        yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_add_to_cart_api_success(client):
    resp = client.post(
        "/cart/add",
        data=json.dumps({"id": 1, "quantity": 1}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.get_data(as_text=True))
    assert data["success"] == True


def test_add_to_cart_api_nonexistent(client):
    resp = client.post(
        "/cart/add",
        data=json.dumps({"id": 2, "quantity": 1}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.get_data(as_text=True))
    assert data["success"] == False


def test_add_to_cart_api_failed_outofstock(client):
    db.session.add(
        Product(
            name="Potato",
            price=1.0,
            description="Tuber from the ground",
            image="potato.jpg",
            stock=0,
            category_id=1,
        )
    )
    resp = client.post(
        "/cart/add",
        data=json.dumps({"id": 2, "quantity": 1}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.get_data(as_text=True))
    assert data["success"] == False


def test_add_to_cart_api_baddata(client):
    resp = client.post(
        "/cart/add",
        data=json.dumps({"id": "a", "quantity": 1}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.get_data(as_text=True))
    assert data["success"] == False
    resp = client.post(
        "/cart/add",
        data=json.dumps({"wrong": 1}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.get_data(as_text=True))
    assert data["success"] == False


def test_remove_from_cart_api_success(client):
    with client:
        test_add_to_cart_api_success(client)
        resp = client.post(
            "/cart/del",
            data=json.dumps({"id": 1}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert 1 not in session["cart"]


def test_remove_from_cart_api_fail(client):
    with client:
        test_add_to_cart_api_success(client)
        resp = client.post(
            "/cart/del",
            data=json.dumps({"id": 2}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert 1 in session["cart"]


def test_remove_from_cart_api_baddata(client):
    resp = client.post(
        "/cart/del",
        data=json.dumps({"id": "a"}),
        content_type="application/json",
    )
    assert resp.status_code == 400
