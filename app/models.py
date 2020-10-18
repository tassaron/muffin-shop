from .__init__ import db, bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        kwargs["password"] = bcrypt.generate_password_hash(kwargs["password"]).decode(
            "utf-8"
        )
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.email)

    def check_password_hash(self, actual_password, alleged_password):
        return bcrypt.check_password_hash(actual_password, alleged_password)


class ShippingAddress(db.Model):
    id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    address1 = db.Column(db.String(30), nullable=False)
    address2 = db.Column(db.String(30), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    province = db.Column(db.String(2), nullable=False)


class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(30), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_category.id"), nullable=False
    )


class ShoppingCart(db.Model):
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
