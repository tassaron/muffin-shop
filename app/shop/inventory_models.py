from tassaron_flask_template.main.plugins import db
from tassaron_flask_template.main.images import Images


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)


class Product(db.Model):
    """Product which will be available for purchase in the store if stock > 0"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    _image = db.Column(db.String(36), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id"), nullable=False
    )

    @property
    def image(self):
        return Images.path(self._image).split("/", 2)[2]

    @image.setter
    def image(self, new_image):
        self._image = new_image