from enum import Enum

class StatusEnum(Enum):
  DRAFT = "DRAFT"
  PENDING = "PENDING"
  PAID = "PAID"
  
class PaymentTermsEnum(Enum):
  ONE = "ONE"
  SEVEN = "SEVEN"
  FOURTEEN = "FOURTEEN"
  THIRTY = "THIRTY"