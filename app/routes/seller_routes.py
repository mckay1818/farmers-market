from app import db
from app.routes.validation_functions import validate_request_and_create_obj, validate_current_user
from app.models.seller import Seller
from app.models.product import Product
from flask import Blueprint, jsonify, abort, make_response, request

sellers_bp = Blueprint("sellers", __name__, url_prefix="/sellers")

##################
# SELLER ROUTES #
##################

# READ
@sellers_bp.route("", methods=["GET"])
def get_all_sellers():
    sellers = Seller.query.all()
    sellers_response = []
    for seller in sellers:
        sellers_response.append(seller.to_dict())
    return jsonify(sellers_response)

@sellers_bp.route("/<store_name>", methods=["GET"])
def get_one_seller_by_id(store_name):
    store_name = store_name.strip().replace("-", " ")
    seller = Seller.validate_by_store_name_and_get_entry(store_name)
    if not seller:
        abort(make_response({"message": f"Seller {store_name} not found"}, 404))
    return seller.to_dict()

# UPDATE
@sellers_bp.route("/<store_name>", methods=["PUT"])
def update_one_seller(store_name):
    store_name = store_name.strip().replace("-", " ")
    seller = Seller.validate_by_store_name_and_get_entry(store_name)
    if not seller:
        abort(make_response({"message": f"Seller {store_name} not found"}, 404))
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
@sellers_bp.route("/<store_name>", methods=["DELETE"])
def delete_one_seller(store_name):
    store_name = store_name.strip().replace("-", " ")
    seller = Seller.validate_by_store_name_and_get_entry(store_name)
    if not seller:
        abort(make_response({"message": f"Seller {store_name} not found"}, 404))

    db.session.delete(seller)
    db.session.commit()
    return make_response(jsonify(f"Seller {seller.first_name} {seller.last_name}, owner of {seller.store_name} successfully deleted."), 200)


##################
# NESTED PRODUCT ROUTES #
##################

# CREATE
@sellers_bp.route("/<store_name>/products", methods=["POST"])
def add_product_to_seller(store_name):
    current_user = validate_current_user(store_name)
    request_body = request.get_json()
    request_body["seller_id"] = current_user.id

    new_product = validate_request_and_create_obj(Product, request_body)

    db.session.add(new_product)
    db.session.commit()
    return make_response(jsonify(f"Product {new_product.name} from {new_product.seller.store_name} successfully created."), 201)

# READ
@sellers_bp.route("/<store_name>/products", methods=["GET"])
def get_all_products_for_one_seller(store_name):
    store_name = store_name.strip().replace("-", " ")
    seller = Seller.validate_by_store_name_and_get_entry(store_name)
    products = Product.query.filter_by(seller_id=seller.id)
    products_response = []
    for product in products:
        products_response.append(product.to_dict())
    return jsonify(products_response)

# TODO - add route for reading 1 product by id

# UPDATE
@sellers_bp.route("/<store_name>/products/<product_id>", methods=["PUT"])
def update_one_product_for_one_seller(store_name, product_id):
    current_user = validate_current_user(store_name)
    product = Product.query.filter_by(seller=current_user, id=product_id).first()
    if not product:
        abort(make_response({"message": f"Product not found"}, 404))

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
@sellers_bp.route("/<store_name>/products/<product_id>", methods=["DELETE"])
def delete_one_product_for_one_seller(store_name, product_id):
    current_user = validate_current_user(store_name)
    product = Product.query.filter_by(seller=current_user, id=product_id).first()
    if not product:
        abort(make_response({"message": f"Product not found"}, 404))

    db.session.delete(product)
    db.session.commit()
    return make_response(jsonify(f"Product {product.name} from {product.seller.store_name} successfully deleted."), 200)