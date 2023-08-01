import flask_login
from flask import current_app
from muffin_shop.helpers.main.plugins import login_manager, db
from muffin_shop.models.main.models import User
from muffin_shop.helpers.main.util import all_base_urls


def nav_selected_bytes(route):
    return bytes(
        f'<a href="{route}" class="nav-link shadow-sm active" aria-current="page">',
        "utf-8",
    )


def test_shop_nav_link(markdown_index_client):
    resp = markdown_index_client.get("/products")
    assert resp.status_code == 200
    assert nav_selected_bytes("/products") in resp.data


def test_about_page_nav_link(shop_index_client):
    resp = shop_index_client.get("/about")
    assert resp.status_code == 200
    assert nav_selected_bytes("/about") in resp.data


def test_404_page(markdown_index_client):
    resp = markdown_index_client.get("/invalid")
    assert resp.status_code == 404


def test_login_success(markdown_index_client):
    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    resp = markdown_index_client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert bytes("Logged in! ✔️", "utf-8") in resp.data
    assert flask_login.current_user == user


def test_login_failure(markdown_index_client):
    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    resp = markdown_index_client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "wordpass"},
        follow_redirects=True,
    )
    assert b"Wrong email or password" in resp.data
    assert flask_login.current_user != user


def test_registration_success(markdown_index_client):
    assert User.query.filter_by(email="test@example.com").first() is None
    resp = markdown_index_client.post(
        "/account/register",
        data={
            "email": "test@example.com",
            "password": "password",
            "confirmp": "password",
        },
        follow_redirects=True,
    )
    assert User.query.filter_by(email="test@example.com").first() is not None


def test_registration_failure(markdown_index_client):
    assert User.query.filter_by(email="test@example.com").first() is None
    resp = markdown_index_client.post(
        "/account/register",
        data={
            "email": "test@example.com",
            "password": "password",
            "confirmp": "",
        },
        follow_redirects=True,
    )
    assert User.query.filter_by(email="test@example.com").first() is None
    resp = markdown_index_client.post(
        "/account/register",
        data={
            "email": "nodomainname",
            "password": "password",
            "confirmp": "password",
        },
        follow_redirects=True,
    )
    assert User.query.filter_by(email="nodomainname").first() is None


def test_anonymous_user(markdown_index_client):
    anon1 = login_manager.anonymous_user()
    anon2 = login_manager.anonymous_user()
    db.session.add(anon1)
    db.session.add(anon2)
    db.session.commit()
    assert len(User.query.filter_by(email=None).all()) == 2


def test_reregistration_failure(markdown_index_client):
    test_registration_success(markdown_index_client)
    resp = markdown_index_client.post(
        "/account/register",
        data={
            "email": "test@example.com",
            "password": "password",
            "confirmp": "password",
        },
        follow_redirects=True,
    )
    assert len(User.query.filter_by(email="test@example.com").all()) == 1


def test_user_privilege(markdown_index_client):
    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    resp = markdown_index_client.get("/account/profile")
    assert resp.status_code == 302
    resp = markdown_index_client.get("/admin/images")
    assert resp.status_code == 404
    markdown_index_client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert flask_login.current_user == user
    resp = markdown_index_client.get("/account/profile")
    assert resp.status_code == 200
    assert nav_selected_bytes("/about") not in resp.data
    resp = markdown_index_client.get("/admin/images")
    assert resp.status_code == 404


def test_all_anonymous_user_routes(markdown_index_client):
    markdown_index_client.get("/")
    endpoints = [
        url
        for url in all_base_urls()
        if not url.startswith(current_app.config["ADMIN_URL"])
    ]
    try:
        endpoints.remove("/view_shipping_address")
        endpoints.remove("/view_cart")
    except ValueError:
        pass
    for endpoint in endpoints:
        resp = markdown_index_client.get(endpoint)
        assert resp.status_code == 200 or resp.status_code == 302


def test_all_logged_in_user_routes(markdown_index_client):
    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    markdown_index_client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    endpoints = [
        url
        for url in all_base_urls()
        if not url.startswith(current_app.config["ADMIN_URL"])
    ]
    try:
        endpoints.remove("/view_shipping_address")
        endpoints.remove("/view_cart")
    except ValueError:
        pass
    endpoints.remove("/account/register")
    endpoints.remove("/account/login")
    endpoints.remove("/account/logout")
    endpoints.remove("/account/reset_password")
    endpoints.remove("/account/verify_email")
    for endpoint in endpoints:
        resp = markdown_index_client.get(endpoint)
        assert resp.status_code == 200
    endpoints = [
        url
        for url in all_base_urls()
        if url.startswith(current_app.config["ADMIN_URL"])
    ]
    for endpoint in endpoints:
        resp = markdown_index_client.get(endpoint)
        assert resp.status_code == 404


def test_static(markdown_index_client):
    # Irrelevant when using Nginx in production, but still important
    resp = markdown_index_client.get("/static/img/logo.svg")
    assert resp.status_code == 200
