from abc import ABC, abstractmethod
from random import choice
from typing import Optional


class AbstractBase(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def _first_token(self) -> str:
        return choice(list(filter(lambda x: x[0].isupper(), self._tokens.keys())))

    def _result(self, length: Optional[int]) -> str:
        if not length:
            length = 7
        elif not isinstance(length, int) or not 0 < length <= 20:
            raise ValueError("Length should be a integer in range (1, 20).")
        rand_value = self._first_token()
        while len(rand_value) < length:
            rand_token = choice(list(filter(lambda x: x[1] != " ", self._tokens[rand_value[-2:]])))
            if len(rand_value) == length - 1 and length % 2 != 0:
                if any(x[1] == " " for x in self._tokens[rand_value[-2:]]):
                    rand_token = choice(list(filter(lambda x: x[1] == " ", self._tokens[rand_value[-2:]])))

            rand_value += rand_token
        return rand_value[:length]
