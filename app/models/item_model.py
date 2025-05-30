from sqlalchemy import Column, String, Integer, Float, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.adapters.database import Base
from ._utils import ResourceMixin
from sqlalchemy.orm import relationship


class Item(ResourceMixin, Base):
    __tablename__ = "items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=text("uuid_generate_v4()"),
        unique=True,
        index=True,
        nullable=False,
    )
    name = Column(String, unique=False, index=True, nullable=False)
    price = Column(Float, unique=False, index=False, nullable=False)
    quantity = Column(Integer, unique=False, index=False, nullable=False)
    total = Column(Float, unique=False, index=False, nullable=False)

    invoice_id = Column(UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False)
    invoice = relationship("Invoice", back_populates="items")
