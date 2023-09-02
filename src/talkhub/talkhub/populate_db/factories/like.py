from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from providers import RandomValueFromListProvider

from ..dto import LikeDTO


class LikeFactory:
    def __init__(
        self, user_id_provider: RandomValueFromListProvider, tweet_id_provider: RandomValueFromListProvider
    ) -> None:
        self._user_id_provider = user_id_provider
        self._tweet_id_provider = tweet_id_provider

    def generate(self) -> LikeDTO:
        return LikeDTO(user_id=self._user_id_provider(), tweet_id=self._tweet_id_provider())
