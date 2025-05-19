from fastapi import APIRouter
from app.schemas.item_schema import ItemOutputSchema
from typing import List
from app.services.items_services import ItemsService
from fastapi.responses import JSONResponse
from uuid import UUID

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

items_router = APIRouter()

@items_router.get(
  "/items",
  summary="items endpoint",
  description="This endpoint returns a list of items",
  response_model= List[ItemOutputSchema]
)
async def get_items():
  """To get all the items"""
  resp = ItemsService.fetch_all_items()
  return resp
  
  
@items_router.get(
  "/items/{item_id}",
  summary="items endpoint",
  description="Get item from item_id",
  response_model= ItemOutputSchema
)
async def get_item(item_id: UUID) :
  """To get item from item_id"""
  resp = ItemsService.fetch_item_by_id(item_id)
  return resp
  