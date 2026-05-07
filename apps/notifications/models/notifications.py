from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Notifications(models.Model):
    class NotificationType(models.TextChoices):
        SYSTEM = "system", "System"
        AUTHENTICATION = "authentication", "Authentication"
        MESSAGE = "message", "Message"
        PAYMENT = "payment", "Payment"
        SECURITY = "security", "Security"

    recipient = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    body = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient"]),
            models.Index(fields=["is_read"]),
            models.Index(fields=["notification_type"])
        ]

    def __str__(self):
        return f"{self.recipient.email} - {self.title}"
