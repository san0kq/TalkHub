from __future__ import annotations

import re
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from ..dto import TweetDTO

from core.models import Tag, Tweet
from django.contrib.auth import get_user_model
from django.db import DataError, IntegrityError, transaction


class TweetDAO:
    def create(self, data: TweetDTO) -> None:
        with transaction.atomic():
            user_model = get_user_model()
            user = user_model.objects.get(pk=data.user_id)

            if data.tags:
                data.text = data.text + " " + data.tags

            tags = re.findall(r"#\w+", data.text)

            if len(tags) > 20:
                raise IntegrityError
            try:
                tags = [Tag.objects.get_or_create(name=tag.lower()[1::])[0] for tag in tags]
            except DataError:
                raise IntegrityError

            tweet = Tweet.objects.create(text=data.text, user=user)
            tweet.tags.set(tags)

    def get_tweet_ids_list(self) -> list[UUID]:
        result: list[UUID] = Tweet.objects.values_list("pk", flat=True)
        return result
