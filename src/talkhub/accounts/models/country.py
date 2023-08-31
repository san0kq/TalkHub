from core.models import BaseModel
from django.db import models


class Country(BaseModel):
    """
    The model is about countries. It is automatically filled in migrations.
    """

    name = models.CharField(max_length=50, unique=True, verbose_name="country")

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self) -> str:
        return f"{self.name}"
