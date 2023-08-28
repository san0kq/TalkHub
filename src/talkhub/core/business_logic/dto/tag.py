from dataclasses import dataclass

from django.contrib.auth.models import AbstractBaseUser


@dataclass
class SearchTagDTO:
    name: str


@dataclass
class TrendingDTO:
    user: AbstractBaseUser
