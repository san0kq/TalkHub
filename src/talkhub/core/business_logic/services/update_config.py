from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from accounts.models import User

from core.models import Config


def update_config(user: User, option: str) -> None:
    if option == "Ratings count":
        option = "-rating_count"
    elif option == "Date of published":
        option = "-created_at"
    config = Config.objects.get(user=user)
    config.tweets_order = option
    config.save()
