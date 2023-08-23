from django.db import models

from .base import BaseModel


class NotificationType(BaseModel):
    name = models.CharField(max_length=7, unique=True, verbose_name="notification type")

    class Meta:
        verbose_name_plural = "notification type"

    def __str__(self) -> str:
        return f"{self.name}"
