from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from providers import RandomValueFromListProvider
    from rand_gen import RandGen

from ..dto import ReplyDTO


class ReplyFactory:
    def __init__(
        self,
        user_id_provider: RandomValueFromListProvider,
        tweet_id_provider: RandomValueFromListProvider,
        text_provider: RandGen,
        tag_provider: RandGen,
    ) -> None:
        self._user_id_provider = user_id_provider
        self._tweet_id_provider = tweet_id_provider
        self._text_provider = text_provider
        self._tag_provider = tag_provider

    def generate(self) -> ReplyDTO:
        tags = ["#" + self._tag_provider.generate(length=randint(3, 10)) for _ in range(randint(0, 10))]
        tags = " ".join(tags)
        return ReplyDTO(
            user_id=self._user_id_provider(),
            tweet_id=self._tweet_id_provider(),
            text=self._text_provider.generate(length=randint(5, 20)),
            tags=tags,
        )
