from app import db
from sqlalchemy.orm import relationship
from .usermixin import UserMixin

class Customer(db.Model, UserMixin):
    username = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, default=5000)
    orders = db.relationship('Order', back_populates='customer', lazy=True)

    # Convenience Initializer/Seconday Constructor
    @classmethod
    def from_dict(cls, dict):
        new_customer = Customer(
        username=dict["username"],
        first_name=dict["first_name"],
        last_name=dict["last_name"],
        email=dict["email"],
        password=dict["password"],
        address_1=dict["address_1"],
        city=dict["city"],
        region=dict["region"],
        postal_code=dict["postal_code"]
        )
        return new_customer

    @classmethod
    def validate_by_username_and_get_entry(cls, username):
        obj = cls.query.filter_by(username=username).first()
        if not obj:
            return None
        return obj


    def to_dict(self):
        return {
            # TODO - REMOVE ID?
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address_1": self.address_1,
            "city": self.city,
            "region": self.region,
            "postal_code": self.postal_code
        }