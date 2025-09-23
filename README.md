# Savannah Backend

**Savannah Backend** is a Django-based REST API and web application backend that handles user authentication, product and category management, and customer profiles.

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Running the App](#running-the-app)  
- [Testing](#testing)  
- [API Endpoints](#api-endpoints)  
---

## Features

- JWT-based authentication with Django REST framework  
- Google OAuth2 login integration  
- Customer profile management  
- Product and category management  
- Recursive category structure with average product price calculation  
- REST API endpoints for frontend consumption  
- Template rendering for product listings  

---

## Tech Stack

- Python 3.11  
- Django 5.x  
- Django REST Framework  
- Django Allauth  
- dj-rest-auth  
- PostgreSQL
- Pytest for testing  

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/rkipchumba/savanna_backend.git
cd savannah_backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

python manage.py createsuperuser
```

## Running the App

```

python manage.py runserver
```

## Testing
```
pytest --cov=customers --cov=products --cov=orders --cov-report=term-missing   
```

## API Endpoints

### Customers / Authentication

- `GET /accounts/login/` - Display login page  
- `POST /accounts/login/` - Submit login credentials  
- `GET /accounts/logout/` - Logout the current user  
- `GET /accounts/signup/` - Display registration page  
- `POST /accounts/signup/` - Submit registration form 

### Google OAuth / Social Login

- `POST /auth/google/` - Social login via Google OAuth2  

### Products

- `GET /api/products/` - List all products  

### Categories

- `GET /api/categories/` - List all categories with products  

### Orders

- `GET /api/orders/` - List all orders  

### Frontend

- `GET /products/` - Render product listing page (HTML template)  
- `GET /orders/` - Render order page (HTML template)  
- `GET /test-sms/` - Test SMS endpoint

