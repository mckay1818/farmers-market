from app import db, jwt
from app.routes.validation_functions import validate_id_and_get_entry, validate_request_and_create_obj
from app.models.seller import Seller
from app.models.customer import Customer
from app.models.usermixin import UserMixin
from app.routes.seller_routes import sellers_bp
from flask import Blueprint, jsonify, abort, make_response, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies, jwt_required

auth_bp = Blueprint("auth", __name__)

# Cb that takes whatever object is passed in as the identity when
#  creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# Cb that loads user from db when accessing a protected route
# and returns an obj (or None if lookup fails)
# @jwt.user_lookup_loader
# def user_lookup_cb(_jwt_header, jwt_data):
#     username = jwt_data["sub"]
#     if Seller.query.f


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
    access_token = create_access_token(identity=user)
    set_access_cookies(response, access_token)
    return response

@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out"})
    unset_access_cookies(response)
    return response

@sellers_bp.route("/signup")
def seller_signup():
    pass

@auth_bp.route("/customer-signup")
def customer_signup():
    pass
