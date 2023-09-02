from dataclasses import dataclass
from uuid import UUID


@dataclass
class FollowingsDTO:
    profile_id: UUID
    to_profile_id: UUID
