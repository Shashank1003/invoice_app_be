from app.entities.invoices_entity import InvoiceListEntity, InvoiceEntity
from app.common.utils import Utils
from app.adapters.database import db_session
from app.common.exceptions import BadRequestError, ServerError


class InvoicesService:
    def fetch_all_invoices(self):
        invoices_entity = InvoiceListEntity.get_all_invoices()
        return invoices_entity

    def fetch_invoice_by_id(self, invoice_id):
        invoice_entity = InvoiceEntity.get_invoice(invoice_id)
        return invoice_entity

    def create_invoice(self, request):
        due_date = Utils.generate_due_date(
            invoice_date=request.invoice_date, payment_terms=request.payment_terms
        )
        total = Utils.calculate_total(items=request.items)
        modified_request = request.copy(update={"due_date": due_date, "total": total})
        if db_session.in_transaction():
            db_session.rollback()
        try:
            with db_session.begin():

                invoice_created = InvoiceEntity.create_invoice(modified_request.dict())
                if invoice_created:
                    items_created = InvoiceEntity.create_invoice_items(
                        items=request.items, invoice_id=invoice_created.id
                    )
                    invoice_created.items.extend(items_created)
                    return invoice_created
        except Exception as e:
            db_session.rollback()
            print(e)
            raise ServerError()

    def update_invoice(self, invoice_id, request):
        existing_invoice = InvoiceEntity.get_invoice_by_id(invoice_id=invoice_id)
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
        if db_session.in_transaction():
            db_session.rollback()
        try:
            with db_session.begin():
                updated_invoice = InvoiceEntity.update_invoice(
                    request=modified_request.dict()
                )
                InvoiceEntity.delete_invoice_items(invoice_id=invoice_id)
                items_created = InvoiceEntity.create_invoice_items(
                    items=request.items, invoice_id=invoice_id
                )

                if updated_invoice:
                    updated_invoice.items.extend(items_created)
                    return updated_invoice
        except Exception as e:
            db_session.rollback()
            print(e)
            raise ServerError()

    def delete_invoice(self, invoice_id):
        existing_invoice = InvoiceEntity.get_invoice_by_id(invoice_id=invoice_id)
        if existing_invoice is None:
            raise BadRequestError(
                status_code=404, detail=f"invoice with id {invoice_id} not found!"
            )

        if db_session.in_transaction():
            db_session.rollback()
        try:
            with db_session.begin():
                InvoiceEntity.delete_invoice_items(invoice_id=invoice_id)
                InvoiceEntity.delete_invoice(invoice_id=invoice_id)
                return True
        except Exception as e:
            db_session.rollback()
            print(e)
            raise ServerError()
