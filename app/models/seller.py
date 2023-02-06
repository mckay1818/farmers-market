from app import db
from sqlalchemy.orm import relationship
from .usermixin import UserMixin

class Seller(db.Model, UserMixin):
    store_name = db.Column(db.String(80), nullable=False)
    store_description = db.Column(db.Text)
    products = db.relationship('Product', back_populates='seller', lazy=True)

    # Convenience Initializer/Seconday Constructor
    @classmethod
    def from_dict(cls, dict):
        new_seller = Seller(
        store_name=dict["store_name"],
        store_description=dict["store_description"],
        first_name=dict["first_name"],
        last_name=dict["last_name"],
        email=dict["email"],
        password=dict["password"],
        address_1=dict["address_1"],
        city=dict["city"],
        region=dict["region"],
        postal_code=dict["postal_code"]
        )
        return new_seller

    @classmethod
    def validate_by_store_name_and_get_entry(cls, store_name):
        obj = cls.query.filter_by(store_name=store_name).first()
        if not obj:
            return None
        return obj


    def to_dict(self):
        return {
            "id": self.id,
            "store_name": self.store_name,
            "store_description": self.store_description,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address_1": self.address_1,
            "city": self.city,
            "region": self.region,
            "postal_code": self.postal_code
        }
