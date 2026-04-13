import asyncio
from typing import Callable, Dict, List, Any


class AsyncEventBus:
    """
    Simple in-memory async event bus.
    For production, replace with Kafka or RabbitMQ.
    """

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: Any):
        event_type = getattr(event, "event_type", type(event).__name__)
        handlers = self._handlers.get(event_type, [])
        for handler in handlers:
            # Fire and forget — don't block the command response
            asyncio.create_task(handler(event))


event_bus = AsyncEventBus()
