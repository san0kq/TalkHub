from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class LogoutView(View):
    """
    Controller for logging out of the account.

    Supports only GET requests.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request=request)
        return redirect("signin")
