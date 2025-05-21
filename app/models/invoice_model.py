from sqlalchemy import Column, String, text, Date
from sqlalchemy.dialects.postgresql import UUID
from app.adapters.database import Base
from ._utils import ResourceMixin
import datetime

class Invoice(ResourceMixin, Base):
  __tablename__ = "invoices"
  
  id = Column(UUID(as_uuid=True),
              primary_key=True,
              default=text("uuid_generate_v4()"),
              unique=True,
              index=True,
              nullable=False)
  due_date = Column(Date, unique=False, index=True, nullable=False)
  client_name= Column(String, unique=False, nullable=False, index=True)
  client_email = Column(String, unique=False, nullable=False, index=True)
  street_from = Column(String, unique=False, nullable=False, index=False)
  street_to = Column(String, unique=False, nullable=False, index=False)
  city_from = Column(String, unique=False, nullable=False, index=False)
  city_to = Column(String, unique=False, nullable=False, index=False)
  postcode_from = Column(String, unique=False, nullable=False, index=False)
  postcode_to = Column(String, unique=False, nullable=False, index=False)
  country_from = Column(String, unique=False, nullable=False, index=True)
  country_to = Column(String, unique=False, nullable=False, index=True)
  invoice_date=Column(Date,
                    default=datetime.date.today,
                    unique=False,
                    index=True,
                    nullable=False)