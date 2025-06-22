import logging
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.common.exceptions import (
    BadRequestError,
    ServerError,
    bad_request_handler,
    server_error_handler,
)

# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Create a stream handler and set formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Get the root logger and configure it
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.handlers.clear()  # Optional: Clear default handlers to avoid duplicates
root_logger.addHandler(handler)

# Optional: configure SQLAlchemy logging
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.DEBUG)

# origins = [
#     "http://localhost:3000",
# ]


def create_app(**kwargs: Any) -> FastAPI:
    app = FastAPI(
        title="invoice app",
        description=(
            "backend for invoice web-app with async function calls "
            "and session injection"
        ),
        version="2.0",
        docs_url="/docs/openapi",
        openapi_url="/docs/openapi.json",
        redoc_url="/docs/redoc",
    )

    app.include_router(api_router, prefix="/api/v2")
    app.add_exception_handler(ServerError, server_error_handler)
    app.add_exception_handler(BadRequestError, bad_request_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
