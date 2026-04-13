from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
