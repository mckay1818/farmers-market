from app import db
from app.routes.validation_functions import validate_id_and_get_entry, validate_request_and_create_obj
from app.models.seller import Seller
from app.models.product import Product
from flask import Blueprint, jsonify, abort, make_response, request

sellers_bp = Blueprint("sellers", __name__, url_prefix="/sellers")

##################
# SELLER ROUTES #
##################

# CREATE
@sellers_bp.route("", methods=["POST"])
def create_seller():
    request_body = request.get_json()
    new_seller = validate_request_and_create_obj(Seller, request_body)

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

    
# @sellers_bp.route("/<seller_id>", methods=["GET"])
# def get_one_seller_by_id(seller_id):
#     seller = Seller.validate_id_and_get_entry(seller_id)
#     return seller.to_dict()

@sellers_bp.route("/<store_name>", methods=["GET"])
def get_one_seller_by_id(store_name):
    store_name = store_name.strip().replace("_", " ")
    seller = Seller.validate_by_store_name_and_get_entry(store_name)
    if not seller:
        abort(make_response({"message": f"Seller {store_name} not found"}, 404))
    return seller.to_dict()

# UPDATE
@sellers_bp.route("/<seller_id>", methods=["PUT"])
def update_one_seller(seller_id):
    seller = validate_id_and_get_entry(Seller, seller_id)
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
    seller = validate_id_and_get_entry(Seller, seller_id)
    db.session.delete(seller)
    db.session.commit()
    return make_response(jsonify(f"Seller {seller.first_name} {seller.last_name}, owner of {seller.store_name} successfully deleted."), 200)


##################
# NESTED PRODUCT ROUTES #
##################

# CREATE
@sellers_bp.route("/<seller_id>/products", methods=["POST"])
def add_product_to_seller(seller_id):
    seller = validate_id_and_get_entry(Seller, seller_id)
    request_body = request.get_json()
    request_body["seller_id"] = seller.id

    new_product = validate_request_and_create_obj(Product, request_body)

    db.session.add(new_product)
    db.session.commit()
    return make_response(jsonify(f"Product {new_product.name} from {new_product.seller.store_name} successfully created."), 201)

# READ
@sellers_bp.route("/<seller_id>/products", methods=["GET"])
def get_all_products_for_one_seller(seller_id):
    seller = validate_id_and_get_entry(Seller, seller_id)
    products = Product.query.filter_by(seller_id=seller.id)
    products_response = []
    for product in products:
        products_response.append(product.to_dict())
    return jsonify(products_response)

# TODO - add route for reading 1 product by id

# UPDATE
@sellers_bp.route("/<seller_id>/products/<product_id>", methods=["PUT"])
def update_one_product_for_one_seller(seller_id, product_id):
    seller = validate_id_and_get_entry(Seller, seller_id)
    product = validate_id_and_get_entry(Product, product_id)
    request_body = request.get_json()
    try:
        product.name = request_body["name"]
        product.price = request_body["price"]
        product.quantity = request_body["quantity"]
        product.image_file = request_body["image_file"]
        product.description = request_body["description"]
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}."}), 400))

    db.session.commit()
    return make_response(jsonify(f"Product {product.name} from {product.seller.store_name} successfully updated."), 200)
    

# DELETE
@sellers_bp.route("/<seller_id>/products/<product_id>", methods=["DELETE"])
def delete_one_product_for_one_seller(seller_id, product_id):
    seller = validate_id_and_get_entry(Seller, seller_id)
    product = validate_id_and_get_entry(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return make_response(jsonify(f"Product {product.name} from {product.seller.store_name} successfully deleted."), 200)
