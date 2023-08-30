from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Notification
    from django.contrib.auth.models import AbstractBaseUser


def get_notifications(user: AbstractBaseUser) -> list[Notification]:
    notifications = user.notifications.select_related("tweet", "notification_type").all().order_by("-created_at")
    return list(notifications)
