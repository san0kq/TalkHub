from __future__ import annotations

import time
import uuid
from logging import getLogger
from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse

if TYPE_CHECKING:
    from accounts.models import User

from accounts.models import EmailConfirmationCode, Profile
from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import (
    ConfirmationCodeExpired,
    ConfirmationCodeNotExists,
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)

logger = getLogger(__name__)


def create_user(data: RegistrationDTO) -> None:
    logger.info("Get user creation request", extra={"user": data})

    user_model: User = get_user_model()

    if user_model.objects.filter(email=data.email).exists():
        raise EmailAlreadyExistsError
    if user_model.objects.filter(username=data.username).exists():
        raise UsernameAlreadyExistsError

    created_user = user_model.objects.create_user(
        email=data.email, password=data.password, username=data.username, date_of_birth=data.date_of_birth
    )
    confirmation_code = str(uuid.uuid4())
    code_expiration_time = int(time.time()) + settings.CONFIRMATION_CODE_LIFETIME

    EmailConfirmationCode.objects.create(code=confirmation_code, user=created_user, expiration=code_expiration_time)

    confirmation_url = settings.SERVER_HOST + reverse("confirm-signup") + f"?code={confirmation_code}"
    send_mail(
        subject="Confirm your email",
        message=f"Please confirm email by clicking the link below:\n\n{confirmation_url}",
        from_email=settings.EMAIL_FROM,
        recipient_list=[data.email],
    )


def confirm_user_registration(confirmation_code: str) -> None:
    try:
        code_data = EmailConfirmationCode.objects.get(code=confirmation_code)
    except EmailConfirmationCode.DoesNotExist as err:
        logger.error("Provided code doesn't exists.", exc_info=err, extra={"code": confirmation_code})
        raise ConfirmationCodeNotExists

    if time.time() > code_data.expiration:
        logger.info(
            "Provided expiration code expired.",
            extra={"current_time": str(time.time()), "code_expiration": str(code_data.expiration)},
        )
        raise ConfirmationCodeExpired

    user = code_data.user
    user.is_active = True
    user.save()
    Profile.objects.create(user=user)
    code_data.delete()
