# fixtures module, automatically imported by pytest 
# to all files in parent directory, tests
import pytest
from app import create_app
from app import db
from app.models.seller import Seller
from flask.signals import request_finished

SELLER_STORE_NAME = "Green Acres"
SELLER_STORE_DESCRIPTION = "An apple orchard that specializes in homemade pies, jams, and cider."
SELLER_FIRST_NAME = "Lila"
SELLER_LAST_NAME = "Parker"
SELLER_EMAIL = "lilaparker@fakemail.com"
SELLER_ADDRESS_1 = "278 Armstrong Rd"
SELLER_CITY = "Hudson"
SELLER_REGION = "New York"
SELLER_POSTAL_CODE = 12534

# setup application instance
@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    # end session to test that changes are persisted in db
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # clear db after test
    with app.app_context():
        db.drop_all()

# setup test client for HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_seller(app):
    new_seller = Seller(
        store_name=SELLER_STORE_NAME,
        store_description=SELLER_STORE_DESCRIPTION,
        first_name=SELLER_FIRST_NAME,
        last_name=SELLER_LAST_NAME,
        email=SELLER_EMAIL,
        address_1=SELLER_ADDRESS_1,
        city=SELLER_CITY,
        region=SELLER_REGION,
        postal_code=SELLER_POSTAL_CODE
    )
    db.session.add(new_seller)
    db.session.commit()