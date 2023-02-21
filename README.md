# Farmer's Market - Backend

An e-commerce website that allows farmers to sell directly to consumers in an open online marketplace.

This website allows users to create an account as a Seller or a Customer. All registered users are able to access the marketplace of Sellers on login. Sellers can build out their store by adding products, and Customers can add these products to their cart and checkout with Stripe. 

This project backend consists of a Flask REST API connected to a PostgreSQL database via a SQLAlchemy connection.

<img width="600" alt="Farmer's Market landing page" src="https://user-images.githubusercontent.com/72710253/219997390-e9afb831-19b2-415f-a28f-e01dc0918730.png">
<img width="600" alt="Customer's View of a Seller page" src="https://user-images.githubusercontent.com/72710253/219997521-fbe40a0b-a95f-486b-b6af-9f187a3d0b82.png">
<img width="330" alt="Cart page shown with dynamically collapsed navigation bar" src="https://user-images.githubusercontent.com/72710253/219997635-cd3d15d0-671c-4bd3-823d-8b15c20584ee.png">



## Tech Stack

* React: frontend
* Flask: backend REST API
* PostgreSQL: database
* SQLAlchemy: object-relational mapper (ORM)
* Stripe API: customer checkout
* Heroku: deployment [(view deployed project)](https://farmers-market-fe.herokuapp.com/)
* Docker: containerization
* AWS: ECS, RDS, S3 (in-progress)

## Backend Features

* Integration with Stripe API for customer checkout
* Authentication system built with JWT's and custom-made role-based permissions.

## View Deployed Project

* The deployed project on Heroku can be viewed at [https://farmers-market-fe.herokuapp.com/](https://farmers-market-fe.herokuapp.com/)
* Test Seller account credentials:
    * email: tammyburns@fakemail.com
    * password: cowcrazy
* Test Customer account credentials:
    * email: m1@fakemail.com
    * password: greenbeans

## Backend Installation

1. Fork and clone this repository
2. Create a virtual environment by running the following in your terminal (make sure you are in your cloned repo's folder)
```
$ python3 -m venv venv
$ source venv/bin/activate
```
3. Install dependencies
```
(venv) $ pip install -r requirements.txt
```
4. Create a database named farmers_market_development (new to PostgresQL? Find instructions for installation and setup [here](https://www.postgresql.org/))
5. Export the required environment variables
```
(venv) $ export SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@localhost:5432/farmers_market_development'
(venv) $ export FLASK_APP=app.py
(venv) $ export FLASK_ENV=development
```
6. Run `flask run` to start the server on http://localhost:5000
