from apps.notifications.models.notification import Notification


class NotificationSelectors:

    @staticmethod
    def get_notifications(user):
        return Notification.objects.filter(
            recipient=user
        ).order_by('-created_at')


    @staticmethod
    def get_unread_count(user):
        return Notification.objects.filter(
            recipient=user, 
            is_read=False,
        ).count()