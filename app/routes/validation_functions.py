from flask import abort, make_response, jsonify
from app.models.seller import Seller
from app.models.product import Product
from flask_jwt_extended import verify_jwt_in_request, get_current_user


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

def validate_current_user(store_name):
    store_name = store_name.strip().replace("-", " ")
    verify_jwt_in_request()
    current_user = get_current_user()

    if not current_user:
        abort(make_response({"message": f"Seller {current_user.store_name} not found"}, 404))
    if current_user.store_name != store_name:
        abort(make_response({"message": f"Action forbidden"}, 403))

    return current_user
        
