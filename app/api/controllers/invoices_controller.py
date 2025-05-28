from fastapi import APIRouter, Request
from typing import List
from uuid import UUID
from app.schemas.invoice_schema import (
    InvoiceListSchema,
    InvoiceInputSchema,
    InvoiceOutputSchema,
    InvoiceUpdateSchema,
)
from app.services.invoices_services import InvoicesService

invoices_router = APIRouter()


@invoices_router.get(
    path="/invoices",
    summary="invoices endpoint",
    description="This endpoint returns a list of items",
    response_model=List[InvoiceListSchema],
)
async def get_invoices():
    """To get all the invoices"""
    invoices_list = InvoicesService().fetch_all_invoices()
    return invoices_list


@invoices_router.get(
    path="/invoices/{invoice_id}",
    summary="invoices endpoint",
    description="This endpoint returns a single invoice",
    response_model=InvoiceOutputSchema,
)
async def get_invoice(invoice_id: UUID):
    invoice = InvoicesService().fetch_invoice_by_id(invoice_id)
    return invoice


@invoices_router.post(
    path="/invoices",
    summary="invoices endpoint",
    description="This endpoint creates a new invoice",
    response_model=InvoiceOutputSchema,
)
async def create_invoice(request: InvoiceInputSchema):
    invoice_service = InvoicesService()
    invoice = invoice_service.create_invoice(request)
    return invoice


@invoices_router.put(
    path="/invoices/{invoice_id}",
    summary="invoices endpoint",
    description="This endpoint updates a single invoice and associated items",
    response_model=InvoiceOutputSchema,
)
async def update_invoice(invoice_id: UUID, request: InvoiceUpdateSchema):
    invoice_service = InvoicesService()
    updated_invoice = invoice_service.update_invoice(
        invoice_id=invoice_id, request=request
    )
    return updated_invoice


@invoices_router.delete(
    path="/invoices/{invoice_id}",
    summary="invoices endpoint",
    description="This endpoint deletes a single invoice",
)
async def delete_invoice(invoice_id: UUID):
    invoice_service = InvoicesService()
    resp = invoice_service.delete_invoice(invoice_id=invoice_id)
    return resp
