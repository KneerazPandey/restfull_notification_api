from apps.notifications.models import Notification, DeviceToken


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
    
    @staticmethod
    def get_user_device_token(user_id):
        return DeviceToken.objects.filter(
            user__id = user_id
        ).values_list('token', flat=True)
