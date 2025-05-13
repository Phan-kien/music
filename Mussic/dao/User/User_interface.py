from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RegisterInput(BaseModel):
    username: str
    email: str
    password: str

class LoginInput(BaseModel):
    username: str
    password: str

class User(BaseModel):
    user_id: int
    username: str
    email: str
    registration_date: Optional[datetime] = None