from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from accounts.models import User

from accounts.models import Profile
from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import EmailAlreadyExistsError, UsernameAlreadyExistsError
from core.business_logic.services.confirm_email import send_confirm_code
from core.models import Config

logger = getLogger(__name__)


def create_user(data: RegistrationDTO) -> None:
    logger.info("Get user creation request", extra={"user": data})

    user_model: User = get_user_model()

    if user_model.objects.filter(email=data.email).exists():
        logger.error("Email already exists", extra={"email": data.email})
        raise EmailAlreadyExistsError
    if user_model.objects.filter(username=data.username).exists():
        logger.error("Username already exists", extra={"username": data.username})
        raise UsernameAlreadyExistsError

    created_user = user_model.objects.create_user(
        email=data.email, password=data.password, username=data.username, date_of_birth=data.date_of_birth
    )
    Config.objects.create(tweets_order="-created_at", user=created_user)
    Profile.objects.create(user=created_user)
    logger.info("Register user", extra={"user_id": created_user.pk})
    send_confirm_code(user=created_user, email=data.email)
