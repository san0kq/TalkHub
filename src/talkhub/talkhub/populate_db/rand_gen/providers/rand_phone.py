from random import choice, randint

from .rand_base import AbstractBase


class RandPhone(AbstractBase):
    def __init__(self):
        self.operators = (
            "+37533",
            "+37529",
            "+37544",
            "+37524",
            "+37525",
            "+37515",
            "+37516",
            "+37517",
            "+37521",
            "+37522",
            "+37523",
        )

    def _result(self, length: None = None) -> str:
        result = choice(self.operators)
        for _ in range(7):
            result += str(randint(0, 9))
        return result

    def generate(self, length: None) -> str:
        if length:
            raise ValueError("The provider RandPhone does not support the " "phone number length.")
        return self._result()
