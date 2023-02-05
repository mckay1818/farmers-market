from app import db
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash

class UserMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    address_1 = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    region = db.Column(db.String(80), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)

    @property
    def password(self):
        raise AttributeError("Cannot read password")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)