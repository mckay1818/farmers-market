from app import db
from sqlalchemy.orm import relationship

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(80), nullable=False)
    store_description = db.Column(db.Text)
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

    # Convenience Initializer/Seconday Constructor
    @classmethod
    def from_dict(cls, dict):
        new_seller = Seller(
        store_name=dict["store_name"],
        store_description=dict["store_description"],
        first_name=dict["first_name"],
        last_name=dict["last_name"],
        email=dict["email"],
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
