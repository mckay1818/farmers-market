from app import db
from sqlalchemy.orm import relationship

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    description = db.Column(db.Text)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    seller = db.relationship('Seller', back_populates='products')
    orders = db.relationship('Order', secondary='order_product', back_populates='products')

    def __repr__(self):
        return f"Product {self.name} with quantity {self.quantity}"