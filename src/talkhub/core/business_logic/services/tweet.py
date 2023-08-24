from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import BooleanField, Count, Value

if TYPE_CHECKING:
    from accounts.models import User
    from core.business_logic.dto import CreateTweetDTO

from core.models import Config, Tweet


def get_tweets(user: User) -> list[Tweet]:
    order_by = Config.objects.get(user=user).tweets_order
    tweets = (
        Tweet.objects.select_related("user__profile", "parent_tweet")
        .prefetch_related("retweets")
        .annotate(
            rating_count=Count("rating"),
            retweet_count=Count("retweet"),
            reply_count=Count("tweet"),
            is_retweet=Value(False, output_field=BooleanField()),
        )
        .all()
    )
    retweets = tweets.filter(retweet__isnull=False).annotate(is_retweet=Value(True, output_field=BooleanField()))
    tweets = tweets.union(retweets, all=True).order_by(order_by)

    return list(tweets)


def create_tweet(data: CreateTweetDTO, user: User) -> None:
    Tweet.objects.create(text=data.text, user=user)
