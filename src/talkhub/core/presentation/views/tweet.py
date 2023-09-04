from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from uuid import UUID

from core.business_logic.dto import CreateTweetDTO
from core.business_logic.exceptions import (
    AccessDeniedError,
    PageDoesNotExists,
    RetweetAlreadyExistsError,
    TagsError,
    TweetDoesNotExists,
)
from core.business_logic.services import (
    create_reply,
    create_retweet,
    create_tweet,
    delete_retweet,
    delete_tweet,
    get_tweet_by_uuid,
    get_tweets,
    initial_tweet_form,
    tweet_like,
    update_tweet,
)
from core.presentation.common import paginate_pages
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import CreateTweetForm


class IndexView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        tweets = get_tweets(user=user)
        try:
            tweets_paginated, prev_page, next_page = paginate_pages(request=request, data=tweets, per_page=20)
        except PageDoesNotExists as err:
            return HttpResponseBadRequest(content=err)

        context = {"tweets": tweets_paginated, "next_page": next_page, "prev_page": prev_page}
        return render(request, "index.html", context=context)


class CreateTweet(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = CreateTweetForm()
        context = {"form": form}
        return render(request, "create_tweet.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CreateTweetForm(request.POST)
        if form.is_valid():
            user = request.user
            data = convert_data_from_form_to_dto(dto=CreateTweetDTO, data_from_form=form.cleaned_data)
            try:
                create_tweet(data=data, user=user)
                return redirect("profile", profile_uuid=user.profile.pk)
            except TagsError as err:
                error_message = err
                context = {"form": form, "error_message": error_message}
                return render(request, "create_tweet.html", context=context)
        else:
            context = {"form": form}
            return render(request, "create_tweet.html", context=context)


class TweetView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, tweet_uuid: UUID) -> HttpResponse:
        try:
            tweet, reply_tweets = get_tweet_by_uuid(tweet_uuid=tweet_uuid)
        except TweetDoesNotExists:
            return redirect("index")

        try:
            reply_tweets_paginated, prev_page, next_page = paginate_pages(request, reply_tweets, per_page=20)

        except PageDoesNotExists as err:
            return HttpResponseBadRequest(content=err)

        context = {
            "tweet": tweet,
            "reply_tweets_paginated": reply_tweets_paginated,
            "prev_page": prev_page,
            "next_page": next_page,
        }
        return render(request, "tweet.html", context=context)


class TweetLikeView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, tweet_uuid: UUID) -> HttpResponse:
        tweet_like(tweet_uuid=tweet_uuid, user=request.user)
        current_page = request.META.get("HTTP_REFERER")
        return redirect(current_page)


class TweetReplyView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, parent_tweet_uuid: UUID) -> HttpResponse:
        form = CreateTweetForm()
        parent_tweet = get_tweet_by_uuid(tweet_uuid=parent_tweet_uuid)[0]
        context = {"form": form, "parent_tweet": parent_tweet}
        return render(request, "create_reply.html", context=context)

    def post(self, request: HttpRequest, parent_tweet_uuid: UUID) -> HttpResponse:
        form = CreateTweetForm(request.POST)
        if form.is_valid():
            user = request.user
            data = convert_data_from_form_to_dto(dto=CreateTweetDTO, data_from_form=form.cleaned_data)
            create_reply(data=data, user=user, parent_tweet_uuid=parent_tweet_uuid)
            return redirect("tweet", tweet_uuid=parent_tweet_uuid)
        else:
            parent_tweet = get_tweet_by_uuid(tweet_uuid=parent_tweet_uuid)[0]
            context = {"form": form, "parent_tweet": parent_tweet}
            return render(request, "create_reply.html", context=context)


class RetweetView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, tweet_uuid: UUID) -> HttpResponse:
        user = request.user
        try:
            create_retweet(user=user, tweet_uuid=tweet_uuid)
        except RetweetAlreadyExistsError:
            current_page = request.META.get("HTTP_REFERER")
            return redirect(current_page)
        return redirect("profile", profile_uuid=user.profile.pk)


class UpdateTweetView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, tweet_uuid: UUID) -> HttpResponse:
        initial = initial_tweet_form(tweet_uuid=tweet_uuid)
        form = CreateTweetForm(initial=initial)
        context = {"form": form}
        return render(request, "update_tweet.html", context=context)

    def post(self, request: HttpRequest, tweet_uuid: UUID) -> HttpResponse:
        form = CreateTweetForm(request.POST)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=CreateTweetDTO, data_from_form=form.cleaned_data)
            error_message: AccessDeniedError | TagsError | None = None
            try:
                update_tweet(data=data, tweet_uuid=tweet_uuid, user=request.user)

            except AccessDeniedError as err:
                error_message = err
                context = {"form": form, "error_message": error_message}
                return render(request, "update_tweet.html", context=context)

            except TagsError as err:
                error_message = err
                context = {"form": form, "error_message": error_message}
                return render(request, "update_tweet.html", context=context)

            return redirect("profile", profile_uuid=request.user.profile.pk)

        else:
            context = {"form": form}
            return render(request, "update_tweet.html", context=context)


class DeleteTweetView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, tweet_uuid: UUID) -> HttpResponse:
        try:
            delete_tweet(tweet_uuid=tweet_uuid, user=request.user)
        except AccessDeniedError:
            return redirect("index")

        current_page = request.META.get("HTTP_REFERER")
        return redirect(current_page)


class DeleteRetweetView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, retweet_pk: int) -> HttpResponse:
        try:
            delete_retweet(retweet_pk=retweet_pk, user=request.user)
        except AccessDeniedError:
            return redirect("index")

        current_page = request.META.get("HTTP_REFERER")
        return redirect(current_page)
