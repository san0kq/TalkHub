from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..dto import FollowingsDTO

from accounts.models import Profile
from django.db import transaction


class FollowersDAO:
    def create(self, data: FollowingsDTO) -> None:
        with transaction.atomic():
            profile = Profile.objects.get(pk=data.profile_id)
            to_profile = Profile.objects.get(pk=data.to_profile_id)
            profile.followings.add(to_profile)
