from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from providers import RandomValueFromListProvider

from ..dto import FollowingsDTO


class FollowingsFactory:
    def __init__(self, profile_id_provider: RandomValueFromListProvider) -> None:
        self._profile_id_provider = profile_id_provider

    def generate(self) -> FollowingsDTO:
        return FollowingsDTO(profile_id=self._profile_id_provider(), to_profile_id=self._profile_id_provider())
