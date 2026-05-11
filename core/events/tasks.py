from celery import shared_task
from django.utils.module_loading import import_string

from apps.notifications.events.notification_created import (
    NotificationCreatedEvent
)


EVENT_MAPPING = {
    "NotificationCreatedEvent": NotificationCreatedEvent
}


@shared_task
def execute_event_handler_async(
    handler_path,
    event_class,
    event_data
):

    handler = import_string(handler_path)

    event_cls = EVENT_MAPPING[event_class]

    event = event_cls(**event_data)

    handler(event)