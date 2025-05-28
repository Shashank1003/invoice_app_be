# 🧾 Invoice App - FastAPI

A simple and efficient invoice management system built with **FastAPI**. This application provides RESTful APIs to create, retrieve, update, and delete invoices and items.

---

## 🚀 Features

- 📄 Create, Read, Update, Delete (CRUD) operations for invoices
- 📦 JSON-based API responses
- 🛡️ FastAPI validation with Pydantic
- 📚 Interactive Swagger UI & Redoc documentation
- 🐘 PostgreSQL database integration (via SQLAlchemy)
- 🔐 JWT-based authentication (optional)  : TODO
- 📦 Docker support (optional) : TODO

---

## 🛠️ Installation

1. **Clone the repo**

    ```bash
    git clone git@github.com:Shashank1003/invoice_app_be.git
    cd invoice_app
    ```

2. **Setup virtual env**

    `python -m venv venv
    source venv/bin/activate`

    - On Windows use `venv\Scripts\activate`

3. ***Install dependencies***
    `pip install -r requirements.txt`

4. **Set environment variables**
    Create a .env file in the root directory.
    Use env.EXAMPLE to set env variables

5. **Run the application**
    `uvicorn manage:app --reload`

---

## 📸 Sample API Endpoints

- POST /invoices/ - Create a new invoice

- GET /invoices/{id} - Get invoice by ID

- GET /invoices/ - List all invoices

- PUT /invoices/{id} - Update invoice

- DELETE /invoices/{id} - Delete invoice

- POST /items/ - Create a new item

- GET /items/{id} - Get item by ID

- GET /items/ - List all items

- PUT /items/{id} - Update item

- DELETE /items/{id} - Delete item

---

## 👨‍💻 Author

Shashank Gupta – @Shashank1003 | <guptashashank8975@gmail.com>

---
