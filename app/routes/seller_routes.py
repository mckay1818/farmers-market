from app import db
from app.models.seller import Seller
from flask import Blueprint, jsonify, abort, make_response, request

sellers_bp = Blueprint("sellers", __name__, url_prefix="/sellers")

# TODO - generalize this validate model fn
def validate_seller(cls, request_body):
    try:
        new_seller = cls.from_dict(request_body)
    except KeyError as e:
        # strip one pair of quotes off key
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}."}), 400))
    return new_seller

# TODO - generalize this validate by id fn
def validate_id_and_get_entry(seller_id):
    try:
        seller_id = int(seller_id)
    except:
        abort(make_response({"message": f"Seller ID {seller_id} invalid"}, 400))
    
    seller = Seller.query.get(seller_id)
    if not seller:
        abort(make_response({"message": f"Seller ID {seller_id} not found"}, 404))
    
    return seller

# CREATE
@sellers_bp.route("", methods=["POST"])
def create_seller():
    request_body = request.get_json()
    new_seller = validate_seller(Seller, request_body)

    db.session.add(new_seller)
    db.session.commit()

    return make_response(jsonify(f"Seller {new_seller.first_name} {new_seller.last_name}, owner of {new_seller.store_name} successfully created."), 201)

# READ
@sellers_bp.route("", methods=["GET"])
def get_all_sellers():
    sellers = Seller.query.all()
    sellers_response = []
    for seller in sellers:
        sellers_response.append(seller.to_dict())
    return jsonify(sellers_response)

    
@sellers_bp.route("/<seller_id>", methods=["GET"])
def get_one_seller_by_id(seller_id):
    seller = validate_id_and_get_entry(seller_id)
    return seller.to_dict()

# UPDATE
@sellers_bp.route("/<seller_id>", methods=["PUT"])
def update_one_seller(seller_id):
    seller = validate_id_and_get_entry(seller_id)
    request_body = request.get_json()
    try:
        seller.store_name = request_body["store_name"]
        seller.store_descriptions = request_body["store_description"]
        seller.first_name = request_body["first_name"]
        seller.last_name = request_body["last_name"]
        seller.email = request_body["email"]
        seller.address_1 = request_body["address_1"]
        seller.city = request_body["city"]
        seller.region = request_body["region"]
        seller.postal_code = request_body["postal_code"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}."}), 400))
    
    db.session.commit()
    return make_response(jsonify(f"Seller {seller.first_name} {seller.last_name}, owner of {seller.store_name} successfully updated."), 200)
    
# DELETE
@sellers_bp.route("/<seller_id>", methods=["DELETE"])
def delete_one_seller(seller_id):
    seller = validate_id_and_get_entry(seller_id)
    db.session.delete(seller)
    db.session.commit()
    return make_response(jsonify(f"Seller {seller.first_name} {seller.last_name}, owner of {seller.store_name} successfully deleted."), 200)