from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime


@dataclass
class AttendanceRecord:
    attendance_id: str
    course_id: str
    session_date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    lecturer_id: str
    students: Dict[str, str]  # student_id: status
    notes: str = ""
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.students is None:
            self.students = {}

    def mark_attendance(self, student_id: str, status: str = "present"):

        valid_statuses = ["present", "absent", "late", "excused"]
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {valid_statuses}")
        self.students[student_id] = status

    def get_attendance_stats(self) -> Dict[str, int]:
        stats = {
            "total": len(self.students),
            "present": 0,
            "absent": 0,
            "late": 0,
            "excused": 0
        }

        for status in self.students.values():
            if status in stats:
                stats[status] += 1

        return stats

    def to_dict(self) -> dict:
        return {
            'attendance_id': self.attendance_id,
            'course_id': self.course_id,
            'session_date': self.session_date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'lecturer_id': self.lecturer_id,
            'students': self.students,
            'notes': self.notes,
            'created_at': self.created_at
        }


@dataclass
class AttendanceSummary:
    student_id: str
    course_id: str
    semester: str
    year: int
    total_sessions: int = 0
    present_count: int = 0
    absent_count: int = 0
    late_count: int = 0
    excused_count: int = 0
    attendance_rate: float = 0.0

    def calculate_rate(self):
        if self.total_sessions > 0:
            attended = self.present_count + self.late_count + self.excused_count
            self.attendance_rate = (attended / self.total_sessions) * 100

    def to_dict(self) -> dict:

        return {
            'student_id': self.student_id,
            'course_id': self.course_id,
            'semester': self.semester,
            'year': self.year,
            'total_sessions': self.total_sessions,
            'present_count': self.present_count,
            'absent_count': self.absent_count,
            'late_count': self.late_count,
            'excused_count': self.excused_count,
            'attendance_rate': round(self.attendance_rate, 2)
        }