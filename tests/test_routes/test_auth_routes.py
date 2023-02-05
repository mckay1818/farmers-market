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
    assert response.status_code == 201
    assert response_body == f"Seller {SELLER_FIRST_NAME} {SELLER_LAST_NAME}, owner of {SELLER_STORE_NAME} successfully created."

    new_seller = Seller.query.get(1)

    assert new_seller
    assert new_seller.store_name == SELLER_STORE_NAME