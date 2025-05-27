from app.entities.invoices_entity import InvoiceListEntity, InvoiceEntity
from app.common.utils import Utils
from app.common.enums import PaymentTermsEnum
from app.adapters.database import db_session

class InvoicesService:
  def __init__(self,
              invoice_date = None,
              payment_terms = PaymentTermsEnum.ONE,
              items=[]):
    self.invoice_date = invoice_date
    self.payment_terms = payment_terms
    self.items=items
  
  def fetch_all_invoices(self):
    invoices_entity = InvoiceListEntity.get_all_invoices()
    return invoices_entity
  
  def fetch_invoice_by_id(self, invoice_id):
    invoice_entity = InvoiceEntity.get_invoice_by_id(invoice_id)
    invoice_items = InvoiceEntity.get_invoice_items(invoice_id)
    if invoice_entity and invoice_items:
      invoice_entity.items.extend(invoice_items)
      return invoice_entity
    
  def create_invoice(self, request):
    due_date = Utils.generate_due_date(invoice_date=self.invoice_date,
                                      payment_terms=self.payment_terms) 
    total =  Utils.calculate_total(items=self.items)
    request.due_date = due_date
    request.total = total
    try:
      with db_session.begin():
        
        invoice_created = InvoiceEntity.create_invoice(request.dict())
        if invoice_created:
          items_created = InvoiceEntity.create_invoice_items(items=self.items,
                                                      invoice_id=invoice_created.id)
          invoice_created.items.extend(items_created)
          return invoice_created
    except Exception as e:
      db_session.rollback()
      raise e
      