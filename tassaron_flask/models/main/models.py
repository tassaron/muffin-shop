from ...helpers.main.plugins import plugins
from itsdangerous import TimedJSONWebSignatureSerializer
from datetime import datetime
from flask import current_app

# plugins = create_plugins()
db, migrate, bcrypt, login_manager = plugins


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=True)
    email_verified = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(64), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False)

    @classmethod
    def create_password_hash(cls, new_password):
        return bcrypt.generate_password_hash(new_password).decode("utf-8")

    def __init__(self, **kwargs):
        if kwargs["password"] is not None:
            kwargs["password"] = User.create_password_hash(kwargs["password"])
        if "email_verified" not in kwargs:
            kwargs["email_verified"] = False
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self.email)

    def update_password(self, new_password):
        self.password = User.create_password_hash(new_password)

    def update_email(self, new_email):
        self.email = new_email
        self.email_verified = False

    def create_json_web_token(self):
        serializer = TimedJSONWebSignatureSerializer(
            current_app.config["SECRET_KEY"], 1800
        )
        return serializer.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_json_web_token(token):
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
        return self.is_authenticated

    @property
    def is_admin_authenticated(self):
        return self.email and self.password and self.is_admin

    def get_id(self):
        return str(self.id)


class NewEmail(db.Model):
    """
    Email table with user IDs as the primary key, representing currently 'active' emails
    An email will be removed from this table after the recipient takes action or in a few hours
    """
    id = db.Column(
        db.Integer, primary_key=True, nullable=False
    )
    user_id = db.Column(
        db.Integer, unique=True, nullable=False #db.ForeignKey("user.id")
    )
    typ = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

class OldEmail(db.Model):
    """
    Valid integers for Email Types:
     0 = verification
     1 = password reset
    """
    id = db.Column(
        db.Integer, primary_key=True, nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    typ = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    archive_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def from_email(cls, email: NewEmail):
        return cls(user_id=email.user_id, typ=email.typ, creation_time=email.creation_time)


# Shop Module's Profile_Models
# ---------------------------------------------------


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


