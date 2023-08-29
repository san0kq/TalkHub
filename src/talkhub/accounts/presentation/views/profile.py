from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponseBadRequest

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest
    from uuid import UUID

from accounts.presentation.forms import ProfileEditForm, SearchProfileForm
from core.business_logic.dto import ProfileEditDTO, ProfileFollowDTO, SearchProfileDTO
from core.business_logic.exceptions import EmailAlreadyExistsError, PageDoesNotExists, UsernameAlreadyExistsError
from core.business_logic.services import (
    get_profile,
    initial_profile_form,
    paginate_pages,
    profile_edit,
    profile_follow,
    profile_followers,
    profile_followings,
    profile_unfollow,
    search_profile,
)
from core.presentation.converters import convert_data_from_form_to_dto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View


class ProfileView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, profile_uuid: UUID) -> HttpResponse:
        profile, profile_tweets = get_profile(profile_uuid=profile_uuid)

        try:
            tweets_paginated, prev_page, next_page = paginate_pages(request=request, data=profile_tweets, per_page=20)

        except PageDoesNotExists as err:
            return HttpResponseBadRequest(content=err)

        context = {"profile": profile, "tweets": tweets_paginated, "next_page": next_page, "prev_page": prev_page}

        return render(request, "profile.html", context=context)


class ProfileEditView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        initial_data = initial_profile_form(user_pk=user.pk)
        form = ProfileEditForm(initial=initial_data)
        context = {"form": form}
        return render(request, "profile_edit.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        form = ProfileEditForm(request.POST, files=request.FILES)

        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=ProfileEditDTO, data_from_form=form.cleaned_data)
            error_message: Exception | None = None

            try:
                profile_edit(data=data, user_pk=user.pk)

            except UsernameAlreadyExistsError as err:
                error_message = err
                context = {"form": form, "error_message": error_message}
                return render(request, "profile_edit.html", context=context)

            except EmailAlreadyExistsError as err:
                error_message = err
                context = {"form": form, "error_message": error_message}
                return render(request, "profile_edit.html", context=context)

            return redirect("profile", profile_uuid=user.profile.pk)

        else:
            context = {"form": form}
            return render(request, "profile_edit.html", context=context)


class FollowProfileView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, profile_uuid: UUID) -> HttpResponse:
        data = ProfileFollowDTO(user=request.user, profile_uuid=profile_uuid)
        profile_follow(data=data)
        return redirect("profile", profile_uuid=profile_uuid)


class UnfollowProfileView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, profile_uuid: UUID) -> HttpResponse:
        data = ProfileFollowDTO(user=request.user, profile_uuid=profile_uuid)
        profile_unfollow(data=data)
        return redirect("profile", profile_uuid=profile_uuid)


class ProfileFollowingsView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, profile_uuid: UUID) -> HttpResponse:
        followings = profile_followings(profile_uuid=profile_uuid)

        try:
            followings_paginated, prev_page, next_page = paginate_pages(request=request, data=followings, per_page=20)

        except PageDoesNotExists as err:
            return HttpResponseBadRequest(content=err)

        context = {"followings_paginated": followings_paginated, "prev_page": prev_page, "next_page": next_page}
        return render(request, "followings.html", context=context)


class ProfileFollowersView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest, profile_uuid: UUID) -> HttpResponse:
        followers = profile_followers(profile_uuid=profile_uuid)

        try:
            followers_paginated, prev_page, next_page = paginate_pages(request=request, data=followers, per_page=20)

        except PageDoesNotExists as err:
            return HttpResponseBadRequest(content=err)

        context = {"followers_paginated": followers_paginated, "prev_page": prev_page, "next_page": next_page}
        return render(request, "followers.html", context=context)


class SearchProfileView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        form = SearchProfileForm(request.GET)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=SearchProfileDTO, data_from_form=form.cleaned_data)
            profiles = search_profile(data=data)
            form = SearchProfileForm()

            if profiles:
                try:
                    profiles_paginated, prev_page, next_page = paginate_pages(
                        request=request, data=profiles, per_page=20
                    )

                except PageDoesNotExists as err:
                    return HttpResponseBadRequest(content=err)

                context = {
                    "form": form,
                    "profiles_paginated": profiles_paginated,
                    "prev_page": prev_page,
                    "next_page": next_page,
                    "first_name": data.first_name,
                    "last_name": data.last_name,
                    "username": data.username,
                }
            else:
                context = {"form": form}
            return render(request, "search_profile.html", context=context)
        else:
            return None
