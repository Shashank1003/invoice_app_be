from datetime import date
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.enums import PaymentTermsEnum, StatusEnum


class InvoicesQuery:
    @staticmethod
    async def fetch_all_invoices(db: AsyncSession) -> Sequence[Row]:
        result = await db.execute(
            text(
                """
        SELECT id, due_date, client_name, total, status
        FROM invoices
        """.strip()
            )
        )
        return result.fetchall()

    @staticmethod
    async def fetch_invoice_by_id(
        *, db: AsyncSession, invoice_id: UUID
    ) -> Optional[Row]:
        result = await db.execute(
            text(
                """
        SELECT id, due_date, client_name, total, status, street_from,
        street_to, city_from, city_to, country_from, country_to, postcode_from,
        postcode_to, payment_terms, client_email, invoice_date, description
        FROM invoices WHERE id=:invoice_id
        """.strip()
            ),
            {"invoice_id": invoice_id},
        )
        return result.fetchone()

    @staticmethod
    async def fetch_invoice(*, db: AsyncSession, invoice_id: UUID) -> Optional[Row]:
        result = await db.execute(
            text(
                """
                SELECT
                    i.id,
                    i.due_date,
                    i.client_name,
                    i.total,
                    i.status,
                    i.street_from,
                    i.street_to,
                    i.city_from,
                    i.city_to,
                    i.country_from,
                    i.country_to,
                    i.postcode_from,
                    i.postcode_to,
                    i.client_email,
                    i.invoice_date,
                    i.payment_terms,
                    i.description,
                    COALESCE(json_agg(
                        json_build_object(
                            'id', it.id,
                            'invoice_id', it.invoice_id,
                            'name', it.name,
                            'quantity', it.quantity,
                            'price', it.price,
                            'total', it.total
                        )
                    ) FILTER (WHERE it.id IS NOT NULL), '[]') AS items
                    FROM invoices i
                    LEFT JOIN items it ON i.id = it.invoice_id
                    WHERE i.id = :invoice_id
                    GROUP BY i.id
                    """.strip()
            ),
            {"invoice_id": invoice_id},
        )
        return result.fetchone()

    @staticmethod
    async def create_invoice(
        *,
        db: AsyncSession,
        due_date: date,
        client_name: str,
        total: float,
        status: StatusEnum,
        street_from: str,
        street_to: str,
        city_from: str,
        city_to: str,
        country_from: str,
        country_to: str,
        postcode_from: str,
        postcode_to: str,
        client_email: str,
        invoice_date: date,
        payment_terms: PaymentTermsEnum,
        description: str,
    ) -> Optional[Row]:
        status_str = status.value
        payment_terms_str = payment_terms.value
        result = await db.execute(
            text(
                """
                INSERT INTO invoices (due_date, client_name, total, status, street_from,
                street_to, city_from, city_to, country_from, country_to,
                postcode_from, postcode_to, client_email, invoice_date,
                payment_terms, description)
                VALUES (:due_date, :client_name, :total, :status, :street_from,
                :street_to, :city_from, :city_to, :country_from, :country_to,
                :postcode_from, :postcode_to, :client_email, :invoice_date,
                :payment_terms, :description)
                RETURNING due_date, client_name, total, status, street_from,
                street_to, city_from, city_to, country_from, country_to,
                postcode_from, postcode_to, client_email, invoice_date,
                payment_terms, description, id
                """.strip()
            ),
            {
                "due_date": due_date,
                "client_name": client_name,
                "total": total,
                "status": status_str,
                "street_from": street_from,
                "street_to": street_to,
                "city_from": city_from,
                "city_to": city_to,
                "country_from": country_from,
                "country_to": country_to,
                "postcode_from": postcode_from,
                "postcode_to": postcode_to,
                "client_email": client_email,
                "invoice_date": invoice_date,
                "payment_terms": payment_terms_str,
                "description": description,
            },
        )
        return result.fetchone()

    @staticmethod
    async def update_invoice(
        *,
        db: AsyncSession,
        due_date: date,
        client_name: str,
        total: float,
        status: StatusEnum,
        street_from: str,
        street_to: str,
        city_from: str,
        city_to: str,
        country_from: str,
        country_to: str,
        postcode_from: str,
        postcode_to: str,
        client_email: str,
        invoice_date: date,
        payment_terms: PaymentTermsEnum,
        description: str,
        id: UUID,
    ) -> Optional[Row]:
        status_str = status.value
        payment_terms_str = payment_terms.value
        result = await db.execute(
            text(
                """
            UPDATE invoices SET due_date=:due_date, client_name=:client_name,
            total=:total, status=:status, street_from=:street_from,
            street_to=:street_to, city_from=:city_from, city_to=:city_to,
            country_from=:country_from, country_to=:country_to,
            postcode_from=:postcode_from, postcode_to=:postcode_to,
            client_email=:client_email, invoice_date=:invoice_date,
            payment_terms=:payment_terms, description=:description
            WHERE id = :id
            RETURNING due_date, client_name, total, status, street_from,
            street_to, city_from, city_to, country_from, country_to,
            postcode_from, postcode_to, client_email, invoice_date,
            payment_terms, description, id;
            """.strip()
            ),
            {
                "due_date": due_date,
                "client_name": client_name,
                "total": total,
                "status": status_str,
                "street_from": street_from,
                "street_to": street_to,
                "city_from": city_from,
                "city_to": city_to,
                "country_from": country_from,
                "country_to": country_to,
                "postcode_from": postcode_from,
                "postcode_to": postcode_to,
                "client_email": client_email,
                "invoice_date": invoice_date,
                "payment_terms": payment_terms_str,
                "description": description,
                "id": id,
            },
        )
        return result.fetchone()

    @staticmethod
    async def delete_invoice(*, db: AsyncSession, invoice_id: UUID) -> bool:
        await db.execute(
            text(
                """
        DELETE FROM invoices WHERE id=:invoice_id
        """.strip()
            ),
            {"invoice_id": invoice_id},
        )
        return True
