from app import db
from sqlalchemy.orm import relationship

class OrderProduct(db.Model):
    __tablename__ = 'order_product'
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer)

    order = relationship('Order', back_populates='products_association')
    product = relationship('Product', back_populates='orders')