from dataclasses import dataclass
from typing import List, Optional
from .user import User


@dataclass
class Lecturer(User):

    employee_id: str = ""
    department: str = ""
    specialization: str = ""
    office_number: str = ""
    office_hours: str = ""
    assigned_courses: List[str] = None
    assigned_classes: List[str] = None

    def __post_init__(self):
        super().__post_init__()
        self.role = "lecturer"
        if self.assigned_courses is None:
            self.assigned_courses = []
        if self.assigned_classes is None:
            self.assigned_classes = []

    def to_dict(self) -> dict:

        base_dict = super().to_dict()
        base_dict.update({
            'employee_id': self.employee_id,
            'department': self.department,
            'specialization': self.specialization,
            'office_number': self.office_number,
            'office_hours': self.office_hours,
            'assigned_courses': self.assigned_courses,
            'assigned_classes': self.assigned_classes
        })
        return base_dict