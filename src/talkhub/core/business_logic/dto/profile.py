from dataclasses import dataclass
from datetime import date
from typing import Optional

from django.core.files.uploadedfile import InMemoryUploadedFile


@dataclass
class ProfileEditDTO:
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    about: Optional[str]
    country: Optional[str]
    avatar: Optional[InMemoryUploadedFile]
    date_of_birth: date
