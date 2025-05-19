import uuid
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from app.adapters.database import Base
from ._utils import ResourceMixin

class Item(ResourceMixin, Base):
  __tablename__ = "items"
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
  name= Column(String, unique=False, index=True, nullable=False)
  price = Column(Float, unique=False, index=False, nullable=False)
  quantity = Column(Integer, unique=False, index=False, nullable=False)
  total =Column(Float, unique=False, index=False, nullable=False)