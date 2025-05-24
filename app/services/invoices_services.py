from app.entities.invoices_entity import InvoiceListEntity

class InvoicesService:
  
  def fetch_all_invoices(self):
    invoices_entity = InvoiceListEntity.get_all_invoices()
    return invoices_entity