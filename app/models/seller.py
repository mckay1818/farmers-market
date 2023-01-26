from app import db
from sqlalchemy.orm import relationship

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    address_1 = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(80), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    products = db.relationship('Product', back_populates='seller', lazy=True)

    def __repr__(self):
        return f"Seller {self.first_name} {self.last_name}, email {self.email}"