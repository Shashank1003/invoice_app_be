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