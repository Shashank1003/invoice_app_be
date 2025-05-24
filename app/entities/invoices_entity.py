from dataclasses import dataclass
from uuid import UUID
from datetime import date
from app.common.enums import StatusEnum, PaymentTermsEnum
from app.queries.invoices_queries import InvoicesQuery

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