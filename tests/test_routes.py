import os
import tempfile
import pytest
import flask_login
from tassaron_flask_template.main import create_app, init_app
from tassaron_flask_template.main.plugins import db, bcrypt, login_manager
from tassaron_flask_template.main.models import User
from tassaron_flask_template.main.routes import all_base_urls


def nav_selected_bytes(route):
    return bytes(
        f'<li class="nav-item active">\n                        <a class="nav-link" href="{route}">',
        "utf-8",
    )


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
        with client:
            yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_index_nav_link(client):
    resp = client.get("/")
    assert nav_selected_bytes("/") in resp.data
    assert resp.status_code == 200


def test_about_page_nav_link(client):
    resp = client.get("/about")
    assert nav_selected_bytes("/about") in resp.data


def test_404_page(client):
    resp = client.get("/invalid")
    assert nav_selected_bytes("/") in resp.data
    assert resp.status_code == 404


def test_login_success(client):
    db.create_all()
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
    db.create_all()
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
    db.create_all()
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
    db.create_all()
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
    db.create_all()
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
    db.create_all()
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
    assert nav_selected_bytes("/") not in resp.data
    resp = client.get("/admin/images")
    assert resp.status_code == 404
    assert nav_selected_bytes("/") in resp.data


def test_all_anonymous_user_routes(client):
    client.get("/")
    endpoints = [url for url in all_base_urls() if not url.startswith(app.config["ADMIN_URL"])]
    try:
        endpoints.remove("/view_shipping_address")
        endpoints.remove("/view_cart")
    except ValueError:
        pass
    for endpoint in endpoints:
        resp = client.get(endpoint)
        assert resp.status_code == 200 or resp.status_code == 302


def test_all_logged_in_user_routes(client):
    db.create_all()
    user = User(email="test@example.com", password="password", is_admin=False)
    db.session.add(user)
    db.session.commit()
    client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    endpoints = [url for url in all_base_urls() if not url.startswith(app.config["ADMIN_URL"])]
    try:
        endpoints.remove("/view_shipping_address")
        endpoints.remove("/view_cart")
    except ValueError:
        pass
    endpoints.remove("/account/register")
    endpoints.remove("/account/login")
    endpoints.remove("/account/logout")
    endpoints.remove("/account/reset_password")
    for endpoint in endpoints:
        resp = client.get(endpoint)
        assert resp.status_code == 200
    endpoints = [url for url in all_base_urls() if url.startswith(app.config["ADMIN_URL"])]
    for endpoint in endpoints:
        resp = client.get(endpoint)
        assert resp.status_code == 404
