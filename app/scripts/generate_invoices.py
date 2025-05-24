import random
from uuid import uuid4
from faker import Faker

from app.adapters.database import db_session
from app.models.invoice_model import Invoice
from app.models.item_model import Item
from app.common.enums import StatusEnum, PaymentTermsEnum

faker = Faker()

def generate_fake_invoice():
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
    total_sum = 0
    for i in range(random.randint(1,10)):
      quantity= random.randint(1, 100)
      price = round(random.uniform(10.0, 500.0), 2)
      total = round(quantity * price, 2)
      item = Item(
        id= uuid4(),
        name = faker.word(),
        quantity= quantity,
        price = price,
        total = total,
        # invoice_id = invoice.id -- handled automatically by sqlAlchemy
      )
      total_sum = total_sum + total
      invoice.items.append(item)
      
    invoice.total = round(total_sum, 2)  # type: ignore
    return invoice
      

def seed_invoices(n=10):
  try:
    for i in range(n):
      db_session.add(generate_fake_invoice())
    db_session.commit()
    print(f"seeded {n} invoices successfully!")
  except Exception as e:
    db_session.rollback()
    print(f"error in seeding invoices. {e}")
  finally:
    db_session.close()
    
if __name__ == "__main__":
  seed_invoices(30)