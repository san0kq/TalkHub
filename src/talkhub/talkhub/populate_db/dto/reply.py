from dataclasses import dataclass
from uuid import UUID


@dataclass
class ReplyDTO:
    tweet_id: UUID
    user_id: int
    text: str
    tags: str
