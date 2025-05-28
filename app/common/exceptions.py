from dataclasses import dataclass
from typing import Any, Optional

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse


@dataclass
class ServerError(Exception):
    status_code: int = 500
    detail: str = "It ain't you, it is me"


@dataclass
class BadRequestError(RequestValidationError):
    status_code: int
    detail: Any


async def server_error_handler(request: Request, exc) -> JSONResponse:
    """
    5xx Server Error Handler
    :param request: Incoming Api request
    :type request: Request
    :param exc: Server error Exception
    :type exc: ServerError
    :return: Json response with status code and message
    :rtype: JSONResponse
    """
    return JSONResponse(
        status_code=500, content={"message": exc.detail, "status": exc.status_code}
    )


async def bad_request_handler(request: Request, exc) -> JSONResponse:
    """
    4xx Bad Request Handler Server Error Handler
    :param request: Incoming Api request
    :type request: Request
    :param exc: BadRequestError error inherits RequestValidationError
    :type exc: BadRequestError
    :return: Json response with status code and message
    :rtype: JSONResponse
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": exc.status_code},
    )
