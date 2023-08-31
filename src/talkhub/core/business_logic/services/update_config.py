from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

from core.models import Config


def update_config(user: AbstractBaseUser, option: str) -> None:
    """
    Changing the user's configuration to choose between two types of
    tweet sorting on the main page.
    If a specific option is selected in the HTML, its equivalent value is
    recorded in the database for the particular user and saved there for tweet sorting.
    """
    if option == "Ratings count":
        option = "-rating_count"
    elif option == "Date of published":
        option = "-sort_date"
    config = Config.objects.get(user=user)
    config.tweets_order = option
    config.save()
