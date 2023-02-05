from app import db
from sqlalchemy.orm import relationship
from .usermixin import UserMixin

class Customer(db.Model, UserMixin):
    username = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, default=5000)
    orders = db.relationship('Order', back_populates='customer', lazy=True)

    def __repr__(self):
        return f"Customer {self.username}, email {self.email}"