from muffin_shop.helpers.main.app_factory import create_app, init_app
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.shop.inventory_models import *
import tempfile
import os


def test_product_image_safe_path():
    app = create_app()
    db_fd, db_path = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///" + db_path
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["TESTING"] = True
    app = init_app(app)
    with app.app_context():
        db.create_all()
        db.session.add(
            ProductCategory(
                name="Food",
                image="potato.jpg",
            )
        )
        product_with_path_traversal_image = Product(
            name="Potato",
            price=1.0,
            description="Tuber from the ground",
            image="../../logo.png",
            stock=1,
            category_id=1,
        )
        normal_product = Product(
            name="Potato",
            price=1.0,
            description="Tuber from the ground",
            image="logo.png",
            stock=1,
            category_id=1,
        )
        assert product_with_path_traversal_image.image == normal_product.image
    os.close(db_fd)
    os.unlink(db_path)