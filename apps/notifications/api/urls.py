from django.urls import path
from apps.notifications.api.views import (
    NotificationListAPIView
)


urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='list')
]