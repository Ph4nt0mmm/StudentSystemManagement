from typing import List, Dict, Any
from ..modules.schedules import Schedule
import os


class ScheduleManager:


    def __init__(self):
        self.schedules_file = "File/schedules.text"
        os.makedirs("File", exist_ok=True)

    def create_schedule(self, schedule_data: Dict[str, Any]) -> Dict[str, Any]:

        pass

    def get_user_schedule(self, user_id: str) -> Schedule:

        pass