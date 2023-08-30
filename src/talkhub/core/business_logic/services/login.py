from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from django.contrib.auth import authenticate

if TYPE_CHECKING:
    from core.business_logic.dto import LoginDTO
    from django.contrib.auth.models import AbstractBaseUser

from core.business_logic.exceptions import InvalidAuthCredentials

logger = getLogger(__name__)


def authenticate_user(data: LoginDTO) -> AbstractBaseUser:
    user = authenticate(email=data.email, password=data.password)
    if user:
        logger.info("Successfully login", extra={"email": data.email})
        return user
    else:
        logger.error("Invalid credentials", extra={"email": data.email})
        raise InvalidAuthCredentials("Invalid credentials.")
