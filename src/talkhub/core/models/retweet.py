from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseModel


class Retweet(BaseModel):
    tweet = models.ForeignKey(
        to="Tweet", related_name="retweets", related_query_name="retweet", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=get_user_model(), related_name="retweets", related_query_name="retweet", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "retweets"
        unique_together = ("tweet", "user")

    def __str__(self) -> str:
        return f"Tweet ID: {self.tweet.pk}. User ID: {self.user.pk}"
