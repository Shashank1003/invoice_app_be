import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import BadRequestError, ServerError
from app.entities.items_entity import ItemsEntity, ItemsEntityInvoice
from app.queries.items_queries import ItemsQuery
from app.schemas.item_schema import (
    ItemInvoiceInputSchema,
    ItemUpdateSchema,
)

logger = logging.getLogger(__name__)


class ItemsService:

    @staticmethod
    async def fetch_all_items(db: AsyncSession) -> list[ItemsEntity]:
        items = await ItemsQuery.fetch_all_items(db=db)
        item_entities = [ItemsEntity(**item._mapping) for item in items]
        return item_entities

    @staticmethod
    async def fetch_item_by_id(item_id: UUID, db: AsyncSession) -> ItemsEntity:
        item = await ItemsQuery.fetch_item_by_id(item_id=item_id, db=db)
        if item:
            return ItemsEntity(**item._mapping)
        raise BadRequestError(status_code=404, detail="item not found!")

    @staticmethod
    async def create_item(
        request: ItemInvoiceInputSchema, db: AsyncSession
    ) -> ItemsEntityInvoice:
        resp = await ItemsQuery.create_item(db=db, **request.model_dump())
        if resp:
            return ItemsEntityInvoice(**resp._mapping)
        raise ServerError()

    @staticmethod
    async def update_item(
        item_id: UUID, request: ItemUpdateSchema, db: AsyncSession
    ) -> ItemsEntity:
        item = await ItemsQuery.fetch_item_by_id(db=db, item_id=item_id)
        if item is None:
            raise BadRequestError(
                status_code=404, detail=f"item with id {item_id} not found!"
            )

        resp = await ItemsQuery.update_item(
            db=db,
            item_id=item_id,
            name=request.name,
            quantity=request.quantity,
            price=request.price,
            total=request.total,
        )
        if resp:
            return ItemsEntity(*resp)
        raise ServerError()

    @staticmethod
    async def delete_item(item_id: UUID, db: AsyncSession) -> bool:
        item = await ItemsQuery.fetch_item_by_id(db=db, item_id=item_id)
        if item is None:
            raise BadRequestError(
                status_code=404, detail=f"item with id {item_id} not found!"
            )

        await ItemsQuery.delete_item(db=db, item_id=item_id)
        return True
