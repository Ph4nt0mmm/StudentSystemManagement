from dataclasses import dataclass
from typing import Optional
from .user import User


@dataclass
class Student(User):

    std_code: str = ""
    class_: str = ""
    gender: str = ""
    national_code: str = ""
    phone: str = ""
    address: str = ""
    date_of_birth: str = ""
    enrollment_date: str = ""
    lecturer_id: str = ""  # ID of assigned lecturer

    def __post_init__(self):
        super().__post_init__()
        self.role = "student"

    def to_dict(self) -> dict:

        base_dict = super().to_dict()
        base_dict.update({
            'std_code': self.std_code,
            'class_': self.class_,
            'gender': self.gender,
            'national_code': self.national_code,
            'phone': self.phone,
            'address': self.address,
            'date_of_birth': self.date_of_birth,
            'enrollment_date': self.enrollment_date,
            'lecturer_id': self.lecturer_id
        })
        return base_dict