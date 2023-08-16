from datetime import date
from typing import Any

from django.core.exceptions import ValidationError


class ValidateMinAge:
    def __init__(self, min_age: int) -> None:
        self._min_age = min_age

    def __call__(self, date: date) -> Any:
        age = (date.today() - date).days / 365
        if self._min_age > age:
            raise ValidationError(f"The minimum allowable age is {self._min_age} years.")


class ValidateMaxAge:
    def __init__(self, max_age: int) -> None:
        self._max_age = max_age

    def __call__(self, date: date) -> Any:
        age = (date.today() - date).days / 365
        if self._max_age < age:
            raise ValidationError(f"The maximum allowable age is {self._max_age} years.")
