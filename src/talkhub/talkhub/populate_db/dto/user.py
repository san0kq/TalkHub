from dataclasses import dataclass
from datetime import date


@dataclass
class UserDTO:
    email: str
    username: str
    date_of_birth: date
    password: str
    first_name: str
    last_name: str
    about: str
