from app.models.seller import Seller
from app.models.product import Product

SELLER_ID = 1
SELLER_STORE_NAME = "Green Acres"
SELLER_STORE_DESCRIPTION = "An apple orchard that specializes in homemade pies, jams, and cider."
SELLER_FIRST_NAME = "Lila"
SELLER_LAST_NAME = "Parker"
SELLER_EMAIL = "lilaparker@fakemail.com"
SELLER_ADDRESS_1 = "278 Armstrong Rd"
SELLER_CITY = "Hudson"
SELLER_REGION = "New York"
SELLER_POSTAL_CODE = 12534

# assert response_body.id == 1
# assert response_body.store_name == SELLER_STORE_NAME
# assert response_body.store_description == SELLER_STORE_DESCRIPTION
# assert response_body.first_name == SELLER_FIRST_NAME
# assert response_body.last_name == SELLER_LAST_NAME
# assert response_body.email == SELLER_EMAIL
# assert response_body.address_1 == SELLER_ADDRESS_1
# assert response_body.city == SELLER_CITY
# assert response_body.region == SELLER_REGION
# assert response_body.postal_code == SELLER_POSTAL_CODE

##################
# SELLER ROUTES #
##################

# CREATE
def test_create_one_seller(client):
    # Act
    response = client.post("/sellers", json={
        "store_name": SELLER_STORE_NAME,
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "address_1": SELLER_ADDRESS_1,
        "city": SELLER_CITY,
        "region": SELLER_REGION,
        "postal_code": SELLER_POSTAL_CODE
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 201
    assert response_body == f"Seller {SELLER_FIRST_NAME} {SELLER_LAST_NAME}, owner of {SELLER_STORE_NAME} successfully created."

    new_seller = Seller.query.get(1)

    assert new_seller
    assert new_seller.store_name == SELLER_STORE_NAME

def test_create_seller_must_contain_store_name(client):
    # Act
    response = client.post("/sellers", json={
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "address_1": SELLER_ADDRESS_1,
        "city": SELLER_CITY,
        "region": SELLER_REGION,
        "postal_code": SELLER_POSTAL_CODE
    })
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert "Request body must include store_name" in response_body["message"]
    assert Seller.query.all() == []

# READ
def test_get_sellers_none_saved(client):
    # Act
    response = client.get("/sellers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_sellers(client, one_seller):
    # Act
    response = client.get("/sellers")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body[0]["store_name"] == SELLER_STORE_NAME

def test_get_one_seller_by_id(client, one_seller):
    # Act
    response = client.get("/sellers/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "store_name": SELLER_STORE_NAME,
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "address_1": SELLER_ADDRESS_1,
        "city": SELLER_CITY,
        "region": SELLER_REGION,
        "postal_code": SELLER_POSTAL_CODE
    }

def test_get_one_seller_invalid_id(client, one_seller):
    # Act
    response = client.get("/sellers/blah")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert "Seller ID blah invalid" in response_body["message"]

def test_get_one_seller_nonexistent_id(client, one_seller):
    # Act
    response = client.get("/sellers/5")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" in response_body
    assert "Seller ID 5 not found" in response_body["message"]

# UPDATE
def test_update_one_seller(client, one_seller):
    # Act
    response = client.put("/sellers/1", json={
        "store_name": "A New Store Name",
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "address_1": SELLER_ADDRESS_1,
        "city": SELLER_CITY,
        "region": SELLER_REGION,
        "postal_code": SELLER_POSTAL_CODE
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == f"Seller {SELLER_FIRST_NAME} {SELLER_LAST_NAME}, owner of A New Store Name successfully updated."

    new_seller = Seller.query.get(1)

    assert new_seller
    assert new_seller.store_name == "A New Store Name"

def test_update_one_seller_nonexistent_id(client, one_seller):
    # Act
    response = client.put("/sellers/5", json={
        "store_name": "A New Store Name",
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "address_1": SELLER_ADDRESS_1,
        "city": SELLER_CITY,
        "region": SELLER_REGION,
        "postal_code": SELLER_POSTAL_CODE
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" in response_body
    assert "Seller ID 5 not found" in response_body["message"]

def test_update_one_seller_invalid_id(client, one_seller):
    # Act
    response = client.put("/sellers/blah", json={
        "store_name": "A New Store Name",
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "address_1": SELLER_ADDRESS_1,
        "city": SELLER_CITY,
        "region": SELLER_REGION,
        "postal_code": SELLER_POSTAL_CODE
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert "Seller ID blah invalid" in response_body["message"]


# DELETE
def test_delete_one_seller(client, one_seller):
    # Act
    response = client.delete("/sellers/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == f"Seller {SELLER_FIRST_NAME} {SELLER_LAST_NAME}, owner of {SELLER_STORE_NAME} successfully deleted."
    assert Seller.query.get(1) == None

def test_delete_nonexistent_seller(client, one_seller):
    # Act
    response = client.delete("/sellers/5")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" in response_body
    assert "Seller ID 5 not found" in response_body["message"]

def test_delete_invalid_seller(client, one_seller):
    # Act
    response = client.delete("/sellers/blah")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert "Seller ID blah invalid" in response_body["message"]

##################
# NESTED PRODUCT ROUTES #
##################

# CREATE
def test_create_one_product(client, one_seller):
    # Act
    response = client.post("/sellers/1/products", json={
        "name": "Sweet Corn",
        "price": 3,
        "quantity": 20,
        "image_file": None,
        "description": "Delicious sweet corn!"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 201
    assert response_body == f"Product Sweet Corn from {SELLER_STORE_NAME} successfully created."

    new_product = Product.query.get(1)

    assert new_product
    assert new_product.price == 3
    assert new_product.quantity == 20
    assert new_product.image_file == "default.jpg"
    assert new_product.description == "Delicious sweet corn!"
    assert new_product.seller.store_name == "Green Acres"

def test_create_one_product_must_contain_name(client, one_seller):
    # Act
    response = client.post("/sellers/1/products", json={
        "price": 3,
        "quantity": 20,
        "image_file": None,
        "description": "Delicious sweet corn!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert "Request body must include name" in response_body["message"]
    assert Product.query.all() == []

# READ
def test_get_all_products_from_one_seller(client, one_saved_product):
    # Act
    response = client.get("/sellers/1/products")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body[0]["name"] == "Sweet Corn"


# UPDATE



# DELETE 