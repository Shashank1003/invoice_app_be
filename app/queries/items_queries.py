from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession


class ItemsQuery:
    @staticmethod
    async def fetch_all_items(db: AsyncSession) -> Sequence[Row]:
        all_items = await db.execute(
            text("""SELECT id, name, quantity, price, total FROM items""".strip())
        )
        return all_items.fetchall()

    @staticmethod
    async def fetch_item_by_id(db: AsyncSession, item_id: UUID) -> Optional[Row]:
        item = await db.execute(
            text(
                """
        SELECT id, name, quantity, price, total FROM items
        WHERE id=:item_id
        """.strip()
            ),
            {"item_id": item_id},
        )
        return item.fetchone()

    @staticmethod
    async def create_item(
        db: AsyncSession,
        name: str,
        quantity: int,
        price: float,
        total: float,
        invoice_id: UUID,
    ) -> Optional[Row]:
        result = await db.execute(
            text(
                """
        INSERT INTO items (name, quantity, price, total, invoice_id)
        VALUES (:name, :quantity, :price, :total, :invoice_id)
        RETURNING id, name, quantity, price, total, invoice_id
        """.strip()
            ),
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "total": total,
                "invoice_id": invoice_id,
            },
        )
        return result.fetchone()

    @staticmethod
    async def update_item(
        db: AsyncSession,
        item_id: UUID,
        name: str,
        quantity: int,
        price: float,
        total: float,
    ) -> Optional[Row]:
        result = await db.execute(
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
            ),
            {
                "item_id": item_id,
                "name": name,
                "quantity": quantity,
                "price": price,
                "total": total,
            },
        )
        return result.fetchone()

    @staticmethod
    async def delete_item(db: AsyncSession, item_id: UUID) -> bool:
        await db.execute(
            text(
                """
        DELETE FROM items
        WHERE id=:item_id
        """.strip()
            ),
            {"item_id": item_id},
        )
        return True

    @staticmethod
    async def create_invoice_item(
        db: AsyncSession,
        name: str,
        quantity: int,
        price: float,
        total: float,
        invoice_id: UUID,
    ) -> Optional[Row]:
        result = await db.execute(
            text(
                """
        INSERT INTO items (name, quantity, price, total, invoice_id)
        VALUES (:name, :quantity, :price, :total, :invoice_id)
        RETURNING id, name, quantity, price, total
        """.strip()
            ),
            {
                "name": name,
                "quantity": quantity,
                "price": price,
                "total": total,
                "invoice_id": invoice_id,
            },
        )
        return result.fetchone()

    @staticmethod
    async def delete_invoice_items(db: AsyncSession, invoice_id: UUID) -> bool:
        await db.execute(
            text(
                """
                DELETE FROM items
                WHERE invoice_id=:invoice_id
                """.strip()
            ),
            {"invoice_id": invoice_id},
        )
        return True
