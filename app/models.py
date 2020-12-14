from .plugins import plugins
from itsdangerous import TimedJSONWebSignatureSerializer
import os
from flask import current_app

# plugins = create_plugins()
db, migrate, bcrypt, login_manager = plugins


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=True)
    password = db.Column(db.String(64), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, **kwargs):
        if kwargs["password"] is not None:
            self.update_password(kwargs["password"])
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.email)

    def update_password(self, new_password):
        self.password = bcrypt.generate_password_hash(new_password).decode("utf-8")

    def create_password_reset_token(self):
        serializer = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"], 1800)
        return serializer.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_password_reset_token(token):
        serializer = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"])
        try:
            user_id = serializer.loads(token)["user_id"]
        except KeyError:
            return None
        return User.query.get(user_id)

    def check_password_hash(self, alleged_password):
        return bcrypt.check_password_hash(self.password, alleged_password)

    @property
    def is_anonymous(self):
        return False if self.email and self.password else True

    @property
    def is_authenticated(self):
        return False if self.is_anonymous else True

    @property
    def is_active(self):
        return False if self.is_anonymous else True

    @property
    def is_admin_authenticated(self):
        return self.email and self.password and self.is_admin

    def get_id(self):
        return str(self.id)


# Shop Module
#---------------------------------------------------

class ShippingAddress(db.Model):
    user_id = db.Column(
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
