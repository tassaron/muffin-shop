import os
import tempfile
import pytest
from muffin_shop.helpers.main.app_factory import create_app, init_app
from muffin_shop.helpers.main.plugins import db, bcrypt, login_manager
from test_routes import client as normal_client


@pytest.fixture
def client():
    global app, db, bcrypt, login_manager
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    app = init_app(
        app,
        modules={"main": {"name": "Home", "module": ".about", "navigation": [".shop"]}},
    )
    client = app.test_client()
    with app.app_context():
        with client:
            db.create_all()
            yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_normal_about_page(normal_client):
    resp = normal_client.get("/about")
    assert resp.status_code == 200
    resp = normal_client.get("/about/")
    assert resp.status_code == 404
    resp = normal_client.get("/shop")
    assert resp.status_code == 404


# Future feature!
# def test_index_about_page(client):
#    resp = client.get("/about")
#    assert resp.status_code == 404
#    resp = client.get("/shop")
#    assert resp.status_code == 200
