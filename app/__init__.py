from typing import Tuple

# from celery import Celery
from fastapi import FastAPI

# from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.api.routes import api_router
from app.common.exceptions import ServerError, BadRequestError, server_error_handler, bad_request_handler

# from app.extensions import configure_sentry_extensions
# from app.middlewares.authorization_middleware import AuthorizationMiddleware
# from app.middlewares.sentry_middleware import SentryMiddleware

"""When you wanna debug , log everything inside application uncomment the below and run"""
# import logging
# logging.basicConfig(level=logging.DEBUG)
# sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
# sqlalchemy_logger.setLevel(logging.DEBUG)

def register_endpoints() -> FastAPI:
    """
    Register API rounter with a new FAST API App instance.

    Returns:
        FastAPI: FastAPI Web API Instance, with resgistered routes.
    """
    # we create the Web API framework
    web_api = FastAPI(
        title="invoice app",
        description="backend for invoice web-app",
        version="1.0",
        root_path="",
        # docs_url=docs_config.DOCS_URL,
        # openapi_url=docs_config.OPENAPI_URL,
        # redoc_url=docs_config.REDOC_URL,
    )

    web_api.include_router(api_router)

    # Configure Middlewares
    # web_api.add_middleware(SentryMiddleware)
    # web_api.add_middleware(SentryAsgiMiddleware)
    # web_api.add_middleware(AuthorizationMiddleware)
    # https://github.com/tiangolo/fastapi/issues/1802
    web_api.add_exception_handler(ServerError, server_error_handler)
    web_api.add_exception_handler(BadRequestError, bad_request_handler)
    return web_api


def create_app(**kwargs) -> FastAPI:
    """
    Application Factory

    Returns:
        FastAPI: Fast API instance
    """
    app: FastAPI = FastAPI(
        title="invoice app",
        description="backend for invoice web-app",
    )

    # Load Endpoints
    web_api = register_endpoints()

    app.mount("/api/v1", app=web_api)

    return app