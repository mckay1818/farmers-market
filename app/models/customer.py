from app import db
from .usermixin import UserMixin
from app.models.cart import Cart
from app.models.product import Product
from app.models.cart_product import CartProduct

class Customer(db.Model, UserMixin):
    username = db.Column(db.String(20), unique=True, nullable=False)
    # 1-1 relationship
    cart = db.relationship('Cart', back_populates='customer', uselist=False)
    orders = db.relationship('Order', back_populates='customer')

    # Convenience Initializer/Seconday Constructor
    @classmethod
    def from_dict(cls, dict):
        new_customer = Customer(
        username=dict["username"],
        first_name=dict["first_name"],
        last_name=dict["last_name"],
        email=dict["email"],
        password=dict["password"],
        address_1=dict["address_1"],
        city=dict["city"],
        region=dict["region"],
        postal_code=dict["postal_code"],
        cart=Cart()
        )
        return new_customer

    @classmethod
    def validate_by_username_and_get_entry(cls, username):
        obj = cls.query.filter_by(username=username).first()
        if not obj:
            return None
        return obj

    def to_dict(self):
        return {
            # TODO - REMOVE ID?
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address_1": self.address_1,
            "city": self.city,
            "region": self.region,
            "postal_code": self.postal_code
        }

    def get_cart_items(self):
        items = Product.query.join(CartProduct).filter_by(cart_id=self.cart.id).all()
        items_list = []
        if not self.cart.products:
            return items_list
        for item in items:
            items_list.append({
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
            })

        return items_list

    # def clear_cart(self):
    #     next_id = self.cart.id + 1
    #     self.cart = Cart(id=next_id, customer_id=self.id)