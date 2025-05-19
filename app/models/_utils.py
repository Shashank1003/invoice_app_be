"""
Here you will find the core models and abstract functions
which will be acting as a abstract base extract class, following the
Model Inheritance
"""
from typing import Any, Dict, List

from sqlalchemy import Boolean, Column, DateTime, func, true

from app.adapters.database import Base, db_session
from sqlalchemy.orm import class_mapper


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

    def create(self):
        """Save a model Instance to the database
        :return: self
        :except: return error
        """
        try:
            db_session.add(self)
            db_session.commit()
            db_session.refresh(self)
        except Exception as e:
            db_session.rollback()
            raise e
        else:
            return self

    def update(self, **kwargs):
        """
        Update the model Instance
        :param kwargs: Attributes
        :return: db_session.commit()'s result
        """
        try:
            for attr, value in iter(kwargs.items()):
                setattr(self, attr, value)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
        else:
            return self

    def delete(self, force_delete=False):
        """
        Delete a model instance.
        :return: db_session.commit()'s result
        :except: returns error
        """
        try:
            if force_delete is True:
                db_session.delete(self)
            else:
                setattr(self, "active", False)
        except Exception as e:
            db_session.rollback()
            raise e
        else:
            db_session.commit()
            return True

    @classmethod
    def create_bulk(cls, bulk_data: List[Dict[str, Any]]):
        try:
            mapper = class_mapper(cls)
            db_session.bulk_insert_mappings(mapper, bulk_data)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
        else:
            return

    @classmethod
    def update_bulk(cls, bulk_data: List[Dict[str, Any]]):
        try:
            mapper = class_mapper(cls)
            db_session.bulk_update_mappings(mapper, bulk_data)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
        else:
            return
