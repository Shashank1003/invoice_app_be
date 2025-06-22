import datetime

from sqlalchemy import Column, Date, Float, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

from app.adapters.database.core import Base
from app.common.enums import PaymentTermsEnum, StatusEnum

from ._utils import ResourceMixin


class Invoice(ResourceMixin, Base):
    __tablename__ = "invoices"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=text("uuid_generate_v4()"),
        unique=True,
        index=True,
        nullable=False,
    )
    # keeping due_date as nullable as it will be handled by BE
    # We will receive due days in the form of payment terms
    due_date = Column(Date, unique=False, index=True, nullable=True)
    client_name = Column(String, unique=False, nullable=False, index=True)
    client_email = Column(String, unique=False, nullable=False, index=True)
    street_from = Column(String, unique=False, nullable=False, index=False)
    street_to = Column(String, unique=False, nullable=False, index=False)
    city_from = Column(String, unique=False, nullable=False, index=False)
    city_to = Column(String, unique=False, nullable=False, index=False)
    postcode_from = Column(String, unique=False, nullable=False, index=False)
    postcode_to = Column(String, unique=False, nullable=False, index=False)
    country_from = Column(String, unique=False, nullable=False, index=True)
    country_to = Column(String, unique=False, nullable=False, index=True)
    invoice_date = Column(
        Date, default=datetime.date.today, unique=False, index=True, nullable=False
    )
    status = Column(Enum(StatusEnum), nullable=False, unique=False, index=True)
    payment_terms = Column(
        Enum(PaymentTermsEnum), nullable=False, unique=False, index=True
    )
    description = Column(String, unique=False, nullable=False, index=False)
    total = Column(Float, unique=False, nullable=False, index=True)

    items = relationship("Item", back_populates="invoice", cascade="all, delete-orphan")
