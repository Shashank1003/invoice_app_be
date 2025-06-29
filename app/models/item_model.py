from sqlalchemy import Column, Float, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ._utils import ResourceMixin


class Item(ResourceMixin):  # you can skip (ResourceMixin, Base) and do (ResourceMixin)
    # as Base is already passed in ResourceMixin
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
