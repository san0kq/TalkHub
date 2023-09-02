from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dto import NotificationDTO

from core.models import Notification, NotificationType
from django.contrib.auth import get_user_model
from django.db import transaction


class NotificationDAO:
    def create(self, data: NotificationDTO) -> None:
        with transaction.atomic():
            user_model = get_user_model()
            user = user_model.objects.get(pk=data.user_id)
            notification_type = NotificationType.objects.get(name="admin")
            notification = Notification.objects.create(user=user, text=data.text, notification_type=notification_type)
            notification.recipients.add(user)
