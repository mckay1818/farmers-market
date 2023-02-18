from app import db
from app.routes.validation_functions import validate_request_and_create_obj, validate_current_user, validate_model_by_id
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.cart import Cart
from app.models.cart_product import CartProduct
from flask import Blueprint, jsonify, abort, make_response, request
import stripe
import os

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")
stripe.api_key="sk_test_51McZSQAmweu3gL544pjHvx0hhbgTnzEeUDwUKP9ufhxKhaZRX8rDqKO4llb3xgZBIAqeLLeJFqrVDP45tF8NyeJD008l3rIZe4"

