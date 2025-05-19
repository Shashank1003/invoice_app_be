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
      raise Exception("Item not found")
    item_entity = ItemsEntity(*item)
    return item_entity  
  
  @staticmethod
  def create_item(request):
    resp = ItemsQuery.create_item(**request.model_dump())
    if resp is None:
      raise Exception("Item creation failed")
    return ItemsEntity(*resp)
  
  @staticmethod
  def update_item(item_id, request):
    resp = ItemsQuery.update_item(item_id=item_id,
                                  name=request.name,
                                  quantity=request.quantity,
                                  price=request.price,
                                  total=request.total
                                  )
    if resp is None:
      raise Exception("Item update failed")
    return ItemsEntity(*resp)
  
  