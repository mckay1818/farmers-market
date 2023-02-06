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
    assert "message" in response_body
    assert "Login successful" in response_body["message"]

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

