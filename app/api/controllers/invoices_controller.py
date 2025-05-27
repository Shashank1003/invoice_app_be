from fastapi import APIRouter, Request
from typing import List
from uuid import UUID
from app.common.exceptions import BadRequestError, ServerError
from app.schemas.invoice_schema import InvoiceListSchema,InvoiceInputSchema,InvoiceOutputSchema
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
async def create_invoice( request: InvoiceInputSchema):
  invoice = InvoicesService(invoice_date=request.invoice_date,
                            payment_terms=request.payment_terms,
                            items=request.items
                            ).create_invoice(request)
  return invoice