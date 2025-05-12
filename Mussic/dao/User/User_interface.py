from dataclasses import dataclass
from typing import Optional

@dataclass
class RegisterInput:
    username: str
    email: str
    password: str

@dataclass
class LoginInput:
    username: str
    password: str

@dataclass
class UserOutput:
    id: int
    username: str
    email: str
