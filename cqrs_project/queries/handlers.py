from fastapi import APIRouter, HTTPException
from typing import List

from infrastructure.mongo_database import mongo_client
from queries.schemas import OrderResponseSchema

router = APIRouter()


@router.get("/orders/{customer_id}", response_model=List[OrderResponseSchema])
async def get_orders_by_customer(customer_id: str):
    db = mongo_client["cqrs_db"]
    collection = db["order_projections"]

    orders = []
    async for doc in collection.find({"customer_id": customer_id}):
        doc["_id"] = str(doc["_id"])  # serialize ObjectId
        orders.append(doc)

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this customer")

    return orders


@router.get("/orders/detail/{order_id}", response_model=OrderResponseSchema)
async def get_order_detail(order_id: str):
    db = mongo_client["cqrs_db"]
    collection = db["order_projections"]

    doc = await collection.find_one({"order_id": order_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")

    doc["_id"] = str(doc["_id"])
    return doc
