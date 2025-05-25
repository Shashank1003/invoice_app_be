from sqlalchemy import text
from app.adapters.database import db_session
from uuid import UUID

class ItemsQuery:
  @staticmethod
  def fetch_all_items():
    all_items = db_session.execute(
      text(
        """SELECT id, name, quantity, price, total FROM items""".strip()
      )
    ).fetchall()
    return all_items
  
  @staticmethod
  def fetch_item_by_id(item_id: UUID):
    item = db_session.execute(
      text(
        """
        SELECT id, name, quantity, price, total FROM items 
        WHERE id=:item_id
        """.strip()
      ),
      {"item_id": item_id }
    ).fetchone()
    return item
  
  @staticmethod
  def create_item(name:str, quantity: int, price: float, total: float):
    result = db_session.execute(
      text(
        """
        INSERT INTO items (name, quantity, price, total)
        VALUES (:name, :quantity, :price, :total)
        RETURNING id, name, quantity, price, total 
        """.strip()
      ),
      {"name": name,
       "quantity": quantity,
       "price": price,
       "total": total}
    ).fetchone()
    db_session.commit()
    return result
  
  @staticmethod
  def update_item(item_id: UUID,
                  name: str,
                  quantity: int,
                  price: float,
                  total: float
                  ):
    result= db_session.execute(
      text(
        """
        UPDATE items
        SET name=:name,
        quantity=:quantity,
        price=:price,
        total=:total
        WHERE id=:item_id
        RETURNING id, name, quantity, price, total
        """.strip()
      ), {
        "item_id": item_id,
        "name": name,
        "quantity": quantity,
        "price": price,
        "total": total
      }
    ).fetchone()
    db_session.commit()
    return result
  
  @staticmethod
  def delete_item(item_id: UUID):
    db_session.execute(
      text(
        """
        DELETE FROM items
        WHERE id=:item_id
        """.strip()
      ), {"item_id": item_id}
    )
    db_session.commit()
    
  @staticmethod
  def fetch_invoice_items(invoice_id: UUID):
    result = db_session.execute(
      text(
        """
        SELECT id, name, quantity, price, total FROM items 
        WHERE invoice_id=:invoice_id; 
        """.strip()
        ), {"invoice_id": invoice_id}
      ).fetchall()
    return result