import logging
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from app.common.exceptions import BadRequestError, ServerError

logger = logging.getLogger(__name__)

P = ParamSpec("P")
R = TypeVar("R")


def exception_wrapper(
    fn: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]:
    @wraps(fn)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await fn(*args, **kwargs)
        except BadRequestError:
            raise
        except SQLAlchemyError as e:
            logger.error(f"SQLAlchemy error: {e}")
            raise ServerError()
        except Exception as e:
            logger.error(f"Unhandled DB error: {e}")
            raise ServerError()

    return wrapper
