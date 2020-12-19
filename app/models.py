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

    @classmethod
    def create_password_hash(cls, new_password):
        return bcrypt.generate_password_hash(new_password).decode("utf-8")

    def __init__(self, **kwargs):
        if kwargs["password"] is not None:
            kwargs["password"] = User.create_password_hash(kwargs["password"])
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.email)

    def update_password(self, new_password):
        self.password = User.create_password_hash(new_password)

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
    """Saved for registered user after placing an order.
    If a user has no ShippingAddress then we use the staticmethod default()"""
    @staticmethod
    def default():
        return {
            "first_name": "",
            "last_name": "",
            "phone": "",
            "address1": "",
            "address2": "",
            "postal_code": "",
            "city": "",
            "province": "",
        }
    @staticmethod
    def names():
        return {
            "first_name": "First Name",
            "last_name": "Last Name",
            "phone": "Phone Number",
            "address1": "Address 1",
            "address2": "Address 2",
            "postal_code": "Postal Code",
            "city": "City",
            "province": "Province",
        }
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


class ShoppingCart(db.Model):
    """Shopping carts in the database should belong to a registered user"""
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True, nullable=False
    )
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
