# E-commerce API with Django Rest Framework

This project is an e-commerce backend API built using Django Rest Framework. It includes functionalities for viewing, creating, and deleting products, managing wishlists and orders, and implementing JWT authentication with phone OTP. The project also uses PostgreSQL as the database and drf-spectacular for API documentation.

## Features

- **Product Management**: View, create, update, and delete products.
- **Wishlist Management**: Add and remove products from the wishlist.
- **Order Management**: Place and manage orders.
- **Authentication**: Simple JWT authentication with phone OTP.
- **API Documentation**: Comprehensive API documentation using drf-spectacular.
- **Database**: PostgreSQL.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Ashmil114/E-commerce-API.git
    cd E-commerce-API
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the PostgreSQL database**:
    - Create a PostgreSQL database and update the `DATABASES` setting in `settings.py` with your database credentials.

5. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Authentication

- **POST** `/api/customer/verification-code` - Create an OTP.
- **POST** `/api/customer/validate-verification-code` - Login with phone OTP.
- **POST** `/api/customer/token/refresh` - Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.


### Products

- **GET** `/api/products/` - List all products.
- **POST** `/api/products/` - Create a new product.
- **GET** `/api/products/{id}/` - Retrieve a product by ID.
- **PUT** `/api/products/{id}/` - Update a product by ID.
- **DELETE** `/api/products/{id}/` - Delete a product by ID.

### Wishlist

- **GET** `/api/wishlist/` - List all wishlist items.
- **POST** `/api/wishlist/` - Add a product to the wishlist.
- **DELETE** `/api/wishlist/{id}/` - Remove a product from the wishlist.

### Orders

- **GET** `/api/order/` - List all orders.
- **POST** `/api/order/create-order/` - Create a new order.
- **GET** `/api/order/{id}/` - Retrieve an order by ID.
- **PUT** `/api/order/status/{id}` - Update Status of an order by ID.
- **PUT** `/api/order/cancel-order/{id}/` - Cancel an order by ID.

## API Documentation

The API documentation is generated using drf-spectacular and can be accessed at `/api/schema/` and `/api/schema/docs`.


## Contact

For any inquiries, please contact ashmilk114@gmail.com

---

Happy coding! 🚀
