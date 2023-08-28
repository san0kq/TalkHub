from __future__ import annotations

import re
from typing import TYPE_CHECKING

from django.db import DataError, IntegrityError, transaction
from django.db.models import BooleanField, Count, Q, Value

if TYPE_CHECKING:
    from accounts.models import User
    from core.business_logic.dto import CreateTweetDTO
    from uuid import UUID

from core.business_logic.exceptions import AccessDeniedError, TagsError, TweetDoesNotExists
from core.models import Config, Notification, NotificationType, Rating, Retweet, Tag, Tweet, TweetRating


def get_tweets(user: User) -> list[Tweet]:
    order_by = Config.objects.get(user=user).tweets_order
    tweets = (
        Tweet.objects.select_related("user__profile", "parent_tweet")
        .prefetch_related("retweets")
        .annotate(
            rating_count=Count("rating", distinct=True),
            retweet_count=Count("retweet", distinct=True),
            reply_count=Count("tweet", distinct=True),
            is_retweet=Value(False, output_field=BooleanField()),
        )
        .filter(user__profile__follower=user.profile)
    )
    retweets = (
        Tweet.objects.select_related("user__profile", "parent_tweet")
        .prefetch_related("retweets")
        .annotate(
            rating_count=Count("rating", distinct=True),
            retweet_count=Count("retweet", distinct=True),
            reply_count=Count("tweet", distinct=True),
            is_retweet=Value(True, output_field=BooleanField()),
        )
        .filter(Q(retweet__isnull=False) & Q(retweet__user__profile__in=user.profile.followings.all()))
    )
    tweets = tweets.union(retweets, all=True).order_by(order_by)

    return list(tweets)


def create_tweet(data: CreateTweetDTO, user: User) -> None:
    with transaction.atomic():
        tags = re.findall(r"#\w+", data.text)
        if len(tags) > 20:
            raise TagsError("Maximum number of tags is 20.")
        try:
            tags = [Tag.objects.get_or_create(name=tag.lower()[1::])[0] for tag in tags]
        except DataError:
            raise TagsError("The maximum tag length is 30 characters.")
        tweet = Tweet.objects.create(text=data.text, user=user)
        tweet.tags.set(tags)


def get_tweet_by_uuid(tweet_uuid: UUID) -> tuple[Tweet, list[Tweet]]:
    try:
        tweet = (
            Tweet.objects.select_related("user__profile")
            .annotate(
                rating_count=Count("rating", distinct=True),
                retweet_count=Count("retweet", distinct=True),
                reply_count=Count("tweet", distinct=True),
            )
            .get(pk=tweet_uuid)
        )
    except Tweet.DoesNotExist:
        raise TweetDoesNotExists("Tweet does not exists.")

    reply_tweets = (
        Tweet.objects.select_related("user__profile")
        .annotate(
            rating_count=Count("rating", distinct=True),
            retweet_count=Count("retweet", distinct=True),
            reply_count=Count("tweet", distinct=True),
        )
        .filter(parent_tweet=tweet)
        .order_by("-created_at")
    )
    return tweet, list(reply_tweets)


def tweet_like(tweet_uuid: UUID, user: User) -> None:
    with transaction.atomic():
        tweet = Tweet.objects.get(pk=tweet_uuid)
        rating = Rating.objects.get(name="like")
        notification_type = NotificationType.objects.get(name="rating")
        try:
            TweetRating.objects.create(tweet=tweet, rating=rating, user=user)
            notification = Notification.objects.create(tweet=tweet, user=user, notification_type=notification_type)
            notification.recipients.add(tweet.user)
        except IntegrityError:
            TweetRating.objects.get(tweet=tweet, rating=rating, user=user).delete()


def create_reply(data: CreateTweetDTO, user: User, parent_tweet_uuid: UUID) -> None:
    parent_tweet = Tweet.objects.get(pk=parent_tweet_uuid)
    Tweet.objects.create(text=data.text, user=user, parent_tweet=parent_tweet)


def create_retweet(user: User, tweet_uuid: UUID) -> None:
    tweet = Tweet.objects.get(pk=tweet_uuid)
    Retweet.objects.create(tweet=tweet, user=user)


def initial_tweet_form(tweet_uuid: UUID) -> dict[str, str]:
    text = Tweet.objects.get(pk=tweet_uuid).text
    initial = {"text": text}
    return initial


def update_tweet(data: CreateTweetDTO, tweet_uuid: UUID, user: User) -> None:
    with transaction.atomic():
        tweet = Tweet.objects.get(pk=tweet_uuid)
        if tweet.user != user:
            raise AccessDeniedError("You do not have access to this tweet.")

        new_tags = re.findall(r"#\w+", data.text)
        if len(new_tags) > 20:
            raise TagsError("Maximum number of tags is 20.")

        old_tags = tweet.tags.all()

        for tag in old_tags:
            if tag.name not in new_tags:
                tweet.tags.remove(tag)

        try:
            tags = [Tag.objects.get_or_create(name=tag.lower()[1::])[0] for tag in new_tags]
        except DataError:
            raise TagsError("The maximum tag length is 30 characters.")

        tweet.text = data.text
        tweet.tags.set(tags)
        tweet.save()


def delete_tweet(tweet_uuid: UUID, user: User) -> None:
    tweet = Tweet.objects.get(pk=tweet_uuid)
    if tweet.user != user:
        raise AccessDeniedError("You do not have access to this tweet.")
    Tweet.objects.filter(pk=tweet_uuid).delete()
