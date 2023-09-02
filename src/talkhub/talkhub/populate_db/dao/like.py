from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dto import LikeDTO

from core.models import Notification, NotificationType, Rating, Tweet, TweetRating
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction


class LikeDAO:
    def create(self, data: LikeDTO) -> None:
        with transaction.atomic():
            user_model = get_user_model()
            user = user_model.objects.get(pk=data.user_id)
            tweet = Tweet.objects.get(pk=data.tweet_id)
            rating = Rating.objects.get(name="like")
            notification_type = NotificationType.objects.get(name="rating")

            if tweet.user == user:
                raise IntegrityError

            TweetRating.objects.create(tweet=tweet, user=user, rating=rating)
            notification = Notification.objects.create(tweet=tweet, user=user, notification_type=notification_type)
            notification.recipients.add(tweet.user)
