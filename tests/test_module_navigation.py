import pytest
from muffin_shop.helpers.main.app_factory import init_app
from muffin_shop.helpers.main.plugins import db, bcrypt, login_manager
from test_routes import client as normal_client


@pytest.fixture
def client(app):
    app = init_app(
        app,
        modules={"main": {"name": "Home", "module": ".about", "navigation": [".shop"]}},
    )
    client = app.test_client()
    with app.app_context():
        with client:
            db.create_all()
            yield client


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
