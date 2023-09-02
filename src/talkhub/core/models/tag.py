from django.db import models

from .base import BaseModel


class Tag(BaseModel):
    """
    Storage of unique tags.
    """

    name = models.CharField(max_length=30, unique=True, verbose_name="tag")

    class Meta:
        verbose_name_plural = "tags"

    def __str__(self) -> str:
        return f"{self.name}"
