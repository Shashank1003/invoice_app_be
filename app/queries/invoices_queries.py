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