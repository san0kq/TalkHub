from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dto import ReplyDTO

from core.models import Tag, Tweet
from django.contrib.auth import get_user_model
from django.db import DataError, IntegrityError, transaction


class ReplyDAO:
    def create(self, data: ReplyDTO) -> None:
        with transaction.atomic():
            user_model = get_user_model()
            user = user_model.objects.get(pk=data.user_id)
            tweet = Tweet.objects.get(pk=data.tweet_id)

            if data.tags:
                data.text = data.text + " " + data.tags

            tags = re.findall(r"#\w+", data.text)

            if len(tags) > 20:
                raise IntegrityError
            try:
                tags = [Tag.objects.get_or_create(name=tag.lower()[1::])[0] for tag in tags]
            except DataError:
                raise IntegrityError

            tweet = Tweet.objects.create(text=data.text, user=user, parent_tweet=tweet)
            tweet.tags.set(tags)
