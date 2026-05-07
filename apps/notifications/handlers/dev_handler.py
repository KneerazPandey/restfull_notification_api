from core.events.registry import EventRegistry


@EventRegistry.register('notification.created')
def development_handler(event):
    print(f"Development Handler running, {event.notification_id}")