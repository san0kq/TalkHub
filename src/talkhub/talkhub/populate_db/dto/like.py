from dataclasses import dataclass
from uuid import UUID


@dataclass
class LikeDTO:
    user_id: int
    tweet_id: UUID
