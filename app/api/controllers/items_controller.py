import logging
from dataclasses import asdict
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.database.dependencies import get_db
from app.schemas.item_schema import (
    ItemInvoiceInputSchema,
    ItemInvoiceOutputSchema,
    ItemOutputSchema,
    ItemUpdateSchema,
)
from app.services.items_services import ItemsService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

items_router = APIRouter()


@items_router.get(
    path="/items",
    summary="items endpoint",
    description="This endpoint returns a list of items",
    response_model=List[ItemOutputSchema],
)
async def get_items(db: AsyncSession = Depends(get_db)) -> List[ItemOutputSchema]:
    """To get all the items"""
    resp = await ItemsService.fetch_all_items(db=db)
    return [ItemOutputSchema.model_validate(asdict(r)) for r in resp]


@items_router.get(
    path="/items/{item_id}",
    summary="items endpoint",
    description="Get item from item_id",
    response_model=ItemOutputSchema,
)
async def get_item(
    item_id: UUID, db: AsyncSession = Depends(get_db)
) -> ItemOutputSchema:
    """To get item from item_id"""
    resp = await ItemsService.fetch_item_by_id(item_id=item_id, db=db)
    return ItemOutputSchema.model_validate(asdict(resp))


@items_router.post(
    path="/items",
    summary="Create item",
    description="Create a new item",
    response_model=ItemInvoiceOutputSchema,
)
async def create_item(
    request: ItemInvoiceInputSchema, db: AsyncSession = Depends(get_db)
) -> ItemInvoiceOutputSchema:
    """To create a new item"""
    resp = await ItemsService.create_item(request=request, db=db)
    return ItemInvoiceOutputSchema.model_validate(asdict(resp))


@items_router.put(
    path="/items/{item_id}",
    summary="Update item",
    description="Update an existing item",
    response_model=ItemOutputSchema,
)
async def update_item(
    item_id: UUID, request: ItemUpdateSchema, db: AsyncSession = Depends(get_db)
) -> ItemOutputSchema:
    resp = await ItemsService.update_item(item_id=item_id, request=request, db=db)
    return ItemOutputSchema.model_validate(asdict(resp))


@items_router.delete(
    path="/items/{item_id}",
    summary="Delete item",
    description="Delete an existing item by id",
    response_model=bool,
)
async def delete_item(item_id: UUID, db: AsyncSession = Depends(get_db)) -> bool:
    resp = await ItemsService.delete_item(item_id=item_id, db=db)
    return resp
