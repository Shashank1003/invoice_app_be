import asyncio
import random
from uuid import uuid4

from faker import Faker

from app.adapters.database.core import AsyncSessionLocal  # your async sessionmaker
from app.common.enums import PaymentTermsEnum, StatusEnum
from app.models.invoice_model import Invoice
from app.models.item_model import Item

# from sqlalchemy.ext.asyncio import AsyncSession


faker = Faker()


def generate_fake_invoice() -> Invoice:
    invoice = Invoice(
        id=uuid4(),
        client_name=faker.name(),
        client_email=faker.email(),
        street_from=faker.street_address(),
        street_to=faker.street_address(),
        city_from=faker.city(),
        city_to=faker.city(),
        postcode_from=faker.postcode(),
        postcode_to=faker.postcode(),
        country_from=faker.country(),
        country_to=faker.country(),
        invoice_date=faker.date_this_year(),
        due_date=None,
        status=random.choice(list(StatusEnum)),
        payment_terms=random.choice(list(PaymentTermsEnum)),
        description=faker.sentence(),
        total=0.0,  # will be updated after item creation
    )
    total_sum = 0.0
    for _ in range(random.randint(1, 10)):
        quantity = random.randint(1, 100)
        price = round(random.uniform(10.0, 500.0), 2)
        total = round(quantity * price, 2)
        item = Item(
            id=uuid4(),
            name=faker.word(),
            quantity=quantity,
            price=price,
            total=total,
            # invoice_id = invoice.id -- handled automatically by sqlAlchemy
        )
        total_sum = total_sum + total
        invoice.items.append(item)

    invoice.total = round(total_sum, 2)  # type: ignore[attr-defined]
    return invoice


async def seed_invoices(n: int = 10) -> None:
    async with AsyncSessionLocal() as session:

        try:
            invoices = [generate_fake_invoice() for _ in range(n)]
            session.add_all(invoices)
            await session.commit()
            print(f"seeded {n} invoices successfully!")
        except Exception as e:
            await session.rollback()
            print(f"error in seeding invoices. {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_invoices(30))

# Run this query in PostgreSQL to set due_date
"""
UPDATE invoices
SET due_date = CASE payment_terms
    WHEN 'ONE' THEN invoice_date + INTERVAL '1 day'
    WHEN 'SEVEN' THEN invoice_date + INTERVAL '7 days'
    WHEN 'FOURTEEN' THEN invoice_date + INTERVAL '14 days'
    WHEN 'THIRTY' THEN invoice_date + INTERVAL '30 days'
    ELSE NULL
END;
"""
