from flask import abort, make_response, jsonify
from app.models.seller import Seller
from app.models.product import Product


def validate_request_and_create_obj(cls, request_body):
    try:
        new_obj = cls.from_dict(request_body)
    except KeyError as e:
        # strip one pair of quotes off key
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}."}), 400))
    return new_obj

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