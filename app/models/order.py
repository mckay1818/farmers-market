from app import db
from sqlalchemy.orm import relationship


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime)
    is_shipped = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='orders')
    products = db.relationship('Product', secondary='order_product', back_populates='orders')


    def __repr__(self):
        return f"Order #{self.id} made by Customer {self.customer}"