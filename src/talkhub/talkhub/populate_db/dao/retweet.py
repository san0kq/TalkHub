from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dto import RetweetDTO

from core.models import Retweet, Tweet
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction


class RetweetDAO:
    def create(self, data: RetweetDTO) -> None:
        with transaction.atomic():
            user_model = get_user_model()
            user = user_model.objects.get(pk=data.user_id)
            tweet = Tweet.objects.get(pk=data.tweet_id)

            if tweet.user == user:
                raise IntegrityError

            Retweet.objects.create(user=user, tweet=tweet)
            tweet.retweet_count += 1
            tweet.save()
