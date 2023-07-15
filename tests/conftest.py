import os
import tempfile
import pytest
from muffin_shop.helpers.main.app_factory import create_app, init_app


@pytest.fixture
def app():
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SERVER_NAME"] = "0.0.0.0:5000"
    app.config["TESTING"] = True
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    app = init_app(app)
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client
