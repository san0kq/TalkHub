from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import authenticate

if TYPE_CHECKING:
    from core.business_logic.dto import LoginDTO
    from django.contrib.auth.models import AbstractBaseUser

from core.business_logic.exceptions import InvalidAuthCredentials


def authenticate_user(data: LoginDTO) -> AbstractBaseUser:
    user = authenticate(email=data.email, password=data.password)
    if user:
        return user
    else:
        raise InvalidAuthCredentials
