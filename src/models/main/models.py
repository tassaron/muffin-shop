from muffin_shop.helpers.main.plugins import db, bcrypt
import jwt
import time
from datetime import datetime
from flask import current_app


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
        return jwt.encode(
            {"exp": int(time.time() + 1800), "user_id": self.id},
            current_app.config["SECRET_KEY"],
            algorithm=current_app.config.get("JWT_ALGO", "HS256"),
        )

    @staticmethod
    def verify_json_web_token(token):
        try:
            user_id = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=[current_app.config.get("JWT_ALGO", "HS256")],
            )["user_id"]
        except (KeyError, jwt.exceptions.InvalidTokenError):
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

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(
        db.Integer, unique=True, nullable=False  # db.ForeignKey("user.id")
    )
    typ = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class OldEmail(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    typ = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    archive_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def from_email(cls, email: NewEmail):
        """Construct an OldEmail from a NewEmail, thus adding an `archive_time`"""
        return cls(
            user_id=email.user_id, typ=email.typ, creation_time=email.creation_time
        )


EmailTypes = {
    0: "verification",
    1: "password reset",
}
