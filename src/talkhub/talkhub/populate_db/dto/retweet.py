from dataclasses import dataclass
from uuid import UUID


@dataclass
class RetweetDTO:
    tweet_id: UUID
    user_id: int
