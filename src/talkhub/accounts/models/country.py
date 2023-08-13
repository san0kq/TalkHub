from core.models import BaseModel
from django.db import models


class Country(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="country")

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self) -> str:
        return f"{self.name}"
