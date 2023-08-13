from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseModel


class Tweet(BaseModel):
    text = models.CharField(max_length=400)
    user = models.ForeignKey(
        to=get_user_model(), related_name="tweets", related_query_name="tweet", on_delete=models.CASCADE
    )
    parent_tweet = models.ForeignKey(
        to="self", null=True, blank=True, related_name="tweets", related_query_name="tweet", on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(to="Tag", related_name="tweets", related_query_name="tweet")

    class Meta:
        verbose_name_plural = "tweets"

    def __str__(self) -> str:
        return f"Tweet ID: {self.pk} | User ID: {self.user_id.pk}"
