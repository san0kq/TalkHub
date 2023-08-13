from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseModel


class TweetRating(BaseModel):
    tweet = models.ForeignKey(to="Tweet", related_name="ratings", related_query_name="rating", on_delete=models.CASCADE)
    rating = models.ForeignKey(
        to="Rating", related_name="ratings", related_query_name="rating", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=get_user_model(), related_name="ratings", related_query_name="rating", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "tweet_ratings"
        unique_together = ("tweet_id", "user_id")

    def __str__(self) -> str:
        return f"From user ID {self.user.pk} {self.rating.name} to tweet {self.tweet.pk}"
