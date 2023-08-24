from __future__ import annotations

import time
import uuid
from logging import getLogger
from typing import TYPE_CHECKING

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

if TYPE_CHECKING:
    from accounts.models import User

from accounts.models import EmailConfirmationCode
from core.business_logic.exceptions import ConfirmationCodeExpired, ConfirmationCodeNotExists

logger = getLogger(__name__)


def send_confirm_code(user: User, email: str) -> None:
    confirmation_code = str(uuid.uuid4())
    code_expiration_time = int(time.time()) + settings.CONFIRMATION_CODE_LIFETIME

    if EmailConfirmationCode.objects.filter(user=user).exists():
        EmailConfirmationCode.objects.filter(user=user).delete()
    EmailConfirmationCode.objects.create(code=confirmation_code, user=user, expiration=code_expiration_time)

    confirmation_url = (
        settings.SERVER_HOST + reverse("confirm-signup") + f"?code={confirmation_code}" + f"&email={email}"
    )
    send_mail(
        subject="Confirm your email",
        message=f"Please confirm email by clicking the link below:\n\n{confirmation_url}",
        from_email=settings.EMAIL_FROM,
        recipient_list=[email],
    )


def confirm_user_email(confirmation_code: str, email: str) -> None:
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

    if user.is_active:
        user.email = email
    else:
        user.is_active = True

    user.save()
    code_data.delete()
