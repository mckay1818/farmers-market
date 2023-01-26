from app import db
from sqlalchemy.orm import relationship

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    address_1 = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(80), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, default=5000)
    orders = db.relationship('Order', back_populates='customer', lazy=True)

    def __repr__(self):
        return f"Customer {self.first_name} {self.last_name}, email {self.email}"