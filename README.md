# 📦 URL Shortener API
* A simple URL Shortening service built with FastAPI.
* It provides endpoints to create short-links, redirect to original URLs.

## 🔧 Features
* Create short codes for long URLs.
* Redirect using the short codes.
* User registration and authentication(JWT).
* Basic admin routes for analytics and management.
* Uses SQLAlchemy(SQLite/PostgreSQL) for persistance.
* CRUD support, input validation using Pydantic schemas.

### Getting Started

Prerequisites

'''python
    python 3.12 -m venv fastapienv
    source fastapi/bin/activate
    pip install -r requirements.txt
'''

Configuration