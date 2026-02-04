
from typing import List, Dict, Any
from ..modules.assignment import Assignment
import os


class AssignmentManager:


    def __init__(self):
        self.assignments_file = "File/assignments_list.text"
        os.makedirs("File", exist_ok=True)

    def create_assignment(self, assignment_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def get_assignments_by_course(self, course_id: str) -> List[Assignment]:

        pass

    def submit_assignment(self, assignment_id: str, student_id: str) -> Dict[str, Any]:

        pass