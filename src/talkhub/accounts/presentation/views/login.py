from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from accounts.presentation.forms import LoginForm
from core.business_logic.dto import LoginDTO
from core.business_logic.exceptions import InvalidAuthCredentials
from core.business_logic.services import authenticate_user
from core.presentation.converters import convert_data_from_form_to_dto
from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm()
        context = {"form": form}
        return render(request, "login.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm(request.POST)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=LoginDTO, data_from_form=form.cleaned_data)

            try:
                user = authenticate_user(data=data)
            except InvalidAuthCredentials:
                return HttpResponseBadRequest("Invalid credentials.")

            login(request=request, user=user)

            return redirect("index")

        else:
            context = {"form": form}
            return render(request, "login.html", context=context)
