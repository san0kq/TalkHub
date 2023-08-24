from dataclasses import dataclass
from datetime import date
from typing import Optional

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class ProfileEditDTO:
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    about: Optional[str]
    country: Optional[str]
    avatar: InMemoryUploadedFile | bool | None
    date_of_birth: Optional[date]
