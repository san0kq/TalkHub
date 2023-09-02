from django.db import models

from .base import BaseModel


class Rating(BaseModel):
    """
    Rating type model. Currently stores likes and dislikes. It can be extended.
    """

    name = models.CharField(max_length=7, unique=True, verbose_name="rating")

    class Meta:
        verbose_name_plural = "ratings"

    def __str__(self) -> str:
        return f"{self.name}"
