from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseModel


class Config(BaseModel):
    """
    User settings storage model. It can be extended.
    """

    tweets_order = models.CharField(max_length=20)
    user = models.OneToOneField(
        to=get_user_model(), related_name="config", related_query_name="config", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "configs"

    def __str__(self) -> str:
        return f"User ID {self.user.pk} config"
