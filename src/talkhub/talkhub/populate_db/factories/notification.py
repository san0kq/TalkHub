from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from providers import RandomValueFromListProvider
    from rand_gen import RandGen

from ..dto import NotificationDTO


class NotificationFactory:
    def __init__(self, user_id_provider: RandomValueFromListProvider, text_provider: RandGen) -> None:
        self._user_id_provider = user_id_provider
        self._text_provider = text_provider

    def generate(self) -> NotificationDTO:
        return NotificationDTO(
            user_id=self._user_id_provider(), text=self._text_provider.generate(length=randint(3, 5))
        )
