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


def validate_id_and_get_entry(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {obj_id} invalid"}, 400))
    
    obj = cls.query.get(obj_id)
    if not obj:
        abort(make_response({"message": f"{cls.__name__} {obj_id} not found"}, 404))
    
    return obj