from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from core.events.registry import EventRegistry


@EventRegistry.register('notification.created')
def notification_websocket_handler(event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{event.recipient_id}',
        {
            'type': 'send_notification',
            'data': {
                'id': event.notification_id,
                'title': event.title,
                'body': event.body,
            }
        }
    )