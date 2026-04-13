from pydantic import BaseModel, Field
from typing import List
import uuid


class OrderItemSchema(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0, description="Must be greater than 0")


class CreateOrderCommand(BaseModel):
    customer_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    items: List[OrderItemSchema] = Field(..., min_length=1)
