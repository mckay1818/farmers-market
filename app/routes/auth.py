from app import db, jwt
from app.routes.validation_functions import validate_id_and_get_entry, validate_request_and_create_obj
from app.models.seller import Seller
from app.models.customer import Customer
from app.models.usermixin import UserMixin
from app.models.product import Product
from flask import Blueprint, jsonify, abort, make_response, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies

auth_bp = Blueprint("auth", __name__)

# Cb that loads user from db when accessing a protected route
# and returns an obj
# 

@auth_bp.route("/login", methods=["POST"])
def login():
    request_body = request.get_json()
    try:
        email = request_body["email"]
        password = request_body["password"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}."}), 400))

    user = Seller.query.filter_by(email=email).first()
    if Seller.query.filter_by(email=email).first():
        user = Seller.query.filter_by(email=email).first()
        additional_claims = {"role": f"{user.__tablename__}", "username": f"{user.store_name}"}
    elif Customer.query.filter_by(email=email).first():
        user = Customer.query.filter_by(email=email).first()
        additional_claims = {"role": f"{user.__tablename__}", "username": f"{user.username}"}
    else:
        return abort(make_response({"message": f"User not found"}, 404))
    
    if not user.verify_password(password):
        return abort(make_response({"message": f"Incorrect password"}, 401))

    response = jsonify({"message": "Login successful"})
    access_token = create_access_token(email, additional_claims=additional_claims)
    set_access_cookies(response, access_token)
    return response

@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out"})
    unset_access_cookies(response)
    return response

@auth_bp.route("/customer-login")
def customer_login():
    pass

@auth_bp.route("/seller-signup")
def seller_signup():
    pass

@auth_bp.route("/customer-signup")
def customer_signup():
    pass
