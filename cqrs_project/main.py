from fastapi import FastAPI
from commands.handlers import router as command_router
from queries.handlers import router as query_router
from infrastructure.event_bus import event_bus
from projectors.handlers import OrderReadModelProjector
from infrastructure.mongo_database import mongo_client
from infrastructure.pg_database import engine
from domain.models import Base

app = FastAPI(title="CQRS Demo - FastAPI + PostgreSQL + MongoDB")

app.include_router(command_router, prefix="/commands", tags=["Commands"])
app.include_router(query_router, prefix="/queries", tags=["Queries"])


@app.on_event("startup")
async def startup():
    # Create PostgreSQL tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Register projectors on event bus
    projector = OrderReadModelProjector(mongo_client)
    event_bus.subscribe("OrderCreated", projector.handle_order_created)


@app.get("/")
async def root():
    return {"message": "CQRS API running. See /docs for endpoints."}
