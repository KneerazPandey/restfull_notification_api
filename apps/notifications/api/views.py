from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
from apps.notifications.services import NotificationService
from apps.notifications.selectors import NotificationSelectors
from apps.notifications.api.serializers import (
    NotificationSerializer, SendNotificationSerializer, BroadcastNotificationSerializer
)


User = get_user_model()


class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        notifications = NotificationSelectors.get_notifications(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    

class SendNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = get_object_or_404(User, id=serializer.validated_data['user_id'])

        notification = NotificationService.create_notification(
            recipient=user,
            title=serializer.validated_data['title'],
            body=serializer.validated_data['title']
        )

        return Response(data={
            'id': notification.id,
            'message': 'Notification Sent'
        })

class BroadcastNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = BroadcastNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        NotificationService.broadcase_notification(
            title=serializer.validated_data['title'],
            body=serializer.validated_data['body']
        )

        return Response({
            'message': 'Broadcast sent'
        })
    
class MarkNotificationAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request, notification_id: str):
        notification = get_object_or_404(
            Notification,
            id=notification_id, 
            recipient=request.user
        )

        NotificationService.mark_all_as_read(notification)

        return Response({
            'message': 'Notification marked as read'
        })
    
class MarkedAllNotificationAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request: Request):
        NotificationService.mark_all_as_read(user=request.user)

        return Response({
            'message': 'All notificatino marked as read'
        })
    

class DeleteNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, notification_id: str):
        notificaiton = get_object_or_404(
            Notification,
            id=notification_id,
            recipient=request.user 
        )

        NotificationService.delete_notification(notification=notificaiton)

        return Response({
            'message': 'Notification Deleted'
        })


class GetUnreadNotificationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        count = NotificationService.get_unread_notification_count(user=request.user)

        return Response({
            'unread_count': count
        })