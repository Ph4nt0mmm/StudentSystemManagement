from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Schedule:

    schedule_id: str
    user_id: str
    user_type: str  # student, lecturer
    semester: str
    year: int
    monday: List[str] = None
    tuesday: List[str] = None
    wednesday: List[str] = None
    thursday: List[str] = None
    friday: List[str] = None
    saturday: List[str] = None
    sunday: List[str] = None
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.monday is None:
            self.monday = []
        if self.tuesday is None:
            self.tuesday = []
        if self.wednesday is None:
            self.wednesday = []
        if self.thursday is None:
            self.thursday = []
        if self.friday is None:
            self.friday = []
        if self.saturday is None:
            self.saturday = []
        if self.sunday is None:
            self.sunday = []

    def get_day_schedule(self, day: str) -> List[str]:

        day_map = {
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'sunday': self.sunday
        }
        return day_map.get(day.lower(), [])

    def to_dict(self) -> dict:

        return {
            'schedule_id': self.schedule_id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'semester': self.semester,
            'year': self.year,
            'monday': self.monday,
            'tuesday': self.tuesday,
            'wednesday': self.wednesday,
            'thursday': self.thursday,
            'friday': self.friday,
            'saturday': self.saturday,
            'sunday': self.sunday,
            'created_at': self.created_at
        }