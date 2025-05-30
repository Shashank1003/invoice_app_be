from dataclasses import dataclass, field
from uuid import UUID
from datetime import date
from app.common.enums import StatusEnum, PaymentTermsEnum
from app.queries.invoices_queries import InvoicesQuery
from app.entities.items_entity import ItemsEntity
from typing import List
from app.queries.items_queries import ItemsQuery
from typing import Optional
from app.common.exceptions import BadRequestError, ServerError


@dataclass
class InvoiceListEntity:
    id: UUID
    due_date: date
    client_name: str
    total: float
    status: StatusEnum

    @classmethod
    def get_all_invoices(cls):
        invoices = InvoicesQuery.fetch_all_invoices()
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
    def get_invoice_by_id(cls, invoice_id: UUID):
        invoice = InvoicesQuery.fetch_invoice_by_id(invoice_id)
        if invoice:
            return cls(**invoice._mapping)
        raise BadRequestError(detail="Invoice not found", status_code=404)

    @classmethod
    def get_invoice(cls, invoice_id: UUID):
        invoice = InvoicesQuery.fetch_invoice(invoice_id)
        if invoice:
            return cls(**invoice._mapping)
        raise BadRequestError(detail="Invoice not found", status_code=404)

    @classmethod
    def create_invoice(cls, request):
        request.pop("items", None)
        invoice = InvoicesQuery.create_invoice(**request)
        if invoice:
            return cls(**invoice._mapping)
        raise ServerError()

    @classmethod
    def create_invoice_items(cls, items, invoice_id):
        items_list = []
        for item in items:
            created_item = ItemsQuery.create_invoice_item(
                **item.dict(), invoice_id=invoice_id
            )
            if created_item:
                items_list.append(ItemsEntity(**created_item._mapping))
            else:
                raise ServerError()
        return items_list

    @classmethod
    def update_invoice(cls, request):
        request.pop("items", None)
        invoice = InvoicesQuery.update_invoice(**request)
        if invoice:
            return cls(**invoice._mapping)
        raise ServerError()

    @classmethod
    def delete_invoice_items(cls, invoice_id):
        ItemsQuery.delete_invoice_items(invoice_id)
        return True

    @classmethod
    def delete_invoice(cls, invoice_id):
        InvoicesQuery.delete_invoice(invoice_id)
        return True
