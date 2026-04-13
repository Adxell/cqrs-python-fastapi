from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class OrderCreatedEvent:
    order_id: str
    customer_id: str
    total_amount: float
    event_type: str = "OrderCreated"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
