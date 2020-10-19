import os
import tempfile
import pytest
from rainbow_shop.run import app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["TESTING"] = True
    client = app.test_client()
    yield client
    os.close(db_fd)
    os.unlink(db_path)


def test_index(client):
    resp = client.get("/", content_type="html/text")
    assert resp.status_code == 200
