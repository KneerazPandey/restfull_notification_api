from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class DeviceToken(models.Model):
    class DeviceType(models.TextChoices):
        ANDROID = "android", "Android"
        IOS = "ios", "Ios"
        WEB = "web", "Web"
        WINDOWS = "windows", "Windows"

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='device_tokens'
    )

    token = models.TextField(unique=True)
    device_type = models.CharField(
        max_length=20,
        choices=DeviceType.choices,
    )

    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["device_type"])
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.device_type}"
