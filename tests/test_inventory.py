import tempfile
import os
from tassaron_flask.helpers.main.app_factory import create_app, init_app
from tassaron_flask.helpers.main.plugins import plugins
from tassaron_flask.models.main.models import User
from tassaron_flask.models.shop.inventory_models import Product
import pytest


@pytest.fixture
def client():
    global app, db, bcrypt, login_manager
    app = create_app()
    db, migrate, bcrypt, login_manager = plugins
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
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
    os.close(db_fd)
    os.unlink(db_path)


def test_inventory_create_product(client):
    resp = client.post(
        f"{app.config['ADMIN_URL']}/inventory/create",
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
        price=1.0,
        description="this is a test",
        image="potato.jpg",
        stock=1,
        category_id=1,
        payment_id="this should get deleted",
    )
    db.session.add(product)
    db.session.commit()
    product = Product.query.get(1)
    assert product.payment_id is not None
    resp = client.post(
        f"{app.config['ADMIN_URL']}/inventory/edit/1",
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
    assert product.payment_id is None
