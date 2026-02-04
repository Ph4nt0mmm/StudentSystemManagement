from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:

    username: str
    password: str
    email: str
    firstname: str
    lastname: str
    role: str = "user"
    created_at: str = None
    is_active: bool = True

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_full_name(self) -> str:

        return f"{self.firstname} {self.lastname}"

    def to_dict(self) -> dict:

        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'role': self.role,
            'created_at': self.created_at,
            'is_active': self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':

        return cls(**data)