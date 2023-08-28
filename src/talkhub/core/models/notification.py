from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseModel


class Notification(BaseModel):
    text = models.CharField(max_length=100, blank=True)
    tweet = models.ForeignKey(
        to="Tweet",
        null=True,
        blank=True,
        related_name="notifications",
        related_query_name="notification",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        to=get_user_model(),
        null=True,
        blank=True,
        related_name="notification_ratings",
        related_query_name="notification_rating",
        on_delete=models.CASCADE,
    )
    recipients = models.ManyToManyField(
        to=get_user_model(), related_name="notifications", related_query_name="notification"
    )
    notification_type = models.ForeignKey(
        to="NotificationType", related_name="notifications", related_query_name="notification", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "notifications"

    def __str__(self) -> str:
        return f"{self.notification_type.name}: {self.text}"
