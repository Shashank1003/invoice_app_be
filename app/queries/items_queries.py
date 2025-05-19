from sqlalchemy import text
from app.adapters.database import db_session

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
  def fetch_item_by_id(item_id):
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