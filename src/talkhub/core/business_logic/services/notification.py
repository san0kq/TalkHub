from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from accounts.models import User
    from core.models import Notification


def get_notifications(user: User) -> list[Notification]:
    notifications = user.notifications.select_related("tweet", "notification_type").all().order_by("-created_at")
    return list(notifications)
