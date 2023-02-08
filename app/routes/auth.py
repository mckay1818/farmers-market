from app import db, jwt
from app.routes.validation_functions import validate_request_and_create_obj
from app.models.seller import Seller
from app.models.customer import Customer
from app.models.usermixin import UserMixin
from app.routes.seller_routes import sellers_bp
from app.routes.customer_routes import customers_bp
from flask import Blueprint, jsonify, abort, make_response, request
from flask_jwt_extended import create_access_token, set_access_cookies, unset_access_cookies, jwt_required, current_user, get_jwt

auth_bp = Blueprint("auth", __name__)

# Cb that takes whatever object is passed in as the identity when
#  creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

# Cb that loads user from db when accessing a protected route
# and returns an obj (or None if lookup fails)
@jwt.user_lookup_loader
def user_lookup_cb(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    role = jwt_data["role"]
    if role == "seller":
        return Seller.query.filter_by(id=identity).first()
    elif role == "customer":
        return Customer.query.filter_by(id=identity).first()


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
    access_token = create_access_token(identity=user, additional_claims=additional_claims)
    set_access_cookies(response, access_token)
    return jsonify(access_token=access_token)

@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "Logged out"})
    unset_access_cookies(response)
    return response

@auth_bp.route("/who_am_i", methods=["GET"])
@jwt_required(optional=True)
def protected():
    # We can now access our sqlalchemy object via `current_user`.
    return jsonify(
        id=current_user.id,
        first_name=current_user.first_name,
        username=current_user.store_name,
    )

@sellers_bp.route("/signup", methods=["POST"])
def seller_signup():
    request_body = request.get_json()
    new_seller = validate_request_and_create_obj(Seller, request_body)

    db.session.add(new_seller)
    db.session.commit()

    return make_response(jsonify(f"Seller {new_seller.first_name} {new_seller.last_name}, owner of {new_seller.store_name} successfully created."), 201)

@customers_bp.route("/signup", methods=["POST"])
def customer_signup():
    request_body = request.get_json()
    new_customer = validate_request_and_create_obj(Customer, request_body)

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify(f"Customer {new_customer.username} successfully created."), 201)
