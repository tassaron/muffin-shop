from tassaron_flask_template.main.plugins import db


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)


class Product(db.Model):
    """Product which will be available for purchase in the store if stock > 0"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(30), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id"), nullable=False
    )
