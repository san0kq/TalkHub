from dataclasses import dataclass


@dataclass
class TweetDTO:
    text: str
    user_id: int
    tags: str
