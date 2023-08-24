from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from core.business_logic.dto import CreateTweetDTO
from core.business_logic.services import create_tweet, get_tweets
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import CreateTweetForm


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


class CreateTweet(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CreateTweetForm()
        context = {"form": form}
        return render(request, "create_tweet.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CreateTweetForm(request.POST)
        if form.is_valid():
            user = request.user
            data = convert_data_from_form_to_dto(dto=CreateTweetDTO, data_from_form=form.cleaned_data)
            create_tweet(data=data, user=user)
            return redirect("profile")
        else:
            context = {"form": form}
            return render(request, "create_tweet.html", context=context)
