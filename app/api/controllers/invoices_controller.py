from dataclasses import asdict
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.dependencies import get_db
from app.common.exceptions import BadRequestError
from app.schemas.invoice_schema import (
    InvoiceInputSchema,
    InvoiceListSchema,
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
async def get_invoices(db: AsyncSession = Depends(get_db)) -> List[InvoiceListSchema]:
    """To get all the invoices"""
    invoice_service = InvoicesService()
    invoices_list = await invoice_service.fetch_all_invoices(db)
    return [InvoiceListSchema.model_validate(asdict(i)) for i in invoices_list]


@invoices_router.get(
    path="/invoices/{invoice_id}",
    summary="invoices endpoint",
    description="This endpoint returns a single invoice",
    response_model=InvoiceOutputSchema,
)
async def get_invoice(
    invoice_id: UUID, db: AsyncSession = Depends(get_db)
) -> InvoiceOutputSchema:
    invoice = await InvoicesService().fetch_invoice_by_id(invoice_id=invoice_id, db=db)
    return InvoiceOutputSchema.model_validate(asdict(invoice))


@invoices_router.post(
    path="/invoices",
    summary="invoices endpoint",
    description="This endpoint creates a new invoice",
    response_model=InvoiceOutputSchema,
)
async def create_invoice(
    request: InvoiceInputSchema, db: AsyncSession = Depends(get_db)
) -> InvoiceOutputSchema:
    invoice = await InvoicesService().create_invoice(request=request, db=db)
    if invoice is None:
        raise BadRequestError(detail="Failed to create invoice", status_code=500)
    return InvoiceOutputSchema.model_validate(asdict(invoice))


@invoices_router.put(
    path="/invoices/{invoice_id}",
    summary="invoices endpoint",
    description="This endpoint updates a single invoice and associated items",
    response_model=InvoiceOutputSchema,
)
async def update_invoice(
    invoice_id: UUID, request: InvoiceUpdateSchema, db: AsyncSession = Depends(get_db)
) -> InvoiceOutputSchema:
    updated_invoice = await InvoicesService().update_invoice(
        invoice_id=invoice_id, request=request, db=db
    )
    if updated_invoice is None:
        raise BadRequestError(detail="Failed to update invoice", status_code=500)
    return InvoiceOutputSchema.model_validate(asdict(updated_invoice))


@invoices_router.delete(
    path="/invoices/{invoice_id}",
    summary="invoices endpoint",
    description="This endpoint deletes a single invoice",
    response_model=bool,
)
async def delete_invoice(invoice_id: UUID, db: AsyncSession = Depends(get_db)) -> bool:
    resp = await InvoicesService().delete_invoice(invoice_id=invoice_id, db=db)
    return resp
