# fixtures module, automatically imported by pytest 
# to all files in parent directory, tests
import pytest
from app import create_app
from app import db
from app.models.seller import Seller
from app.models.product import Product
from flask.signals import request_finished

SELLER_1_STORE_NAME = "Green Acres"
SELLER_1_STORE_DESCRIPTION = "An apple orchard that specializes in homemade pies, jams, and cider."
SELLER_1_FIRST_NAME = "Lila"
SELLER_1_LAST_NAME = "Parker"
SELLER_1_EMAIL = "lilaparker@fakemail.com"
SELLER_1_PASSWORD = "password"
SELLER_1_ADDRESS_1 = "278 Armstrong Rd"
SELLER_1_CITY = "Hudson"
SELLER_1_REGION = "New York"
SELLER_1_POSTAL_CODE = 12534

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
        store_name=SELLER_1_STORE_NAME,
        store_description=SELLER_1_STORE_DESCRIPTION,
        first_name=SELLER_1_FIRST_NAME,
        last_name=SELLER_1_LAST_NAME,
        email=SELLER_1_EMAIL,
        password=SELLER_1_PASSWORD,
        address_1=SELLER_1_ADDRESS_1,
        city=SELLER_1_CITY,
        region=SELLER_1_REGION,
        postal_code=SELLER_1_POSTAL_CODE
    )
    db.session.add(new_seller)
    db.session.commit()

@pytest.fixture
def second_seller(app):
    new_seller = Seller(
        store_name="Happy Cows",
        store_description="A dairy farm in West Tennessee.",
        first_name="Tammy",
        last_name="Burns",
        email="tburns@fakemail.com",
        password="cowcrazy",
        address_1="134 Parham Rd",
        city="Martin",
        region="Tennessee",
        postal_code=38237
    )
    db.session.add(new_seller)
    db.session.commit()

@pytest.fixture
def one_saved_product(app, one_seller):
    new_product = Product(
        name="Sweet Corn",
        price=3,
        quantity=20,
        image_file=None,
        description="Delicious sweet corn!",
        seller_id=1,
    )
    db.session.add(new_product)
    db.session.commit()