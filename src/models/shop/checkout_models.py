from muffin_shop.helpers.main.plugins import db


class Transaction(db.Model):
    """Represents a successful transaction -- a cart of products that someone bought"""

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    uuid = db.Column(db.String(60), nullable=False)
    products = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    shipping_address = db.Column(db.String(1024), nullable=True)
    phone_number = db.Column(db.String(11), nullable=True)
    email_address = db.Column(db.String(40), nullable=True)
    customer_name = db.Column(db.String(40), nullable=True)
    customer_uuid = db.Column(db.String(60), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
