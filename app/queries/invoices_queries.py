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
  
  @staticmethod
  def fetch_invoice(invoice_id: UUID):
    result = db_session.execute(
      text("""
        SELECT 
            i.id,
            i.due_date,
            i.client_name,
            i.total,
            i.status,
            i.street_from,
            i.street_to,
            i.city_from,
            i.city_to,
            i.country_from,
            i.country_to,
            i.postcode_from,
            i.postcode_to,
            i.client_email,
            i.invoice_date,
            i.payment_terms,
            i.description,
            COALESCE(json_agg(
                json_build_object(
                    'id', it.id,
                    'invoice_id', it.invoice_id,
                    'name', it.name,
                    'quantity', it.quantity,
                    'price', it.price,
                    'total', it.total
                )
            ) FILTER (WHERE it.id IS NOT NULL), '[]') AS items
        FROM invoices i
        LEFT JOIN items it ON i.id = it.invoice_id
        WHERE i.id = :invoice_id
        GROUP BY i.id
    """.strip()
    ), {"invoice_id": invoice_id}
    ).fetchone()
    return result
  
  
  @staticmethod
  def create_invoice(due_date, client_name, total, status, street_from,
                    street_to, city_from, city_to, country_from, country_to,
                    postcode_from, postcode_to, client_email, invoice_date, 
                    payment_terms, description):
    status = status.value
    payment_terms = payment_terms.value
    result = db_session.execute(
      text("""
          INSERT INTO invoices (due_date, client_name, total, status, street_from,
          street_to, city_from, city_to, country_from, country_to,
          postcode_from, postcode_to, client_email, invoice_date, 
          payment_terms, description)
          VALUES (:due_date, :client_name, :total, :status, :street_from,
          :street_to, :city_from, :city_to, :country_from, :country_to,
          :postcode_from, :postcode_to, :client_email, :invoice_date, 
          :payment_terms, :description)
          RETURNING due_date, client_name, total, status, street_from,
          street_to, city_from, city_to, country_from, country_to,
          postcode_from, postcode_to, client_email, invoice_date, 
          payment_terms, description, id
          """.strip()
          ),{
            "due_date": due_date,
            "client_name": client_name,
            "total": total,
            "status": status,
            "street_from": street_from,
            "street_to": street_to,
            "city_from": city_from,
            "city_to": city_to,
            "country_from": country_from,
            "country_to": country_to,
            "postcode_from": postcode_from,
            "postcode_to": postcode_to,
            "client_email": client_email,
            "invoice_date": invoice_date, 
            "payment_terms": payment_terms,
            "description": description
          }
    ).fetchone()
    # don't use db-commit here as running this action in transaction.
    return result
  
  @staticmethod
  def update_invoice(due_date, client_name, total, status, street_from,
                    street_to, city_from, city_to, country_from, country_to,
                    postcode_from, postcode_to, client_email, invoice_date, 
                    payment_terms, description, id):
    status = status.value
    payment_terms = payment_terms.value
    result = db_session.execute(
      text("""
          UPDATE invoices SET due_date=:due_date, client_name=:client_name, 
          total=:total, status=:status, street_from=:street_from, 
          street_to=:street_to, city_from=:city_from, city_to=:city_to, 
          country_from=:country_from, country_to=:country_to, postcode_from=:postcode_from, 
          postcode_to=:postcode_to, client_email=:client_email, invoice_date=:invoice_date, 
          payment_terms=:payment_terms, description=:description WHERE id = :id 
          RETURNING due_date, client_name, total, status, street_from, street_to, city_from, 
          city_to, country_from, country_to, postcode_from, postcode_to, client_email, 
          invoice_date, payment_terms, description, id;
          """.strip()),{
            "due_date": due_date,
            "client_name": client_name,
            "total": total,
            "status": status,
            "street_from": street_from,
            "street_to": street_to,
            "city_from": city_from,
            "city_to": city_to,
            "country_from": country_from,
            "country_to": country_to,
            "postcode_from": postcode_from,
            "postcode_to": postcode_to,
            "client_email": client_email,
            "invoice_date": invoice_date, 
            "payment_terms": payment_terms,
            "description": description,
            "id": id
            }
    ).fetchone()
    # don't use db-commit here as running this action in transaction.
    return result
  
  @staticmethod
  def delete_invoice(invoice_id):
    db_session.execute(
      text(
        """
        DELETE FROM invoices WHERE id=:invoice_id
        """.strip()
      ),{"invoice_id": invoice_id}
    )
    # don't use db-commit here as running this action in transaction.
    return True
