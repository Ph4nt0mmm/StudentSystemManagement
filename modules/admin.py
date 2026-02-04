from dataclasses import dataclass
from .user import User


@dataclass
class Admin(User):

    admin_level: str = "super"  # super, normal
    permissions: list = None

    def __post_init__(self):
        super().__post_init__()
        self.role = "admin"
        if self.permissions is None:
            self.permissions = ["all"]

    def to_dict(self) -> dict:

        base_dict = super().to_dict()
        base_dict.update({
            'admin_level': self.admin_level,
            'permissions': self.permissions
        })
        return base_dict