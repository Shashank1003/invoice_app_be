from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.common.enums import PaymentTermsEnum, StatusEnum
from app.schemas.item_schema import ItemInputSchema


class InvoiceInputSchema(BaseModel):
    due_date: Optional[date] = None
    client_name: str = Field(..., max_length=100)
    client_email: str = Field(..., max_length=100)
    street_from: str = Field(...)
    street_to: str = Field(...)
    city_from: str = Field(..., max_length=100)
    city_to: str = Field(..., max_length=100)
    postcode_from: str = Field(..., max_length=10)
    postcode_to: str = Field(..., max_length=10)
    country_from: str = Field(..., max_length=100)
    country_to: str = Field(..., max_length=100)
    invoice_date: date
    status: StatusEnum
    payment_terms: PaymentTermsEnum
    description: str = Field(...)
    total: Optional[float] = Field(gt=0, default=None)
    items: List[ItemInputSchema]
    # Keeping due_date and total as optional as
    # their value will be calculated by BE itself


class InvoiceOutputSchema(InvoiceInputSchema):
    id: UUID = Field(..., description="identifier for item")


class InvoiceListSchema(BaseModel):
    id: UUID = Field(..., description="identifier for item")
    due_date: date
    client_name: str = Field(..., max_length=100)
    total: float = Field(..., gt=0)
    status: StatusEnum


class InvoiceUpdateSchema(InvoiceInputSchema):
    id: Optional[UUID] = Field(
        default=None, description="identifier for invoice (not required!)"
    )
