from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PaymentTermsEnum, StatusEnum
from app.common.exceptions import BadRequestError, ServerError
from app.entities.items_entity import ItemsEntity
from app.queries.invoices_queries import InvoicesQuery
from app.queries.items_queries import ItemsQuery
from app.schemas.item_schema import ItemInputSchema

# from fastapi import HTTPException


@dataclass
class InvoiceListEntity:
    id: UUID
    due_date: date
    client_name: str
    total: float
    status: StatusEnum

    @classmethod
    async def get_all_invoices(cls, db: AsyncSession) -> List["InvoiceListEntity"]:
        invoices = await InvoicesQuery.fetch_all_invoices(db)
        return [cls(**invoice._mapping) for invoice in invoices]

    # info: use cls(**invoice._mapping) instead of cls(*invoice)
    # as cls(*invoice) needs args in exact order while cls(**invoice._mapping)
    # allows args to be in any order (keyword args)


@dataclass
class InvoiceEntity:
    due_date: date
    client_name: str
    total: float
    status: StatusEnum
    street_from: str
    street_to: str
    payment_terms: PaymentTermsEnum
    city_from: str
    city_to: str
    postcode_from: str
    postcode_to: str
    country_from: str
    country_to: str
    client_email: str
    invoice_date: date
    description: str
    items: List[ItemsEntity] = field(default_factory=list)
    id: Optional[UUID] = None

    @classmethod
    async def get_invoice_by_id(
        cls, db: AsyncSession, invoice_id: UUID
    ) -> "InvoiceEntity":
        invoice = await InvoicesQuery.fetch_invoice_by_id(db=db, invoice_id=invoice_id)
        if invoice:
            return cls(**invoice._mapping)
        raise BadRequestError(detail="Invoice not found", status_code=404)

    @classmethod
    async def get_invoice(cls, db: AsyncSession, invoice_id: UUID) -> "InvoiceEntity":
        invoice = await InvoicesQuery.fetch_invoice(invoice_id=invoice_id, db=db)
        if invoice:
            return cls(**invoice._mapping)
        raise BadRequestError(detail="Invoice not found", status_code=404)

    @classmethod
    async def create_invoice(
        cls, db: AsyncSession, request: Dict[str, Any]
    ) -> "InvoiceEntity":
        request.pop("items", None)

        invoice = await InvoicesQuery.create_invoice(**request, db=db)
        if invoice:
            return cls(**invoice._mapping)
        raise ServerError()

    @classmethod
    async def create_invoice_items(
        cls, items: List[ItemInputSchema], invoice_id: UUID, db: AsyncSession
    ) -> List[ItemsEntity]:
        items_list = []
        for item in items:
            created_item = await ItemsQuery.create_invoice_item(
                **item.dict(), invoice_id=invoice_id, db=db
            )
            if created_item:
                items_list.append(ItemsEntity(**created_item._mapping))
            else:
                raise ServerError()
        return items_list

    @classmethod
    async def update_invoice(
        cls, db: AsyncSession, request: Dict[str, Any]
    ) -> "InvoiceEntity":
        request.pop("items", None)
        invoice = await InvoicesQuery.update_invoice(**request, db=db)
        if invoice:
            return cls(**invoice._mapping)
        raise ServerError()

    @classmethod
    async def delete_invoice_items(cls, invoice_id: UUID, db: AsyncSession) -> bool:
        await ItemsQuery.delete_invoice_items(invoice_id=invoice_id, db=db)
        return True

    @classmethod
    async def delete_invoice(cls, db: AsyncSession, invoice_id: UUID) -> bool:
        await InvoicesQuery.delete_invoice(invoice_id=invoice_id, db=db)
        return True
