from .registry import EventRegistry
from .base import BaseEvent
from .tasks import execute_event_handler_async


class EventDispatcher:

    @staticmethod
    def dispatch(event: BaseEvent):

        handlers = EventRegistry.get_handlers(
            event_name=event.event_name
        )

        for handler in handlers:
            handler(event)

    @staticmethod
    def dispatch_async(event: BaseEvent):

        handlers = EventRegistry.get_handlers(
            event_name=event.event_name
        )

        for handler in handlers:

            handler_path = (
                f"{handler.__module__}."
                f"{handler.__name__}"
            )

            execute_event_handler_async.delay(
                handler_path=handler_path,
                event_class=event.__class__.__name__,
                event_data=event.__dict__
            )