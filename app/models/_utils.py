"""
Here you will find the core models and abstract functions
which will be acting as a abstract base extract class, following the
Model Inheritance
"""

from typing import Any, Dict, List, Self

from sqlalchemy import Boolean, Column, DateTime, func, true
from sqlalchemy.ext.asyncio import AsyncSession

# from app.adapters.database import Base, db_session
from sqlalchemy.orm import DeclarativeBase, class_mapper


class Base(DeclarativeBase):
    pass


class ResourceMixin(Base):
    """A base abstract class model
    :param DateTime 'created_on': Datetime created default to server
    :param DateTime 'updated_on': Datetime updated default to server
    :param Boolean 'active': Whether the instance is active,
    if not it should be considered as Marked for deletion
    """

    __abstract__ = True

    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
    )
    active = Column(Boolean(), server_default=true(), nullable=False)

    async def create(self, db: AsyncSession) -> Self:
        """Save a model Instance to the database
        :return: self
        """
        db.add(self)
        await db.flush()  # INSERT but no commit yet
        await db.refresh(self)
        return self

    async def update(self, db: AsyncSession, **kwargs: Any) -> Self:
        """
        Update the model Instance
        :param kwargs: Attributes
        :return: db_session.commit()'s result
        """

        for attr, value in iter(kwargs.items()):
            setattr(self, attr, value)
        await db.flush()
        await db.refresh(self)
        return self

    async def delete(self, db: AsyncSession, force_delete: bool = False) -> bool:
        """
        Delete a model instance.
        :return: db_session.commit()'s result
        """

        if force_delete is True:
            await db.delete(self)
        else:
            setattr(self, "active", False)  # noqa: B010
        await db.flush()
        return True

    @classmethod
    async def create_bulk(
        cls, db: AsyncSession, bulk_data: List[Dict[str, Any]]
    ) -> None:

        mapper = class_mapper(cls)
        await db.run_sync(
            lambda sync_db: sync_db.bulk_insert_mappings(mapper, bulk_data)
        )
        return

    @classmethod
    async def update_bulk(
        cls, db: AsyncSession, bulk_data: List[Dict[str, Any]]
    ) -> None:
        mapper = class_mapper(cls)
        await db.run_sync(
            lambda sync_db: sync_db.bulk_update_mappings(mapper, bulk_data)
        )
        return
