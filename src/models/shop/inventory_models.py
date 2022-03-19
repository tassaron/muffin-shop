from muffin_shop.helpers.main.plugins import db
from muffin_shop.helpers.main.images import Images
from werkzeug.utils import secure_filename


def create_category_sorting_order_func():
    category_sorting_order_i = 0

    def category_sorting_order():
        nonlocal category_sorting_order_i
        category_sorting_order_i += 10
        return category_sorting_order_i

    return category_sorting_order


category_sorting_order = create_category_sorting_order_func()


class ModelWithImage:
    @property
    def image(self):
        return Images.path(self._image).split("/", 1)[1]

    @image.setter
    def image(self, new_image):
        self._image = secure_filename(new_image)


class ProductCategory(ModelWithImage, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    _image = db.Column(db.String(36), nullable=False)
    sorting_order = db.Column(
        db.Integer, nullable=False, default=category_sorting_order
    )


class Product(ModelWithImage, db.Model):
    """Product which will be available for purchase in the store if stock > 0"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    _image = db.Column(db.String(36), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id"), nullable=False
    )
    payment_uuid = db.Column(db.String(60), nullable=True)
