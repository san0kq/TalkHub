from random import choice
from typing import Optional

from .rand_base import AbstractBase
from .tokens import text_tokens


class RandText(AbstractBase):
    def __init__(self) -> None:
        self._tokens = text_tokens.tokens

    def _result(self, length: Optional[int]) -> str:
        if not length:
            length = 7
        elif not isinstance(length, int) or not 0 < length <= 20:
            raise ValueError("Length should be a integer in range (1, 20).")
        random_value = self._first_token()
        while len(random_value.split()) < length:
            random_token = choice(self._tokens[random_value.split()[-1]])

            random_value += f" {random_token}"

        if random_value[-1] == ",":
            random_value = random_value[:-1] + "."
        elif random_value[-1] != ".":
            random_value = random_value + "."

        return random_value

    def generate(self, length: Optional[int]) -> str:
        return self._result(length=length)
