from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from core.business_logic.services import update_config
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View


class UpdateConfig(LoginRequiredMixin, View):
    login_url = "signin"

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        selected_option = request.POST["option"]
        update_config(user=user, option=selected_option)
        return redirect("profile", profile_uuid=user.profile.pk)
