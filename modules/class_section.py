from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class ClassSection:

    class_id: str
    class_name: str
    academic_year: str
    semester: str
    department: str
    head_teacher: str = ""
    students: List[str] = None
    courses: List[str] = None
    meeting_time: str = ""
    classroom: str = ""
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.students is None:
            self.students = []
        if self.courses is None:
            self.courses = []

    def to_dict(self) -> dict:

        return {
            'class_id': self.class_id,
            'class_name': self.class_name,
            'academic_year': self.academic_year,
            'semester': self.semester,
            'department': self.department,
            'head_teacher': self.head_teacher,
            'students': self.students,
            'courses': self.courses,
            'meeting_time': self.meeting_time,
            'classroom': self.classroom,
            'created_at': self.created_at
        }