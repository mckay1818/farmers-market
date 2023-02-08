from app.models.customer import Customer

CUSTOMER_ID = 1
CUSTOMER_USERNAME = "grocerygetter11"
CUSTOMER_FIRST_NAME = "Lux"
CUSTOMER_LAST_NAME = "Sanders"
CUSTOMER_EMAIL = "luxsanders@fakemail.com"
CUSTOMER_PASSWORD = "secretword"
CUSTOMER_ADDRESS_1 = "443 Cherry Lane"
CUSTOMER_CITY = "Hudson"
CUSTOMER_REGION = "New York"
CUSTOMER_POSTAL_CODE = 12534

##################
# SELLER ROUTES #
##################

# READ
def test_get_one_customer_by_store_name(client, one_customer):
    # Act
    response = client.get("/customers/grocerygetter11")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": CUSTOMER_ID,
        "username": CUSTOMER_USERNAME,
        "first_name": CUSTOMER_FIRST_NAME,
        "last_name": CUSTOMER_LAST_NAME,
        "email": CUSTOMER_EMAIL,
        "address_1": CUSTOMER_ADDRESS_1,
        "city": CUSTOMER_CITY,
        "region": CUSTOMER_REGION,
        "postal_code": CUSTOMER_POSTAL_CODE
    }

def test_get_one_customer_nonexistent_store_name(client, one_customer):
    # Act
    response = client.get("/customers/fakeuser")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" in response_body
    assert "Customer fakeuser not found" in response_body["message"]

# UPDATE
def test_update_one_customer(client, customer_access_token):
    # Act
    headers = {"Authorization": f"Bearer {customer_access_token}"}
    response = client.put("/customers/grocerygetter11", headers=headers, json={
        "username": CUSTOMER_USERNAME,
        "first_name": CUSTOMER_FIRST_NAME,
        "last_name": CUSTOMER_LAST_NAME,
        "email": CUSTOMER_EMAIL,
        "address_1": "234 New Rd",
        "city": CUSTOMER_CITY,
        "region": CUSTOMER_REGION,
        "postal_code": CUSTOMER_POSTAL_CODE
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == f"Customer {CUSTOMER_USERNAME} successfully updated."

    updated_customer = Customer.query.get(1)

    assert updated_customer
    assert updated_customer.address_1 == "234 New Rd"

def test_update_one_customer_fails_if_unauthorized(client, customer_access_token):
    # Act
    headers = {"Authorization": f"Bearer {customer_access_token}"}
    response = client.put("/customers/notme", headers=headers, json={
        "username": CUSTOMER_USERNAME,
        "first_name": CUSTOMER_FIRST_NAME,
        "last_name": CUSTOMER_LAST_NAME,
        "email": CUSTOMER_EMAIL,
        "address_1": "234 New Rd",
        "city": CUSTOMER_CITY,
        "region": CUSTOMER_REGION,
        "postal_code": CUSTOMER_POSTAL_CODE
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 403
    assert "message" in response_body
    assert "Action forbidden" in response_body["message"]

def test_update_one_customer_needs_all_fields(client, customer_access_token):
    # Act
    headers = {"Authorization": f"Bearer {customer_access_token}"}
    response = client.put("/customers/grocerygetter11", headers=headers, json={
        "username": CUSTOMER_USERNAME,
        "first_name": CUSTOMER_FIRST_NAME,
        "last_name": CUSTOMER_LAST_NAME,
        "email": CUSTOMER_EMAIL,
        "address_1": CUSTOMER_ADDRESS_1,
        "city": CUSTOMER_CITY,
        "postal_code": CUSTOMER_POSTAL_CODE
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body["message"] == f"Request body must include region."

# DELETE
def test_delete_one_customer(client, customer_access_token):
    # Act
    headers = {"Authorization": f"Bearer {customer_access_token}"}
    response = client.delete("/customers/grocerygetter11", headers=headers)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == f"Customer {CUSTOMER_USERNAME} successfully deleted."
    assert Customer.query.get(1) == None

def test_delete_customer_fails_if_unauthorized(client, customer_access_token):
    # Act
    headers = {"Authorization": f"Bearer {customer_access_token}"}
    response = client.delete("/customers/notme", headers=headers)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 403
    assert "message" in response_body
    assert "Action forbidden" in response_body["message"]