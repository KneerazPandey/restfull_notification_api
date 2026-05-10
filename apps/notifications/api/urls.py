from django.urls import path
from apps.notifications.api.views import (
    NotificationListAPIView, SendNotificationAPIView
)


urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='list'),

    path('send/', SendNotificationAPIView.as_view(), name='send-notification'),
]