from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from core.business_logic.exceptions import PageDoesNotExists
from core.business_logic.services import get_notifications
from core.presentation.common import paginate_pages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View


class NotificationView(LoginRequiredMixin, View):
    """
    Controller responsible for displaying all notifications to the user.
    """

    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        notifications = get_notifications(user=user)

        try:
            notifications_paginated, prev_page, next_page = paginate_pages(
                request=request, data=notifications, per_page=20
            )
        except PageDoesNotExists as err:
            return HttpResponseBadRequest(content=err)

        context = {"notifications_paginated": notifications_paginated, "next_page": next_page, "prev_page": prev_page}

        return render(request, "notification.html", context=context)
