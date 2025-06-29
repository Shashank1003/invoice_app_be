# 🧾 Invoice App - FastAPI (v2.0)

A modern, async-first invoice management system built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. This application provides RESTful APIs to create, retrieve, update, and delete invoices and items.

---

## 🚀 Features

- ✅ Fully Async backend with AsyncSession for non-blocking performance
- ⚛️ Dependency injection for cleaner session management
- ♻️ Modular, layered architecture using Entities, Services, Schemas, and Controllers
- 🔁 RESTful CRUD APIs for Invoices and Items
- ⚡ Robust validation via Pydantic
- 🌐 Interactive Swagger & Redoc documentation
- 🛠️ Docker & PostgreSQL integration
- 🔒 JWT-based auth (TODO)
- ✈️ Dev tooling with pre-commit, mypy, black, isort, flake8

---

## ✅ Prerequisites

- 🐳 [Docker](https://docs.docker.com/get-docker/) installed
- 📦 [Docker Compose](https://docs.docker.com/compose/install/) installed
- 🐍 Python 3.11+

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

8.  **Run migrations inside Docker**

    ```bash
    docker exec -it invoice_web sh -c "alembic upgrade head"
    ```

9.  **Access the app**

    - API root : `http://localhost:8000/api/v2`
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

## 📖 Dev Experience Boosts

- 👩‍💼 Async + Dependency Injection

  - All DB operations use async def with AsyncSession
  - Safe session lifecycle with Depends(get_db)

- 🔎 Type Hints + Static Analysis

  - Strong typing via Pydantic, Literal, UUID, etc.
  - mypy ensures type safety across the codebase

- ↻ Pre-commit Hook Configuration

  - `.pre-commit-config.yaml` includes:
  - `black`
  - `isort`
  - `mypy`
  - `flake8` (with bugbear)

  - Manually run with:
    ```bash
    pre-commit run --all-files
    ```

- 👋 Friendly Errors & Log

  - Centralized BadRequestError and ServerError
  - Custom exception wrapper decorators
  - SQL query logging using sqlalchemy.engine

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

## 🧹 Tech Stack

- 🐍 Backend: FastAPI, SQLAlchemy (async), Alembic
- 🐃 Database: PostgreSQL
- 🚧 Containerization: Docker, Docker Compose
- 🔧 Dev Tools: Black, isort, mypy, flake8, pre-commit

---

## 📊 Future Improvements (TODO)

- JWT Auth
- Pagination & Filtering
- User Roles
- CI/CD Integration
- Unit & Integration Tests

---

## 👨‍💻 Author

Shashank Gupta – @Shashank1003 | <guptashashank8975@gmail.com>

---

> ✨ Built with passion and async love!
