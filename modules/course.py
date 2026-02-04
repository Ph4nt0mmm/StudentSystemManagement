from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Course:

    course_id: str
    course_code: str
    course_name: str
    credits: int
    department: str
    semester: str  # Fall, Spring, Summer
    year: int
    lecturer_id: str = ""
    schedule: str = ""
    classroom: str = ""
    max_students: int = 50
    enrolled_students: List[str] = None
    prerequisites: List[str] = None
    description: str = ""
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.enrolled_students is None:
            self.enrolled_students = []
        if self.prerequisites is None:
            self.prerequisites = []

    def get_full_code(self) -> str:

        return f"{self.course_code}-{self.semester}{self.year}"

    def to_dict(self) -> dict:

        return {
            'course_id': self.course_id,
            'course_code': self.course_code,
            'course_name': self.course_name,
            'credits': self.credits,
            'department': self.department,
            'semester': self.semester,
            'year': self.year,
            'lecturer_id': self.lecturer_id,
            'schedule': self.schedule,
            'classroom': self.classroom,
            'max_students': self.max_students,
            'enrolled_students': self.enrolled_students,
            'prerequisites': self.prerequisites,
            'description': self.description,
            'created_at': self.created_at
        }