from .registry import EventRegistry
from .base import BaseEvent


class EventDispatcher:

    @staticmethod
    def dispatch(event: BaseEvent):
        handlers = EventRegistry.get_handlers(
            event_name=event.event_name
        )

        for handler in handlers:
            handler(event)