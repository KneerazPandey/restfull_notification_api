from rest_framework import serializers
from apps.notifications.models.notification import Notification


class NotificationSerializer(serializers.ModelField):
    class Meta:
        model = Notification

        fields = [
            'id',
            'title',
            'body',
            'notification_type',
            'is_read',
            'read_at',
            'metadata',
            'created_at',
            'updated_at',
        ]


class SendNotificationSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    title = serializers.CharField()
    body = serializers.CharField()


class BroadcastNotificationSerializer(serializers.Serializer):
    title = serializers.CharField()
    body = serializers.CharField()