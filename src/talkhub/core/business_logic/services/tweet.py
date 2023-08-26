from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import BooleanField, Count, Q, Value

if TYPE_CHECKING:
    from accounts.models import User
    from core.business_logic.dto import CreateTweetDTO
    from uuid import UUID

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
        .filter(user__profile__follower=user.profile)
    )
    retweets = (
        Tweet.objects.select_related("user__profile", "parent_tweet")
        .prefetch_related("retweets")
        .annotate(
            rating_count=Count("rating"),
            retweet_count=Count("retweet"),
            reply_count=Count("tweet"),
            is_retweet=Value(True, output_field=BooleanField()),
        )
        .filter(Q(retweet__isnull=False) & Q(retweet__user__profile__in=user.profile.followings.all()))
    )
    tweets = tweets.union(retweets, all=True).order_by(order_by)

    return list(tweets)


def create_tweet(data: CreateTweetDTO, user: User) -> None:
    Tweet.objects.create(text=data.text, user=user)


def get_tweet_by_uuid(tweet_uuid: UUID) -> tuple[Tweet, list[Tweet]]:
    tweet = (
        Tweet.objects.select_related("user__profile")
        .annotate(
            rating_count=Count("rating"),
            retweet_count=Count("retweet"),
            reply_count=Count("tweet"),
        )
        .get(pk=tweet_uuid)
    )
    reply_tweets = (
        Tweet.objects.select_related("user__profile")
        .annotate(rating_count=Count("rating"), retweet_count=Count("retweet"), reply_count=Count("tweet"))
        .filter(parent_tweet=tweet)
        .order_by("-created_at")
    )
    return tweet, list(reply_tweets)
