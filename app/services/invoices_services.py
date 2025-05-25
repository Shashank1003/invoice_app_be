from app.entities.invoices_entity import InvoiceListEntity, InvoiceEntity

class InvoicesService:
  
  def fetch_all_invoices(self):
    invoices_entity = InvoiceListEntity.get_all_invoices()
    return invoices_entity
  
  def fetch_invoice_by_id(self, invoice_id):
    invoice_entity = InvoiceEntity.get_invoice_by_id(invoice_id)
    invoice_items = InvoiceEntity.get_invoice_items(invoice_id)
    if invoice_entity and invoice_items:
      invoice_entity.items.extend(invoice_items)
      return invoice_entity