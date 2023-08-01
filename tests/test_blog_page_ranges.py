import os
import tempfile
import pytest
from muffin_shop.helpers.main.app_factory import create_app, init_app
from muffin_shop.helpers.main.plugins import db

def link_to_page(page_num):
    return bytes(
        f'<a href="/blog/{page_num}">',
        "utf-8",
    )


@pytest.fixture
def app():
    """Shadows the usual app fixture to add CONFIG_PATH=config"""
    os.environ["CONFIG_PATH"] = "config/client/rainey_arcade"
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Shadows the usual client fixture to add custom modules"""
    app = init_app(
        app,
        #modules={
        #    "main": {
        #        "name": "Home",
        #        "module": ".about",
        #        "navigation": [".blog"]
        #    }
        #},
    )
    with app.test_client() as test_client:
        with app.app_context():
            db.create_all()
            yield test_client


def test_blog_0_pages_4_posts(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/0_pages_4_posts"
    resp = client.get("/blog")
    assert bytes("older posts", "utf-8") not in resp.data


def test_blog_0_pages_5_posts(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/0_pages_5_posts"
    resp = client.get("/blog")
    assert bytes("older posts", "utf-8") not in resp.data


def test_blog_1_page(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/1_page"
    resp = client.get("/blog")
    assert bytes("older posts", "utf-8") in resp.data
    assert link_to_page(1) in resp.data
    assert link_to_page(2) not in resp.data


def test_blog_page_selected(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/1_page"
    resp = client.get("/blog/1")
    assert bytes("older posts", "utf-8") in resp.data
    assert link_to_page(1) not in resp.data


def test_blog_2_pages(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/2_pages"
    resp = client.get("/blog")
    assert link_to_page(2) in resp.data


def test_blog_11_pages_selected_11(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/11_pages"
    resp = client.get("/blog/11")
    assert link_to_page(12) not in resp.data
    assert link_to_page(11) not in resp.data
    assert link_to_page(10) in resp.data
    assert link_to_page(1) in resp.data


def test_blog_12_pages(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/12_pages"
    resp = client.get("/blog")
    assert link_to_page(12) in resp.data
    assert link_to_page(1) in resp.data


def test_blog_13_pages(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/13_pages"
    resp = client.get("/blog")
    assert link_to_page(13) in resp.data
    assert link_to_page(2) in resp.data
    assert link_to_page(1) not in resp.data


def test_blog_14_pages_selected_13(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/14_pages"
    resp = client.get("/blog/13")
    assert link_to_page(15) not in resp.data
    assert link_to_page(14) in resp.data
    assert link_to_page(13) not in resp.data
    assert link_to_page(3) in resp.data
    assert link_to_page(2) not in resp.data


def test_blog_14_pages_selected_threshold_8_9(client):
    os.environ["BLOG_PATH"] = f"{os.path.dirname(os.path.abspath(__file__))}/data/blog/14_pages"
    resp = client.get("/blog/9")
    assert link_to_page(14) in resp.data
    assert link_to_page(2) not in resp.data
    resp = client.get("/blog/8")
    assert link_to_page(14) not in resp.data
    assert link_to_page(2) in resp.data
