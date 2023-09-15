from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from accounts.presentation.web.forms import LoginForm
from core.business_logic.dto import LoginDTO
from core.business_logic.exceptions import InvalidAuthCredentials
from core.business_logic.services import authenticate_user
from core.presentation.common import convert_data_from_request_to_dto
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View


class LoginView(View):
    """
    Controller for user authentication.

    Supports both GET and POST requests.

    If the user is already authenticated, it redirects to the main page of the website.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("index")

        form = LoginForm()
        context = {"form": form}
        return render(request, "login.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm(request.POST)

        if form.is_valid():
            data = convert_data_from_request_to_dto(dto=LoginDTO, data_from_form=form.cleaned_data)

            try:
                user = authenticate_user(data=data)
            except InvalidAuthCredentials as err:
                error_message = err
                context = {"form": form, "error_message": error_message}
                return render(request, "login.html", context=context)

            login(request=request, user=user)

            return redirect("index")

        else:
            context = {"form": form}
            return render(request, "login.html", context=context)
