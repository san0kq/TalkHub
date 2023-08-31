from __future__ import annotations

from datetime import date
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rand_gen import RandGen

from ..dto import UserDTO


class UserFactory:
    def __init__(
        self,
        username_provider: RandGen,
        email_profiver: RandGen,
        password_provider: RandGen,
        first_name_provider: RandGen,
        last_name_profivder: RandGen,
        about_provider: RandGen,
    ) -> None:
        self._username_provider = username_provider
        self._email_provider = email_profiver
        self._password_provider = password_provider
        self._first_name_provider = first_name_provider
        self._last_name_provider = last_name_profivder
        self._about_provider = about_provider

    def generate(self) -> UserDTO:
        return UserDTO(
            email=self._email_provider.generate(length=randint(5, 20)),
            username=self._username_provider.generate(length=randint(5, 12)),
            date_of_birth=date(randint(1930, 2004), randint(1, 12), randint(1, 28)),
            password=self._password_provider.generate(length=randint(5, 20)),
            first_name=self._first_name_provider.generate(length=(randint(3, 10))),
            last_name=self._last_name_provider.generate(length=(randint(3, 10))),
            about=self._about_provider.generate(length=randint(5, 20)),
        )
