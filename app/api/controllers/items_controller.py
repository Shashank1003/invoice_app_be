from fastapi import APIRouter
from app.schemas.item_schema import (
    ItemOutputSchema,
    ItemInputSchema,
    ItemUpdateSchema,
    ItemInvoiceInputSchema,
    ItemInvoiceOutputSchema,
)
from typing import List
from app.services.items_services import ItemsService
from uuid import UUID

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

items_router = APIRouter()


@items_router.get(
    path="/items",
    summary="items endpoint",
    description="This endpoint returns a list of items",
    response_model=List[ItemOutputSchema],
)
async def get_items():
    """To get all the items"""
    resp = ItemsService.fetch_all_items()
    return resp


@items_router.get(
    path="/items/{item_id}",
    summary="items endpoint",
    description="Get item from item_id",
    response_model=ItemOutputSchema,
)
async def get_item(item_id: UUID):
    """To get item from item_id"""
    resp = ItemsService.fetch_item_by_id(item_id)
    return resp


@items_router.post(
    path="/items",
    summary="Create item",
    description="Create a new item",
    response_model=ItemInvoiceOutputSchema,
)
async def create_item(request: ItemInvoiceInputSchema):
    """To create a new item"""
    resp = ItemsService.create_item(request)
    return resp


@items_router.put(
    path="/items/{item_id}",
    summary="Update item",
    description="Update an existing item",
    response_model=ItemOutputSchema,
)
async def update_item(item_id: UUID, request: ItemUpdateSchema):
    resp = ItemsService.update_item(item_id, request)
    return resp


@items_router.delete(
    path="/items/{item_id}",
    summary="Delete item",
    description="Delete an existing item by id",
)
async def delete_item(item_id: UUID):
    resp = ItemsService.delete_item(item_id)
    return resp
