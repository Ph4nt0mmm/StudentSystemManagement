from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Assignment:

    assignment_id: str
    course_id: str
    title: str
    description: str
    assignment_type: str  # homework, project, quiz, exam
    max_points: float
    due_date: str
    created_by: str  # lecturer_id
    submissions: List[str] = None  # list of student_ids who submitted
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.submissions is None:
            self.submissions = []

    def is_past_due(self) -> bool:

        due_datetime = datetime.strptime(self.due_date, "%Y-%m-%d %H:%M:%S")
        return datetime.now() > due_datetime

    def to_dict(self) -> dict:

        return {
            'assignment_id': self.assignment_id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'assignment_type': self.assignment_type,
            'max_points': self.max_points,
            'due_date': self.due_date,
            'created_by': self.created_by,
            'submissions': self.submissions,
            'created_at': self.created_at
        }