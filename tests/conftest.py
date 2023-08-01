import os
import tempfile
import pytest
from muffin_shop.helpers.main.app_factory import create_app, init_app
from muffin_shop.helpers.main.plugins import db


@pytest.fixture(scope="function")
def shop_index_client():
    """A client with / as the shop page"""
    os.environ["CONFIG_PATH"] = "config"
    os.environ["MONITOR_ENABLED"] = "0"
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SERVER_NAME"] = "0.0.0.0:5000"
    app.config["TESTING"] = True
    app = init_app(
        app, {"main": {"name": "Home", "module": ".shop", "navigation": [".about"]}}
    )
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def markdown_index_client():
    """
    A client with / as the about page
    """
    os.environ["CONFIG_PATH"] = "config/client/rainey_arcade"
    os.environ["MONITOR_ENABLED"] = "0"
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SERVER_NAME"] = "0.0.0.0:5000"
    app.config["TESTING"] = True
    app = init_app(
        app,
        {
            "main": {
                "name": "Home",
                "module": ".about",
                "navigation": [".shop", ".blog", ".arcade"],
            }
        },
    )
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client
    os.close(db_fd)
    os.unlink(db_path)
