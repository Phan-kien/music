from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional

# User
@dataclass
class User:
    def __init__(self, id=None, username=None, password=None, email=None, token=None, created_at=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.token = token
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def from_dict(cls, data):
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email'),
            token=data.get('token'),
            created_at=created_at
        )
