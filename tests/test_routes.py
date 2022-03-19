import os
import tempfile
import pytest
import flask_login
from muffin_shop.helpers.main.app_factory import create_app, init_app
from muffin_shop.helpers.main.plugins import login_manager, db
from muffin_shop.models.main.models import User
from muffin_shop.helpers.main.util import all_base_urls


def nav_selected_bytes(route):
    return bytes(
        f'<a href="{route}" class="nav-link shadow-sm active" aria-current="page">',
        "utf-8",
    )


@pytest.fixture
def client():
    global app
    os.environ["CONFIG_PATH"] = "config/client/the_rainbow_farm"
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    os.environ["MONITOR_ENABLED"] = "0"
    app = init_app(app)
    client = app.test_client()
    with app.app_context():
        with client:
            db.create_all()
            yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_shop_nav_link(client):
    resp = client.get("/products")
    assert nav_selected_bytes("/products") in resp.data
    assert resp.status_code == 200


def test_about_page_nav_link(client):
    resp = client.get("/about")
    assert nav_selected_bytes("/about") in resp.data


def test_404_page(client):
    resp = client.get("/invalid")
    assert resp.status_code == 404


def test_login_success(client):

    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    resp = client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert bytes("Logged in! ✔️", "utf-8") in resp.data
    assert flask_login.current_user == user


def test_login_failure(client):

    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    resp = client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "wordpass"},
        follow_redirects=True,
    )
    assert b"Wrong email or password" in resp.data
    assert flask_login.current_user != user


def test_registration_success(client):

    assert User.query.filter_by(email="test@example.com").first() is None
    resp = client.post(
        "/account/register",
        data={
            "email": "test@example.com",
            "password": "password",
            "confirmp": "password",
        },
        follow_redirects=True,
    )
    assert User.query.filter_by(email="test@example.com").first() is not None


def test_registration_failure(client):

    assert User.query.filter_by(email="test@example.com").first() is None
    resp = client.post(
        "/account/register",
        data={
            "email": "test@example.com",
            "password": "password",
            "confirmp": "",
        },
        follow_redirects=True,
    )
    assert User.query.filter_by(email="test@example.com").first() is None
    resp = client.post(
        "/account/register",
        data={
            "email": "nodomainname",
            "password": "password",
            "confirmp": "password",
        },
        follow_redirects=True,
    )
    assert User.query.filter_by(email="nodomainname").first() is None


def test_anonymous_user(client):

    anon1 = login_manager.anonymous_user()
    anon2 = login_manager.anonymous_user()
    db.session.add(anon1)
    db.session.add(anon2)
    db.session.commit()
    assert len(User.query.filter_by(email=None).all()) == 2


def test_reregistration_failure(client):
    test_registration_success(client)
    resp = client.post(
        "/account/register",
        data={
            "email": "test@example.com",
            "password": "password",
            "confirmp": "password",
        },
        follow_redirects=True,
    )
    assert len(User.query.filter_by(email="test@example.com").all()) == 1


def test_user_privilege(client):

    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    resp = client.get("/account/profile")
    assert resp.status_code == 302
    resp = client.get("/admin/images")
    assert resp.status_code == 404
    client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert flask_login.current_user == user
    resp = client.get("/account/profile")
    assert resp.status_code == 200
    assert nav_selected_bytes("/about") not in resp.data
    resp = client.get("/admin/images")
    assert resp.status_code == 404


def test_all_anonymous_user_routes(client):
    client.get("/")
    endpoints = [
        url for url in all_base_urls() if not url.startswith(app.config["ADMIN_URL"])
    ]
    try:
        endpoints.remove("/view_shipping_address")
        endpoints.remove("/view_cart")
    except ValueError:
        pass
    for endpoint in endpoints:
        resp = client.get(endpoint)
        assert resp.status_code == 200 or resp.status_code == 302


def test_all_logged_in_user_routes(client):

    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    endpoints = [
        url for url in all_base_urls() if not url.startswith(app.config["ADMIN_URL"])
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
        resp = client.get(endpoint)
        assert resp.status_code == 200
    endpoints = [
        url for url in all_base_urls() if url.startswith(app.config["ADMIN_URL"])
    ]
    for endpoint in endpoints:
        resp = client.get(endpoint)
        assert resp.status_code == 404


def test_static(client):
    # Irrelevant when using Nginx in production, but still important
    resp = client.get("/static/img/logo.svg")
    assert resp.status_code == 200
