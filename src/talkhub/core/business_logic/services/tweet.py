from __future__ import annotations

import re
from logging import getLogger
from typing import TYPE_CHECKING

from django.db import DataError, transaction
from django.db.models import BigIntegerField, BooleanField, CharField, Count, F, UUIDField, Value

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser
    from core.business_logic.dto import CreateTweetDTO
    from uuid import UUID

from core.business_logic.exceptions import AccessDeniedError, TagsError, TweetDoesNotExists
from core.models import Config, Notification, NotificationType, Rating, Retweet, Tag, Tweet, TweetRating

logger = getLogger(__name__)


def get_tweets(user: AbstractBaseUser) -> list[Tweet]:
    """
    Returns a list of all tweets and retweets made by users that
    the authenticated user is subscribed to.
    Annotations are added to gather additional data and distinguish between tweets and retweets.
    """
    order_by = Config.objects.get(user=user).tweets_order
    tweets = (
        Tweet.objects.select_related("user", "parent_tweet")
        .prefetch_related("retweets", "ratings", "tweets")
        .annotate(
            rating_count=Count("rating", distinct=True),
            reply_count=Count("tweet", distinct=True),
            is_retweet=Value(False, output_field=BooleanField()),
            retweet_first_name=Value("", CharField()),
            retweet_last_name=Value("", CharField()),
            retweet_profile_pk=Value(0, UUIDField()),
            retweet_pk=Value(0, BigIntegerField()),
            sort_date=F("created_at"),
        )
        .filter(user__profile__follower=user.profile)
        .filter(parent_tweet__isnull=True)
    )
    retweets = (
        Tweet.objects.select_related("user", "parent_tweet")
        .prefetch_related("retweets", "ratings", "tweets")
        .annotate(
            rating_count=Count("rating", distinct=True),
            reply_count=Count("tweet", distinct=True),
            is_retweet=Value(True, BooleanField()),
            retweet_first_name=F("retweet__user__profile__first_name"),
            retweet_last_name=F("retweet__user__profile__last_name"),
            retweet_profile_pk=F("retweet__user__profile__pk"),
            retweet_pk=F("retweet__pk"),
            sort_date=F("retweet__created_at"),
        )
        .filter(retweet__user__profile__in=user.profile.followings.all())
    )
    tweets = tweets.union(retweets, all=True).order_by(order_by)

    return list(tweets)


def create_tweet(data: CreateTweetDTO, user: AbstractBaseUser) -> None:
    """
    Function for creating a new tweet.

    It checks for the presence of hashtags in the text and saves them to
    the database if they don't already exist.
    It associates the new tweet with the hashtags.
    """
    with transaction.atomic():
        tags = re.findall(r"#\w+", data.text)
        if len(tags) > 20:
            logger.error("Max number of tags", extra={"username": user.username})
            raise TagsError("Maximum number of tags is 20.")
        try:
            tags = [Tag.objects.get_or_create(name=tag.lower()[1::])[0] for tag in tags]
        except DataError:
            logger.error("Max tag len", extra={"username": user.username})
            raise TagsError("The maximum tag length is 30 characters.")
        tweet = Tweet.objects.create(text=data.text, user=user)
        tweet.tags.set(tags)


def get_tweet_by_uuid(tweet_uuid: UUID) -> tuple[Tweet, list[Tweet]]:
    """
    Fetching information about a tweet and retrieving tweets that are replies to the parent tweet.
    """
    try:
        tweet = (
            Tweet.objects.select_related("user__profile")
            .annotate(
                rating_count=Count("rating", distinct=True),
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
            reply_count=Count("tweet", distinct=True),
        )
        .filter(parent_tweet=tweet)
        .order_by("-created_at")
    )
    return tweet, list(reply_tweets)


def tweet_like(tweet_uuid: UUID, user: AbstractBaseUser) -> None:
    """
    The function handles liking or unliking a post.

    It also creates or deletes an additional entry in the notifications model.
    """
    with transaction.atomic():
        tweet = Tweet.objects.get(pk=tweet_uuid)
        rating = Rating.objects.get(name="like")
        notification_type = NotificationType.objects.get(name="rating")

        if TweetRating.objects.filter(tweet=tweet, rating=rating, user=user).exists():
            TweetRating.objects.get(tweet=tweet, rating=rating, user=user).delete()
            notification = Notification.objects.get(tweet=tweet, user=user, notification_type=notification_type)
            notification.recipients.remove(tweet.user)
            notification.delete()
        else:
            TweetRating.objects.create(tweet=tweet, rating=rating, user=user)
            notification = Notification.objects.create(tweet=tweet, user=user, notification_type=notification_type)
            notification.recipients.add(tweet.user)


def create_reply(data: CreateTweetDTO, user: AbstractBaseUser, parent_tweet_uuid: UUID) -> None:
    """
    Creating a reply to a parent tweet.
    """
    with transaction.atomic():
        tags = re.findall(r"#\w+", data.text)

        if len(tags) > 20:
            logger.error("Max number of tags", extra={"username": user.username})
            raise TagsError("Maximum number of tags is 20.")
        try:
            tags = [Tag.objects.get_or_create(name=tag.lower()[1::])[0] for tag in tags]
        except DataError:
            logger.error("Max tag len", extra={"username": user.username})
            raise TagsError("The maximum tag length is 30 characters.")

        parent_tweet = Tweet.objects.get(pk=parent_tweet_uuid)
        tweet = Tweet.objects.create(text=data.text, user=user, parent_tweet=parent_tweet)
        tweet.tags.set(tags)


def create_retweet(user: AbstractBaseUser, tweet_uuid: UUID) -> None:
    """
    Creating a retweet and incrementing the retweet count in the Tweet model.
    """
    tweet = Tweet.objects.get(pk=tweet_uuid)
    Retweet.objects.create(tweet=tweet, user=user)
    tweet.retweet_count += 1
    tweet.save()


def initial_tweet_form(tweet_uuid: UUID) -> dict[str, str]:
    """
    Fetching the original data to populate a form when editing a tweet.
    """
    text = Tweet.objects.get(pk=tweet_uuid).text
    initial = {"text": text}
    return initial


def update_tweet(data: CreateTweetDTO, tweet_uuid: UUID, user: AbstractBaseUser) -> None:
    """
    Editing an existing tweet. Additionally, searching for hashtags in the
    text and performing actions related to them in the database.
    """
    with transaction.atomic():
        tweet = Tweet.objects.get(pk=tweet_uuid)
        if tweet.user != user:
            logger.error(
                "Tweet access denied",
                extra={"username": user.username, "tweet_id": tweet_uuid},
            )
            raise AccessDeniedError("You do not have access to this tweet.")

        new_tags = re.findall(r"#\w+", data.text)
        if len(new_tags) > 20:
            logger.error("Max number of tags", extra={"username": user.username})
            raise TagsError("Maximum number of tags is 20.")

        old_tags = tweet.tags.all()

        for tag in old_tags:
            if tag.name not in new_tags:
                tweet.tags.remove(tag)

        try:
            tags = [Tag.objects.get_or_create(name=tag.lower()[1::])[0] for tag in new_tags]
        except DataError:
            logger.error("Max tag len", extra={"username": user.username})
            raise TagsError("The maximum tag length is 30 characters.")

        logger_data = {
            "tweet_id": tweet_uuid,
            "old_text": tweet.text,
            "new_text": data.text,
        }
        tweet.text = data.text
        tweet.tags.set(tags)
        tweet.save()
        logger.info("Update tweet", extra=logger_data)


def delete_tweet(tweet_uuid: UUID, user: AbstractBaseUser) -> None:
    tweet = Tweet.objects.get(pk=tweet_uuid)
    if tweet.user != user:
        logger.error(
            "Tweet access denied",
            extra={"username": user.username, "tweet_id": tweet_uuid},
        )
        raise AccessDeniedError("You do not have access to this tweet.")
    logger_data = {"username": user.username, "tweet_text": tweet.text}
    tweet.delete()
    logger.info("Tweet deleted", extra=logger_data)


def delete_retweet(retweet_pk: int, user: AbstractBaseUser) -> None:
    """
    Deleting a retweet and decreasing the retweet count in the Tweet table.
    """
    retweet = Retweet.objects.get(pk=retweet_pk)
    if retweet.user != user:
        logger.error(
            "Retweet access denied",
            extra={"username": user.username, "retweet_id": retweet_pk},
        )
        raise AccessDeniedError("You do not have acces to this retweet.")
    logger_data = {"username": user.username, "retweet_id": retweet_pk}
    tweet = retweet.tweet
    retweet.delete()
    tweet.retweet_count -= 1
    tweet.save()
    logger.info("Retweet deleted", extra=logger_data)
