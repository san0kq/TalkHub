from random import choice, randint
from string import digits

from .rand_base import AbstractBase


class RandBankCard(AbstractBase):
    def __init__(self):
        self.card_number = str()

    def _result(self, length: None = None) -> str:
        self.card_number = ""
        for _ in range(15):
            self.card_number += choice(digits)
        sum_of_digits = 0
        for index, number_str in enumerate(self.card_number):
            if index % 2 == 0:
                number = int(number_str) * 2
                if number > 9:
                    number -= 9
            sum_of_digits += int(number_str)

        if sum_of_digits % 10 == 0:  # add a check digit
            self.card_number += "0"
        else:
            self.card_number += str(10 - sum_of_digits % 10)

        return self.card_number

    def generate(self, length: None) -> str:
        if length:
            raise ValueError("The provider RandBankCard does not support the " "phone number length.")
        return self._result()
