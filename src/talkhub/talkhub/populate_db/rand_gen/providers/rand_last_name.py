from typing import Optional

from .rand_base import AbstractBase
from .tokens import lastnames_tokens


class RandLastName(AbstractBase):
    def __init__(self) -> None:
        self._tokens = lastnames_tokens.tokens

    def generate(self, length: Optional[int]) -> str:
        return self._result(length=length)
