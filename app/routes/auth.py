from app import db
from app.routes.validation_functions import validate_id_and_get_entry, validate_request_and_create_obj
from app.models.seller import Seller
from app.models.product import Product
from flask import Blueprint, jsonify, abort, make_response, request

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/seller-login")
def seller_login():
    pass

@auth_bp.route("/customer-login")
def customer_login():
    pass

@auth_bp.route("/seller-signup")
def seller_signup():
    pass

@auth_bp.route("/customer-signup")
def customer_signup():
    pass

@auth.route("/logout")
def logout():
    return "Logout"