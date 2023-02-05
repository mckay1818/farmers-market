from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    if not test_config:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

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
    from .routes.seller_routes import sellers_bp
    from .routes.auth import auth_bp
    app.register_blueprint(sellers_bp)
    app.register_blueprint(auth_bp)

    jwt.init_app(app)
    CORS(app)
    return app