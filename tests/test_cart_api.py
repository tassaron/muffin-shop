from muffin_shop.helpers.main.app_factory import init_app
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.shop.inventory_models import Product, ProductCategory
from flask import json, current_app, session
import pytest


@pytest.fixture
def client(shop_index_client):
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
            price=100,
            description="Tuber from the ground",
            image="potato.jpg",
            stock=1,
            category_id=1,
        )
    )
    db.session.commit()
    yield shop_index_client


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
            price=100,
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


def test_csrf_protection_cart_api(client):
    current_app.config["WTF_CSRF_ENABLED"] = True
    with current_app.test_request_context():
        session["arcade_prizes"] = {}
        try:
            resp = client.post(
                "/cart/add",
                data=json.dumps({"id": 1, "quantity": 1}),
                content_type="application/json",
            )
        except KeyError as e:
            # cart should be missing from the session if csrf has failed, as it should
            # assert str(e) == "'cart'"
            pass
        assert "cart" not in session
