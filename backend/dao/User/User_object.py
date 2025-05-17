from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# User
@dataclass
class User:
    user_id: int
    username: str
    email: str
    password: str
    registration_date: Optional[datetime]