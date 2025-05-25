from sqlalchemy import text
from app.adapters.database import db_session
from uuid import UUID

class InvoicesQuery:
  @staticmethod
  def fetch_all_invoices():
    result = db_session.execute(
      text(
        """
        SELECT id, due_date, client_name, total, status
        FROM invoices
        """.strip()
      )
    ).fetchall()
    return result
  
  
  @staticmethod
  def fetch_invoice_by_id(invoice_id: UUID):
    result = db_session.execute(
      text(
        """
        SELECT id, due_date, client_name, total, status, street_from,
        street_to, city_from, city_to, country_from, country_to, postcode_from,
        postcode_to, payment_terms, client_email, invoice_date, description
        FROM invoices WHERE id=:invoice_id
        """.strip()
      ), {"invoice_id": invoice_id}
    ).fetchone()
    return result