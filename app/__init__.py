from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.common.exceptions import (
    ServerError,
    BadRequestError,
    server_error_handler,
    bad_request_handler,
)

import logging

logging.basicConfig(level=logging.DEBUG)
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.DEBUG)

# origins = [
#     "http://localhost:3000",
# ]


def create_app(**kwargs) -> FastAPI:
    app = FastAPI(
        title="invoice app",
        description="backend for invoice web-app",
        version="1.0",
        docs_url="/docs/openapi",
        openapi_url="/docs/openapi.json",
        redoc_url="/docs/redoc",
    )

    app.include_router(api_router, prefix="/api/v1")

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
