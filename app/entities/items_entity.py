from dataclasses import dataclass
from uuid import UUID

@dataclass
class ItemsEntity:
  id: UUID
  name: str
  quantity: int
  price: float
  total: float