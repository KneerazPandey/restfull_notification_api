from firebase_admin import messaging
from core.events.registry import EventRegistry
from apps.notifications.selectors import NotificationSelectors


@EventRegistry.register('notification.created')
def push_notification_handler(event):
    tokens = NotificationSelectors.get_user_device_token(user_id=event.recipient_id)
    print('sending push notification')
    for device in tokens:
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=event.title,
                    body=event.body,
                ),
                data={
                    'notification_id': str(event.notification_id),
                    'type': 'notification'
                },
                token=device.token,
            )
            messaging.send(message)
        except Exception as e:
            print(f'FCM error: {str(e)}')