from typing import List, Dict, Any
from ..modules.grade import Grade
import os


class GradeManager:

    def __init__(self):
        self.grades_file = "File/grades_list.text"
        os.makedirs("File", exist_ok=True)

    def add_grade(self, grade_data: Dict[str, Any]) -> Dict[str, Any]:

        pass

    def get_student_grades(self, student_id: str) -> List[Grade]:

        pass

    def get_course_grades(self, course_id: str) -> List[Grade]:
        pass