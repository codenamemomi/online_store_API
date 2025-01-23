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
    Windows use `venv\Scripts\activate  #on Mac source venv/bin/activate  
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a [.env](http://_vscodecontentref_/2) file in the root of your project and add your PayPal credentials:

    ```env
    PAYPAL_MODE=sandbox
    PAYPAL_CLIENT_ID=your_paypal_client_id
    PAYPAL_CLIENT_SECRET=your_paypal_client_secret
    ```
    You can get your PayPal credentials from the [PayPal Developer Dashboard](https://developer.paypal)
    .

5. Apply migrations:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

- Access the API at `http://127.0.0.1:8000/store/`
- Access the admin panel at `http://127.0.0.1:8000/admin/`

## API Endpoints

### Products

- GET /store/products/: List all products (accessible by customers and admins)
- POST /store/products/: Create a new product (accessible by admins)
- GET /store/products/{id}/: Retrieve a product by ID (accessible by customers and admins)
- PATCH /store/products/{id}/: Update a product by ID (accessible by admins)
- DELETE /store/products/{id}/: Delete a product by ID (accessible by admins)

### Categories

- GET /store/categories/: List all categories (accessible by customers and admins)
- POST /store/categories/: Create a new category (accessible by admins)
- GET /store/categories/{id}/: Retrieve a category by ID (accessible by customers and admins)
- PATCH /store/categories/{id}/: Update a category by ID (accessible by admins)
- DELETE /store/categories/{id}/: Delete a category by ID (accessible by admins)

### Cart

- POST /store/cart/: Add a product to the cart (accessible by customers and admins)
- GET /store/cart/: Retrieve the cart for the authenticated user (accessible by customers and admins)
- PATCH /store/cart/: Update the quantity of a product in the cart (accessible by customers and admins)
- DELETE /store/cart/: Remove a product from the cart (accessible by customers and admins)

### Orders

- POST /store/orders/: Place an order using the products in the cart (accessible by customers and admins)
- GET /store/orders/{order_id}/: Retrieve an order by ID (accessible by customers and admins)
- PATCH /store/orders/{order_id}/: Update the status of an order by ID (accessible by admins)

### Payments

- POST /store/create/payments/: Create a payment and get the approval URL (accessible by customers)
- GET /store/execute/payment/(link from redirection after payment is done): Execute a payment after approval (accessible by customers)
- GET /store/payments/: Retrieve a payment lists (accessible by admins)
- GET /store/payment/{payment_id}/: Retrieve a payment by ID (accessible by admins)
- DELETE /store/payment/{payment_id}/: Delete a payment by ID (accessible by admins)

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
