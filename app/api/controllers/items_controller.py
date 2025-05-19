from fastapi import APIRouter, Request
from app.schemas.item_schema import ItemOutputSchema, ItemInputSchema
from typing import List
from app.services.items_services import ItemsService
from uuid import UUID
from app.entities.items_entity import ItemsEntity

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

items_router = APIRouter()

@items_router.get(
  path="/items",
  summary="items endpoint",
  description="This endpoint returns a list of items",
  response_model= List[ItemOutputSchema]
)
async def get_items():
  """To get all the items"""
  resp = ItemsService.fetch_all_items()
  return resp
  
  
@items_router.get(
  path="/items/{item_id}",
  summary="items endpoint",
  description="Get item from item_id",
  response_model= ItemOutputSchema
)
async def get_item(item_id: UUID) :
  """To get item from item_id"""
  resp = ItemsService.fetch_item_by_id(item_id)
  return resp
  

@items_router.post(
  path="/items",
  summary="Create item",
  description="Create a new item",
  response_model= ItemOutputSchema
)
async def create_item(request: ItemInputSchema):
  """To create a new item"""
  print(f"request: {request}")
  resp = ItemsService.create_item(request)
  return resp