# 📦 URL Shortener API
A simple URL shortening service built with **FastAPI**. It provides endpoints to create short links, redirect to original URLs, and manage users/admins.

## 🔧 Features
* Create short codes for long URLs.
* Redirect using the short codes.
* User registration and authentication(JWT).
* Basic admin routes for analytics and management.
* Uses SQLAlchemy(SQLite/PostgreSQL) for persistance.
* CRUD support, input validation using Pydantic schemas.

## 🚀 Getting Started

### Prerequisites

```bash
    python 3.12 -m venv fastapienv
    source fastapi/bin/activate
    pip install -r [requirements.txt](http://_vscodecontentref_/1)
```

### Configuration

Copy or edit config.py to set database URL, secret keys, etc.

Run the server

```bash
    uvicorn URL_Shortner.main:app --reload
```
Visit `http://127.0.0.1:8000/docs` for the interactive OpenAPI docs.

## 🧱 Project Sturcture
The Tree below is an example of how this repository is organized. Generated with `tree -L 2`.

```text
├── config.py
├── crud.py
├── database.py
├── __init__.py
├── keygen.py
├── main.py
├── models.py
├── __pycache__
│   ├── config.cpython-312.pyc
│   ├── config.cpython-313.pyc
│   ├── crud.cpython-312.pyc
│   ├── crud.cpython-313.pyc
│   ├── database.cpython-312.pyc
│   ├── database.cpython-313.pyc
│   ├── keygen.cpython-312.pyc
│   ├── keygen.cpython-313.pyc
│   ├── main.cpython-312.pyc
│   ├── main.cpython-313.pyc
│   ├── models.cpython-312.pyc
│   ├── models.cpython-313.pyc
│   ├── schemas.cpython-312.pyc
│   └── schemas.cpython-313.pyc
├── README.md
├── router
│   ├── admin.py
│   ├── auth.py
│   ├── __init__.py
│   ├── __pycache__
│   └── user.py
├── schemas.py
└── shortner.db
```
* **Note:** `__pycache__` and the local `shortner.db` files are typically not committed to Git. Add them to `gitignore` if needed.

## Usage

- **POST** `/auth/register` – create user
- **POST** `/auth/login` – obtain access token
- **POST** `/user/shorten` – supply `{ "url": "https://..." }`
- **GET** `/{shortcode}` – redirect to original link
- **GET** `/admin/...` – admin-only endpoints(These are incomplete but they will be updated).

## Author
Phenesin (https://github.com/Phenesin)
