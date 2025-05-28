from app.entities.items_entity import ItemsEntity, ItemsEntityInvoice
from app.queries.items_queries import ItemsQuery
from app.common.exceptions import BadRequestError, ServerError

import logging

logger = logging.getLogger(__name__)


class ItemsService:

    @staticmethod
    def fetch_all_items() -> list[ItemsEntity]:
        items = ItemsQuery.fetch_all_items()
        item_entities = [ItemsEntity(**item._mapping) for item in items]
        return item_entities

    @staticmethod
    def fetch_item_by_id(item_id):
        item = ItemsQuery.fetch_item_by_id(item_id)
        if item:
            return ItemsEntity(**item._mapping)
        raise BadRequestError(status_code=404, detail="item not found!")

    @staticmethod
    def create_item(request):
        resp = ItemsQuery.create_item(**request.model_dump())
        if resp:
            return ItemsEntityInvoice(**resp._mapping)
        raise ServerError()

    @staticmethod
    def update_item(item_id, request):
        item = ItemsQuery.fetch_item_by_id(item_id=item_id)
        if item is None:
            raise BadRequestError(
                status_code=404, detail=f"item with id {item_id} not found!"
            )

        resp = ItemsQuery.update_item(
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
    def delete_item(item_id):
        item = ItemsQuery.fetch_item_by_id(item_id=item_id)
        if item is None:
            raise BadRequestError(
                status_code=404, detail=f"item with id {item_id} not found!"
            )

        ItemsQuery.delete_item(item_id=item_id)
        return {}
