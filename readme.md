# 🧾 Invoice App - FastAPI

A simple and efficient invoice management system built with **FastAPI**. This application provides RESTful APIs to create, retrieve, update, and delete invoices and items.

---

## 🚀 Features

- 📄 Create, Read, Update, Delete (CRUD) operations for invoices
- 📦 JSON-based API responses
- 🛡️ FastAPI validation with Pydantic
- 📚 Interactive Swagger UI & Redoc documentation
- 🐘 PostgreSQL database integration (via SQLAlchemy)
- 📦 Docker support
- 🔐 JWT-based authentication (optional) : TODO

---

## ✅ Prerequisites

- 🐳 [Docker](https://docs.docker.com/get-docker/) installed
- 📦 [Docker Compose](https://docs.docker.com/compose/install/) installed

---

## 🛠️ Installation

1.  **Clone the repo**

    ```bash
    git clone git@github.com:Shashank1003/invoice_app_be.git
    cd invoice_app
    ```

2.  **Setup virtual env**

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

    - On Windows use

    ```bash
    venv\Scripts\activate
    ```

3.  **_Install dependencies_**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set environment variables**
    Create a .env file in the root directory.
    Use env.EXAMPLE to set env variables

5.  **Run migrations**

    ```bash
    alembic upgrade head
    ```

6.  **Run the application**

    ```bash
    uvicorn manage:app --reload
    ```

7.  **Build and start Docker containers**

    ```bash
    docker compose up --build
    ```

    This will:

    - Build your FastAPI app image.
    - Start PostgreSQL database container.
    - Run the app on `http://localhost:8000`.

8.  **Run migrations on Docker**

    ```bash
    docker exec -it invoice_web sh -c "alembic upgrade head"
    ```

9.  **Access the app**

    - API root : `http://localhost:8000/api/v1`
    - Swagger UI docs: `http://localhost:8000/docs/openapi`
    - Redoc UI docs: `http://localhost:8000/docs/redoc`
    - Swagger UI JSON: `http://localhost:8000/docs/openapi.json`

10. **Stop container**
    To stop and remove containers:

    ```bash
    docker compose down
    ```

11. **Notes**
    - Ensure port `5432` and `8000` are free on your machine.
    - Modify `.env` as per your environment (refer to `env.EXAMPLE`).
    - For production deployment, update database hostname and credentials accordingly.

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

```

```
