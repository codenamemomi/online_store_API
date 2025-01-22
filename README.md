# Online Store API

This is an online store API built with Django. It provides endpoints for managing products, orders, and users.

## Features

- User authentication and authorization
- Product management (CRUD operations)
- Order management (CRUD operations)
- API documentation with Django REST framework
- Role-based access control (Admin and Customer)

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

### Products

- GET /api/products/: List all products (accessible by customers and admins)
- POST /api/products/: Create a new product (accessible by admins)
- GET /api/products/{id}/: Retrieve a product by ID (accessible by customers and admins)
- PATCH /api/products/{id}/: Update a product by ID (accessible by admins)
- DELETE /api/products/{id}/: Delete a product by ID (accessible by admins)

### Categories

- GET /api/categories/: List all categories (accessible by customers and admins)
- POST /api/categories/: Create a new category (accessible by admins)
- GET /api/categories/{id}/: Retrieve a category by ID (accessible by customers and admins)
- PATCH /api/categories/{id}/: Update a category by ID (accessible by admins)
- DELETE /api/categories/{id}/: Delete a category by ID (accessible by admins)

### Cart

- POST /api/cart/: Add a product to the cart (accessible by customers and admins)
- GET /api/cart/: Retrieve the cart for the authenticated user (accessible by customers and admins)
- PATCH /api/cart/: Update the quantity of a product in the cart (accessible by customers and admins)
- DELETE /api/cart/: Remove a product from the cart (accessible by customers and admins)

### Orders

- POST /api/orders/: Place an order using the products in the cart (accessible by customers and admins)
- GET /api/orders/{order_id}/: Retrieve an order by ID (accessible by customers and admins)
- PATCH /api/orders/{order_id}/: Update the status of an order by ID (accessible by admins)

### Permissions

- Admin: Can create, update, and delete products and categories.
- Customer: Can view products and categories.

Testing
- You can use tools like Postman or curl to test the API endpoints.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License.
