from muffin_shop.helpers.main.app_factory import init_app
from muffin_shop.helpers.main.plugins import db
from muffin_shop.models.shop.inventory_models import *


def test_product_image_safe_path(app):
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
            price=100,
            description="Tuber from the ground",
            image="../../logo.png",
            stock=1,
            category_id=1,
        )
        normal_product = Product(
            name="Potato",
            price=100,
            description="Tuber from the ground",
            image="logo.png",
            stock=1,
            category_id=1,
        )
        assert product_with_path_traversal_image.image == normal_product.image
