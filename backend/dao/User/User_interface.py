from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from typing import Optional

class RegisterInput(BaseModel):
    username: constr(min_length=3, max_length=100)
    email: EmailStr
    password: constr(min_length=6)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (can include underscore)')
        return v

    @validator('email')
    def email_length(cls, v):
        if len(v) > 100:
            raise ValueError('Email must be less than 100 characters')
        return v

class LoginInput(BaseModel):
    username: str
    password: str

class User(BaseModel):
    user_id: int
    username: str
    email: str
    registration_date: Optional[datetime] = None

    class Config:
        from_attributes = True