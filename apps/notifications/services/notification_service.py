from django.utils import timezone
from apps.notifications.models import Notification
from django.contrib.auth import get_user_model
from apps.notifications.selectors import NotificationSelectors
from apps.notifications.events import NotificationCreatedEvent
from core.events.dispatcher import EventDispatcher


User = get_user_model()


class NotificationService:

    @staticmethod
    def create_notification(recipient: str, title: str, body: str, notification_type: str = 'system', metadata=None):
        notification = Notification.objects.create(
            recipient=recipient,
            title=title,
            body=body,
            notification_type=notification_type,
            metadata=metadata or {}
        )

        event = NotificationCreatedEvent(
            notification_id=notification.id,
            recipient_id=notification.recipient.id,
            title=notification.title,
            body=notification.body
        )

        EventDispatcher.dispatch(event=event)

        return notification

    @staticmethod
    def broadcase_notification(title: str, body: str, notification_type: str = 'system', metadata=None):
        users = User.objects.all()

        notifications = []

        for user in users:
            notification = Notification.objects.create(
                recipient=user,
                title=title,
                body=body,
                notification_type=notification_type,
                metadata=metadata or {}
            )
            notifications.append(notification)

        return notifications
    
    @staticmethod
    def mark_as_read(notification: Notification):
        notification.is_read = True
        notification.read_at = timezone.now()

        notification.save(
            update_fields=['is_read', 'read_at', 'updated_at']
        )

        return notification
    
    @staticmethod
    def mark_all_as_read(user):
        Notification.objects.filter(
            recipient=user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )


    @staticmethod
    def delete_notification(notification: Notification):
        notification.delete()

    @staticmethod
    def get_unread_notification_count(user):
        return NotificationSelectors.get_unread_count(user=user)
