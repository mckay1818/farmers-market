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


def validate_model_by_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        # handling invalid id type
        abort(make_response({"message":f"{cls.__name__} {model_id} was invalid"}, 400))

    # return obj data if id in db
    model = cls.query.get(model_id)

    # handle nonexistent id
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model


def validate_current_user(username):
    username = username.strip().replace("-", " ")
    verify_jwt_in_request()
    current_user = get_current_user()

    if not current_user:
        abort(make_response({"message": f"Customer {current_user.username} not found"}, 404))
    elif current_user.__tablename__ == "customer":
        if current_user.username != username:
            abort(make_response({"message": f"Action forbidden"}, 403))
    elif current_user.store_name != username:
            abort(make_response({"message": f"Action forbidden"}, 403))

    return current_user
