from app.models.seller import Seller
from app.models.product import Product

SELLER_ID = 1
SELLER_STORE_NAME = "Green Acres"
SELLER_STORE_DESCRIPTION = "An apple orchard that specializes in homemade pies, jams, and cider."
SELLER_FIRST_NAME = "Lila"
SELLER_LAST_NAME = "Parker"
SELLER_EMAIL = "lilaparker@fakemail.com"
SELLER_PASSWORD = "password"
SELLER_ADDRESS_1 = "278 Armstrong Rd"
SELLER_CITY = "Hudson"
SELLER_REGION = "New York"
SELLER_POSTAL_CODE = 12534

# LOGIN
def test_login_seller(client, one_seller):
    # Act
    response = client.post("/login", json={
        "email": SELLER_EMAIL,
        "password": SELLER_PASSWORD,
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert "access_token" in response_body

def test_login_requires_email(client, one_seller):
    # Act
    response = client.post("/login", json={
        "password": SELLER_PASSWORD,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "message" in response_body
    assert "Request body must include email" in response_body["message"]

def test_login_nonexistent_seller(client, one_seller):
    # Act
    response = client.post("/login", json={
        "email": "fakeemail@fakemail.com",
        "password": SELLER_PASSWORD,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" in response_body
    assert "User not found" in response_body["message"]

def test_login_incorrect_password(client, one_seller):
    # Act
    response = client.post("/login", json={
        "email": SELLER_EMAIL,
        "password": "incorrect",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 401
    assert "message" in response_body
    assert "Incorrect password" in response_body["message"]

# CREATE ONE SELLER
def test_create_one_seller(client):
    # Act
    response = client.post("/sellers/signup", json={
        "store_name": SELLER_STORE_NAME,
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "password": SELLER_PASSWORD,
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
    response = client.post("/sellers/signup", json={
        "store_description": SELLER_STORE_DESCRIPTION,
        "first_name": SELLER_FIRST_NAME,
        "last_name": SELLER_LAST_NAME,
        "email": SELLER_EMAIL,
        "password": SELLER_PASSWORD,
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
