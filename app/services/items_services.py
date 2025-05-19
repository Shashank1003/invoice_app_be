from app.entities.items_entity import ItemsEntity
from app.schemas.item_schema import ItemOutputSchema
from app.queries.items_queries import ItemsQuery

import logging

logger = logging.getLogger(__name__)

class ItemsService:
  
  @staticmethod
  def fetch_all_items() -> list[ItemsEntity]:
    items = ItemsQuery.fetch_all_items()
    item_entities = [ItemsEntity(**item._mapping) for item in items]
      
    return item_entities
  
  @staticmethod
  def fetch_item_by_id(item_id) :
    item = ItemsQuery.fetch_item_by_id(item_id)
    
    if item is None:
      raise ValueError("Item not found")
    item_entity = ItemsEntity(*item)
    return item_entity  