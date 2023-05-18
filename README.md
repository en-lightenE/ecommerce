# E-Commerce API

This repository contains an e-commerce API developed using Django and Django REST Framework. The API provides endpoints to manage products, orders, and user authentication.

## Features

- CRUD operations for products
- Create and manage orders
- Unit testing using pytest

## Installation

1. Clone the repository:


2. Create a virtual environment and activate it:

python -m venv env
source env/bin/activate # for Linux/Mac
env\Scripts\activate # for Windows

3. Install the required dependencies:

pip install -r requirements.txt

4. Set up the database:

python manage.py migrate


5. Start the development server:

python manage.py runserver


6. The API will be accessible at `http://localhost:8000/`.

## Usage

You can use tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/) to interact with the API.

Available endpoints:

- `/api/products/` - GET (list products), POST (create a product)
- `/api/products/{id}/` - GET (retrieve a product), PUT (update a product), DELETE (delete a product)



## Testing

Unit tests for the API are implemented using pytest. To run the tests, execute the following command:
pytest
