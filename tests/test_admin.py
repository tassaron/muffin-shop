import pytest
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.main.models import User
from muffin_shop.helpers.main.util import all_base_urls
from flask import current_app


@pytest.fixture
def admin_client(markdown_index_client):
    # db.create_all()
    user = User(email="test@example.com", password="password", is_admin=True)
    db.session.add(user)
    db.session.commit()
    markdown_index_client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    yield markdown_index_client


def test_admin_privilege(admin_client):
    resp = admin_client.get(current_app.config["ADMIN_URL"])
    assert resp.status_code == 200


def test_all_admin_routes(admin_client):
    endpoints = [
        url
        for url in all_base_urls()
        if url.startswith(current_app.config["ADMIN_URL"])
    ]
    endpoints.remove(current_app.config["ADMIN_URL"])
    assert len(endpoints) != 0
    for endpoint in endpoints:
        resp = admin_client.get(endpoint)
        assert resp.status_code == 200
