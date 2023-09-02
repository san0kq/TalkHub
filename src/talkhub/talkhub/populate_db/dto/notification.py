from dataclasses import dataclass


@dataclass
class NotificationDTO:
    user_id: int
    text: str
