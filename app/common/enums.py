from enum import Enum

class StatusEnum(Enum):
  DRAFT = "draft"
  PENDING = "pending"
  PAID = "paid"
  
class PaymentTermsEnum(Enum):
  ONE = "1_day"
  SEVEN = "7_day"
  FOURTEEN = "14_day"
  THIRTY = "30_day"