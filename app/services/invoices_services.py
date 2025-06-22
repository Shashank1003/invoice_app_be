from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequestError, ServerError
from app.common.helper_functions import exception_wrapper
from app.common.utils import Utils
from app.entities.invoices_entity import InvoiceEntity, InvoiceListEntity
from app.schemas.invoice_schema import InvoiceInputSchema, InvoiceUpdateSchema


class InvoicesService:
    @exception_wrapper
    async def fetch_all_invoices(self, db: AsyncSession) -> List[InvoiceListEntity]:
        invoices_entity = await InvoiceListEntity.get_all_invoices(db=db)
        return invoices_entity

    @exception_wrapper
    async def fetch_invoice_by_id(
        self, db: AsyncSession, invoice_id: UUID
    ) -> InvoiceEntity:
        invoice_entity = await InvoiceEntity.get_invoice(db=db, invoice_id=invoice_id)
        return invoice_entity

    @exception_wrapper
    async def create_invoice(
        self, db: AsyncSession, request: InvoiceInputSchema
    ) -> Optional[InvoiceEntity]:
        due_date = Utils.generate_due_date(
            invoice_date=request.invoice_date, payment_terms=request.payment_terms
        )
        total = Utils.calculate_total(items=request.items)
        modified_request = request.copy(
            update={
                "due_date": due_date,
                "total": total,
            }
        )
        invoice_created = await InvoiceEntity.create_invoice(
            request=modified_request.dict(), db=db
        )
        if invoice_created and invoice_created.id:
            items_created = await InvoiceEntity.create_invoice_items(
                db=db, items=request.items, invoice_id=invoice_created.id
            )
            invoice_created.items.extend(items_created)
            return invoice_created
        raise ServerError()

    @exception_wrapper
    async def update_invoice(
        self, db: AsyncSession, invoice_id: UUID, request: InvoiceUpdateSchema
    ) -> Optional[InvoiceEntity]:
        existing_invoice = await InvoiceEntity.get_invoice_by_id(
            db=db, invoice_id=invoice_id
        )
        if existing_invoice is None:
            raise BadRequestError(
                status_code=404, detail=f"invoice with id {invoice_id} not found!"
            )
        new_due_date = Utils.generate_due_date(
            invoice_date=request.invoice_date, payment_terms=request.payment_terms
        )
        new_total = Utils.calculate_total(items=request.items)
        modified_request = request.copy(
            update={"due_date": new_due_date, "total": new_total, "id": invoice_id}
        )
        updated_invoice = await InvoiceEntity.update_invoice(
            db=db, request=modified_request.dict()
        )
        await InvoiceEntity.delete_invoice_items(db=db, invoice_id=invoice_id)
        items_created = await InvoiceEntity.create_invoice_items(
            db=db, items=request.items, invoice_id=invoice_id
        )
        if updated_invoice:
            updated_invoice.items.extend(items_created)
            return updated_invoice
        raise ServerError()

    @exception_wrapper
    async def delete_invoice(self, db: AsyncSession, invoice_id: UUID) -> bool:
        existing_invoice = await InvoiceEntity.get_invoice_by_id(
            db=db, invoice_id=invoice_id
        )
        if existing_invoice is None:
            raise BadRequestError(
                status_code=404, detail=f"invoice with id {invoice_id} not found!"
            )
        await InvoiceEntity.delete_invoice_items(db=db, invoice_id=invoice_id)
        await InvoiceEntity.delete_invoice(db=db, invoice_id=invoice_id)
        return True
