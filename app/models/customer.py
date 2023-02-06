from app import db
from sqlalchemy.orm import relationship
from .usermixin import UserMixin

class Customer(db.Model, UserMixin):
    username = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, default=5000)
    orders = db.relationship('Order', back_populates='customer', lazy=True)

    # @classmethod
    # def validate_by_store_name_and_get_entry(cls, store_name):
    #     obj = cls.query.filter_by(store_name=store_name).first()
    #     if not obj:
    #         return None
    #     return obj


    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "store_name": self.store_name,
    #         "store_description": self.store_description,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "email": self.email,
    #         "address_1": self.address_1,
    #         "city": self.city,
    #         "region": self.region,
    #         "postal_code": self.postal_code
    #     }