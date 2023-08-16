from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views import View

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

from accounts.presentation.forms import RegistrationForm
from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import (
    ConfirmationCodeExpired,
    ConfirmationCodeNotExists,
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from core.business_logic.services import confirm_user_registration, create_user
from core.presentation.converters import convert_data_from_form_to_dto


class RegistrationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = RegistrationForm()
        context = {"form": form}
        return render(request, "registration.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data: RegistrationDTO = convert_data_from_form_to_dto(dto=RegistrationDTO, data_from_form=form.cleaned_data)
            error_message = None
            success_message: str | None = "Confirmation email sent. Please confirm it by the link."
            try:
                create_user(data=data)
            except EmailAlreadyExistsError:
                error_message = f"The email address {data.email} already exists."
                success_message = None
            except UsernameAlreadyExistsError:
                error_message = f"The username {data.username} already exists."
                success_message = None

            context = {"form": form, "success_message": success_message, "error_message": error_message}
            return render(request, "registration.html", context=context)
        else:
            return render(request, "registration.html", {"form": form})


class RegistrationConfirmationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        confirmation_code = request.GET["code"]
        try:
            confirm_user_registration(confirmation_code=confirmation_code)
        except ConfirmationCodeNotExists:
            return HttpResponseBadRequest(content="Invalid confirmation code.")
        except ConfirmationCodeExpired:
            return HttpResponseBadRequest(content="Confirmation code expired.")

        return redirect(to="login")
