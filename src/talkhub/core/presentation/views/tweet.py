from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from core.business_logic.services import get_tweets


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        tweets = get_tweets()

        return render(request, "index.html", context={"tweet": tweets})
