from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from core.business_logic.services import get_notifications
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class NotificationView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        notifications = get_notifications(user=user)
        context = {"notifications": notifications}
        return render(request, "notification.html", context=context)
