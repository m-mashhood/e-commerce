# ecommerce

A multi-vendor ecommerce solution in which multiple users can sign up and
sale there products. The system maintains record of all the products of the vendors, retailers and buyers
who sign up on the system. Retailer & Buyer can purchase the products from Vendor & Retailer respectively. 
Vendors & Retailers can also add the products in the system to sale to other entities.
System also keeps record of all the sales of a vendors & retailers.

### Setup

First, create virtualenv for python:

    python -m venv venv

Activate the environment:

    source venv/bin/activate

Install requirements from requirements.txt:

    pip install -r requirements.txt

Run the project:

    python manage.py runserver

