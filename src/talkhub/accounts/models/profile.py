from core.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models


class Profile(BaseModel):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to="avatar/", null=True, blank=True)
    about = models.CharField(max_length=400, null=True, blank=True)
    country = models.ForeignKey(
        to="Country",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="profiles",
        related_query_name="profile",
    )
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
        related_query_name="profile",
    )
    followings = models.ManyToManyField(
        to="self", symmetrical=False, related_name="profiles", related_query_name="profile", blank=True
    )

    class Meta:
        verbose_name_plural = "profiles"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}. User ID: {self.user_id}"
