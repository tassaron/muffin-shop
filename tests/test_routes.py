import os
import tempfile
import pytest
from rainbow_shop.__init__ import create_app
from rainbow_shop.app import init_app, plugins
from rainbow_shop.models import User

app = create_app()
app = init_app(app)
db, bcrypt, login_manager = plugins


def nav_selected_bytes(route):
    return bytes(
        f'<li class="nav-item active">\n                        <a class="nav-link" href="{route}">',
        "utf-8",
    )


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    client = app.test_client()
    with app.app_context():
        yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_index(client):
    resp = client.get("/")
    assert nav_selected_bytes("/") in resp.data
    assert resp.status_code == 200


def test_about_page(client):
    resp = client.get("/about")
    assert nav_selected_bytes("/about") in resp.data


def test_404_page(client):
    resp = client.get("/invalid")
    assert nav_selected_bytes("/") in resp.data
    assert resp.status_code == 404


def test_login_success(client):
    db.create_all()
    db.session.add(User(email="test@example.com", password="password", is_admin=False))
    db.session.commit()
    resp = client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    assert bytes("Logged in! ✔️", "utf-8") in resp.data


def test_login_failure(client):
    db.create_all()
    db.session.add(User(email="test@example.com", password="password", is_admin=False))
    db.session.commit()
    resp = client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "wordpass"},
        follow_redirects=True,
    )
    assert b"Wrong email or password" in resp.data


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
