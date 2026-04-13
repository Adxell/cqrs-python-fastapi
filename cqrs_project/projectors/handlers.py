from motor.motor_asyncio import AsyncIOMotorClient
from domain.events import OrderCreatedEvent


class OrderReadModelProjector:
    """
    Listens to domain events and updates the MongoDB read model.
    This is what keeps both databases in sync.
    """

    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.collection = mongo_client["cqrs_db"]["order_projections"]

    async def handle_order_created(self, event: OrderCreatedEvent):
        document = {
            "order_id": event.order_id,
            "customer_id": event.customer_id,
            "total_amount": event.total_amount,
            "status": "PENDING",
            "created_at": event.timestamp,
            "display_title": f"Order #{event.order_id[:8]} — ${event.total_amount:.2f}",
        }

        await self.collection.update_one(
            {"order_id": event.order_id},
            {"$set": document},
            upsert=True,
        )
