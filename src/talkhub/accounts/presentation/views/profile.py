from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponseBadRequest

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest

from accounts.presentation.forms import ProfileEditForm
from core.business_logic.dto import ProfileEditDTO
from core.business_logic.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from core.business_logic.services import get_profile, initial_profile_form, profile_edit
from core.presentation.converters import convert_data_from_form_to_dto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import redirect, render
from django.views import View


class ProfileView(LoginRequiredMixin, View):
    login_url = "signin"

    def get(self, request: HttpRequest) -> HttpResponse:
        user = request.user

        try:
            page_number = request.GET["page"]
        except KeyError:
            page_number = 1

        profile, profile_tweets = get_profile(user=user)

        paginator = Paginator(profile_tweets, 20)

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

            return redirect("profile")

        else:
            context = {"form": form}
            return render(request, "profile_edit.html", context=context)
