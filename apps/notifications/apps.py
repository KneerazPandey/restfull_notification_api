from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'apps.notifications'

    def ready(self):
        import apps.notifications.handlers.notification_websocket_handler
        import apps.notifications.handlers.push_notification_handler
