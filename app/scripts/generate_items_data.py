import random
from uuid import uuid4
from faker import Faker

from app.adapters.database import db_session
from app.models.item_model import Item

fake = Faker()


def generate_fake_item():
    quantity = random.randint(1, 100)
    price = round(random.uniform(10.0, 500.0), 2)
    total = round(quantity * price, 2)
    return Item(
        id=uuid4(),
        name=fake.word().capitalize(),
        quantity=quantity,
        price=price,
        total=total,
    )


def seed_items(n=10):
    try:
        for i in range(n):
            db_session.add(generate_fake_item())
        db_session.commit()
        print(f"seeded {n} items successfully")
    except Exception as e:
        db_session.rollback()
        print(f"error in seeding items. {e}")
    finally:
        db_session.close()


if __name__ == "__main__":
    seed_items(30)
