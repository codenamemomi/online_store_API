# Online Store API

This is an online store API built with Django. It provides endpoints for managing products, orders, and users.

## Features

- User authentication and authorization
- Product management (CRUD operations)
- Order management (CRUD operations)
- API documentation with Django REST framework

## Requirements

- Python 3.x
- Django 3.x or higher
- Django REST framework

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/online_store_API.git
    cd online_store_API
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

- Access the API at `http://127.0.0.1:8000/api/`
- Access the admin panel at `http://127.0.0.1:8000/admin/`

## API Endpoints

- `GET /api/products/` - List all products
- `POST /api/products/` - Create a new product
- `GET /api/products/{id}/` - Retrieve a product by ID
- `PUT /api/products/{id}/` - Update a product by ID
- `DELETE /api/products/{id}/` - Delete a product by ID
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create a new order
- `GET /api/orders/{id}/` - Retrieve an order by ID
- `PUT /api/orders/{id}/` - Update an order by ID
- `DELETE /api/orders/{id}/` - Delete an order by ID

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.
