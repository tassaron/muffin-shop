from muffin_shop.helpers.main.app_factory import init_app
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.main.models import User
from muffin_shop.models.shop.inventory_models import Product
from flask import current_app
import pytest


@pytest.fixture
def client(app):
    app = init_app(app)
    client = app.test_client()
    with app.app_context():
        with client:
            db.create_all()
            user = User(email="test@example.com", password="password", is_admin=True)
            db.session.add(user)
            db.session.commit()
            client.post(
                "/account/login",
                data={"email": "test@example.com", "password": "password"},
                follow_redirects=True,
            )
            yield client


def test_inventory_create_product(client):
    resp = client.post(
        f"{current_app.config['ADMIN_URL']}/inventory/create",
        data={
            "name": "Spinach",
            "price": 1.0,
            "description": "this is a test",
            "image": "potato.jpg",
            "stock": 1,
            "category_id": 1,
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200


def test_inventory_edit_product(client):
    product = Product(
        name="Spinach",
        price=100,
        description="this is a test",
        image="potato.jpg",
        stock=1,
        category_id=1,
        payment_uuid="this should get deleted",
    )
    db.session.add(product)
    db.session.commit()
    product = Product.query.get(1)
    assert product.payment_uuid is not None
    resp = client.post(
        f"{current_app.config['ADMIN_URL']}/inventory/edit/1",
        data={
            "name": "Spinach",
            "price": 2.0,
            "description": "this is a test",
            "image": "potato.jpg",
            "stock": 1,
            "category_id": 1,
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    product = Product.query.get(1)
    assert product.payment_uuid is None
