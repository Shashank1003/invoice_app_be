from uuid import UUID
from pydantic import BaseModel, Field

class ItemInputSchema(BaseModel):
  name: str= Field(..., min_length=1, max_length=100)
  quantity: int = Field(..., ge=1 )
  price: float = Field(..., gt=0)
  total: float = Field(..., gt=0)
  
class ItemOutputSchema(ItemInputSchema):
  id: UUID = Field(..., description="identifier for item")
