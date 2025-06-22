# database/dependencies.py
import logging
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequestError, ServerError

from .core import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except BadRequestError:
            raise
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"SQLAlchemy error: {e}")
            raise ServerError()
        except Exception as e:
            await session.rollback()
            logger.error(f"Unhandled DB error: {e}")
            raise e
