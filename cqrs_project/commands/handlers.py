import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from commands.schemas import CreateOrderCommand
from domain.models import Order, Product
from domain.events import OrderCreatedEvent
from infrastructure.event_bus import event_bus
from infrastructure.pg_database import get_session

router = APIRouter()


class OrderCommandHandler:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def handle_create_order(self, command: CreateOrderCommand) -> str:
        order_id = str(uuid.uuid4())
        total = 0.0

        for item in command.items:
            result = await self.db.execute(
                select(Product).where(Product.id == item.product_id)
            )
            product = result.scalars().first()

            if not product:
                raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {item.product_id}")

            product.stock -= item.quantity
            total += product.price * item.quantity

        new_order = Order(
            id=order_id,
            customer_id=command.customer_id,
            total_amount=total,
            status="PENDING",
        )
        self.db.add(new_order)
        await self.db.commit()

        # Publish domain event — read model will update asynchronously
        event = OrderCreatedEvent(
            order_id=order_id,
            customer_id=command.customer_id,
            total_amount=total,
        )
        await event_bus.publish(event)

        return order_id


@router.post("/orders", status_code=201)
async def create_order(
    command: CreateOrderCommand,
    db: AsyncSession = Depends(get_session),
):
    handler = OrderCommandHandler(db)
    order_id = await handler.handle_create_order(command)
    return {"order_id": order_id, "message": "Order created. Read model will sync shortly."}
