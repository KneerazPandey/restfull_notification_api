from dataclasses import dataclass
from core.events.base import BaseEvent


@dataclass(frozen=True, kw_only=True)
class NotificationCreatedEvent(BaseEvent):
    notification_id: str 
    recipient_id: str 

    title: str 
    body: str 

    event_name: str = 'notification.created'