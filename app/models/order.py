from app import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='order')
    cart = db.relationship('Cart', back_populates='order')