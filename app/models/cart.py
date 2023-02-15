from app import db
from app.models.order import Order
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', back_populates='cart')
    # 1-1 relationship
    order = db.relationship('Order', back_populates='cart', uselist=False)
    products_association = db.relationship('CartProduct', back_populates='cart')
    products = association_proxy("products_association", "product")

    def calculate_total(self):
        total = 0
        for product in self.products:
            total += product.price
        return total
    
    def place_order(self):
        order = Order(
            order_date=datetime.now(),
            customer_id=self.customer_id,
            cart_id=self.id,
        )
        db.session.add(order)
        db.session.commit()
