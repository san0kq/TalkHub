from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from ..dto import UserDTO

from accounts.models import Country, Profile
from core.models import Config
from django.contrib.auth import get_user_model
from django.db import transaction


class UserDAO:
    def create(self, data: UserDTO) -> None:
        with transaction.atomic():
            user_model = get_user_model()
            user = user_model.objects.create_user(
                email=data.email,
                username=data.username,
                password=data.password,
                date_of_birth=data.date_of_birth,
            )

            country = Country.objects.order_by("?").first()
            Profile.objects.create(
                first_name=data.first_name,
                last_name=data.last_name,
                about=data.about,
                user=user,
                country=country,
            )
            user.is_active = True
            user.save()
            Config.objects.create(tweets_order="-created_at", user=user)

    def get_user_ids_list(self) -> list[int]:
        user_model = get_user_model()
        result = user_model.objects.values_list("pk", flat=True)
        return result

    def get_profile_ids_list(self) -> list[UUID]:
        result = Profile.objects.values_list("pk", flat=True)
        return result
