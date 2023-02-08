from app import db
from app.routes.validation_functions import validate_request_and_create_obj, validate_current_customer
from app.models.seller import Seller
from app.models.customer import Customer
from app.models.product import Product
from flask import Blueprint, jsonify, abort, make_response, request

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

##################
# CUSTOMER ROUTES #
##################

# READ
@customers_bp.route("/<username>", methods=["GET"])
def get_one_seller_by_id(username):
    username = username.strip().replace("-", " ")
    customer = Customer.validate_by_username_and_get_entry(username)
    if not customer:
        abort(make_response({"message": f"Customer {username} not found"}, 404))
    return customer.to_dict()

# UPDATE
@customers_bp.route("/<username>", methods=["PUT"])
def update_one_customer(username):
    current_user = validate_current_customer(username)
    request_body = request.get_json()
    try:
        current_user.username = request_body["username"]
        current_user.first_name = request_body["first_name"]
        current_user.last_name = request_body["last_name"]
        current_user.email = request_body["email"]
        current_user.address_1 = request_body["address_1"]
        current_user.city = request_body["city"]
        current_user.region = request_body["region"]
        current_user.postal_code = request_body["postal_code"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}."}), 400))
    
    db.session.commit()
    return make_response(jsonify(f"Customer {username} successfully updated."), 200)
