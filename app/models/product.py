from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    description = db.Column(db.Text)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    seller = db.relationship('Seller', back_populates='products')
    carts = db.relationship('CartProduct', back_populates='product')

    # Convenience Initializer/Seconday Constructor
    @classmethod
    def from_dict(cls, dict):
        new_product = Product(
        name=dict["name"],
        price=dict["price"],
        quantity=dict["quantity"],
        image_file=dict["image_file"],
        description=dict["description"],
        seller_id=dict["seller_id"]
        )
        return new_product

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "image_file": self.image_file,
            "description": self.description,
        }

    def update_inventory(self):
        self.quantity -= 1
        # TODO - add deletion of item if out of stock
