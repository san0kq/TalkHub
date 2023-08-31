from random import choice
from typing import Optional

from .rand_base import AbstractBase
from .tokens import emails_tokens


class RandEmail(AbstractBase):
    def __init__(self) -> None:
        self._tokens = emails_tokens.tokens
        self._emails = [
            "@gmail.com",
            "@yandex.ru",
            "@ya.ru",
            "@mail.ru",
            "@rambler.ru",
        ]

    def _first_token(self) -> str:
        return choice(list(self._tokens.keys()))

    def generate(self, length: Optional[int]) -> str:
        return self._result(length=length) + choice(self._emails)
