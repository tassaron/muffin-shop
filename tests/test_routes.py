import os
import tempfile
import pytest
from rainbow_shop.__init__ import create_app
from rainbow_shop.app import init_app, plugins
from rainbow_shop.models import User

db, bcrypt, login_manager = plugins


@pytest.fixture
def client():
    app = create_app()
    app = init_app(app)
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["TESTING"] = True
    client = app.test_client()
    with app.app_context():
        yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_index(client):
    resp = client.get("/")  # , content_type="html/text")
    assert resp.status_code == 200


def test_adminlogin(client):
    db.create_all()
    db.session.add(User(email="admin@example.com", password="password", is_admin=True))
    db.session.commit()
    resp = client.post(
        "/account/login",
        data={"email": "", "password": "password"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
