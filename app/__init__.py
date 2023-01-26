from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/farmers_market_development'


    # import models for Alembic setup
    from app.models.seller import Seller
    from app.models.customer import Customer
    from app.models.product import Product
    from app.models.order import Order
    from app.models.order_product import OrderProduct

    # setup db
    db.init_app(app)
    migrate.init_app(app, db)

    # import and register blueprints

    return app