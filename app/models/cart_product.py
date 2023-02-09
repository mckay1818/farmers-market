from app import db
from sqlalchemy.orm import relationship

class CartProduct(db.Model):
    __tablename__ = 'cart_product'
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    cart = relationship('Cart', back_populates='products_association')
    product = relationship('Product', back_populates='carts')