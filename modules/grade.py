from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime


@dataclass
class Grade:

    grade_id: str
    student_id: str
    course_id: str
    semester: str
    year: int
    lecturer_id: str
    attendance: float = 0.0
    assignments: Dict[str, float] = None
    midterm: float = 0.0
    final: float = 0.0
    project: float = 0.0
    total: float = 0.0
    grade_letter: str = ""
    comments: str = ""
    last_updated: str = None

    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.assignments is None:
            self.assignments = {}

        # Calculate total if not provided
        if self.total == 0.0:
            self.calculate_total()

    def calculate_total(self):

        assignment_total = sum(self.assignments.values()) if self.assignments else 0
        assignment_avg = assignment_total / len(self.assignments) if self.assignments else 0

        # Sample calculation (adjust weights as needed)
        self.total = (
                self.attendance * 0.1 +
                assignment_avg * 0.3 +
                self.midterm * 0.25 +
                self.final * 0.25 +
                self.project * 0.1
        )
        self.determine_grade_letter()

    def determine_grade_letter(self):

        if self.total >= 90:
            self.grade_letter = "A"
        elif self.total >= 80:
            self.grade_letter = "B"
        elif self.total >= 70:
            self.grade_letter = "C"
        elif self.total >= 60:
            self.grade_letter = "D"
        else:
            self.grade_letter = "F"

    def to_dict(self) -> dict:

        return {
            'grade_id': self.grade_id,
            'student_id': self.student_id,
            'course_id': self.course_id,
            'semester': self.semester,
            'year': self.year,
            'lecturer_id': self.lecturer_id,
            'attendance': self.attendance,
            'assignments': self.assignments,
            'midterm': self.midterm,
            'final': self.final,
            'project': self.project,
            'total': self.total,
            'grade_letter': self.grade_letter,
            'comments': self.comments,
            'last_updated': self.last_updated
        }