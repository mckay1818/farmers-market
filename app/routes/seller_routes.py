from app import db
from app.models.seller import Seller
from flask import Blueprint, jsonify, abort, make_response, request

sellers_bp = Blueprint("sellers", __name__, url_prefix="/sellers")

@sellers_bp.route("", methods=["POST"])
def create_seller():
    request_body = request.get_json()
    # validate seller
    new_seller = Seller(
        store_name=request_body["store_name"],
        store_description=request_body["store_description"],
        first_name=request_body["first_name"],
        last_name=request_body["last_name"],
        email=request_body["email"],
        address_1=request_body["address_1"],
        city=request_body["city"],
        region=request_body["region"],
        postal_code=request_body["postal_code"]
        )

    db.session.add(new_seller)
    db.session.commit()

    return make_response(jsonify(f"Seller {new_seller.first_name} {new_seller.last_name}, owner of {new_seller.store_name} successfully created"), 201)

@sellers_bp.route("", methods=["GET"])
def get_all_sellers():
    sellers = Seller.query.all()
    sellers_response = []
    for seller in sellers:
        sellers_response.append({
            "store_name": seller.store_name
        })
    return jsonify(sellers_response)
