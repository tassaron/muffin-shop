import os
import tempfile
import pytest
from rainbow_shop.__init__ import create_app
from rainbow_shop.app import init_app, plugins
from rainbow_shop.models import User

app = create_app()
app = init_app(app)
db, bcrypt, login_manager = plugins


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
    assert resp.status_code == 200


def test_login_success(client):
    db.create_all()
    db.session.add(User(email="test@example.com", password="password", is_admin=False))
    db.session.commit()
    resp = client.post(
        "/account/login",
        data={"email": "test@example.com", "password": "password"},
        follow_redirects=True,
    )
    with app.test_request_context():
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
    with app.test_request_context():
        assert b"Wrong email or password" in resp.data
