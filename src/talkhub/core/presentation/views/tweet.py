from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from core.business_logic.services import get_tweets


class IndexView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        try:
            page_number = request.GET["page"]
        except KeyError:
            page_number = 1

        tweets = get_tweets(user=user)
        paginator = Paginator(tweets, 20)

        try:
            tweets_paginated = paginator.page(page_number)

        except EmptyPage:
            return HttpResponseBadRequest("Page with provided number doesn't exist.")

        if tweets_paginated.has_next():
            next_page = tweets_paginated.next_page_number()
        else:
            next_page = None

        if tweets_paginated.has_previous():
            prev_page = tweets_paginated.previous_page_number()
        else:
            prev_page = None

        context = {"tweets": tweets_paginated, "next_page": next_page, "prev_page": prev_page}
        return render(request, "index.html", context=context)
