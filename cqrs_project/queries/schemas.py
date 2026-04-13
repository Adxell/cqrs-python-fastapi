from pydantic import BaseModel
from typing import Optional


class OrderResponseSchema(BaseModel):
    order_id: str
    customer_id: str
    total_amount: float
    status: str
    created_at: str
    display_title: Optional[str] = None

    class Config:
        from_attributes = True
