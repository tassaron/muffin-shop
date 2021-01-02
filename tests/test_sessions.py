import os
import tempfile
import pytest
import json
from tassaron_flask_template.main import create_app, init_app
from tassaron_flask_template.main.plugins import db
from tassaron_flask_template.main.models import User
from tassaron_flask_template.shop.inventory_models import *
from flask import session


@pytest.fixture
def client():
    global app, db, bcrypt, login_manager
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    app = init_app(app)
    client = app.test_client()
    with app.app_context():
        db.create_all()
        db.session.add(
            User(email="test@example.com", password="password", is_admin=False)
        )
        db.session.add(
            ProductCategory(
                name="Food",
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
    yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_session_is_restored(client):
    with client:
        client.get("/")
        assert session["cart"] == {}
        client.post(
            "/cart/add",
            data=json.dumps({"id": 1, "quantity": 1}),
            content_type='application/json',
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