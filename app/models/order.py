from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime)
    is_shipped = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='orders')
    products_association = db.relationship('OrderProduct', back_populates='order')
    products = association_proxy("products_association", "product")

    def place_order(self):
        self.order_date = datetime.now()
        self.is_shipped = True