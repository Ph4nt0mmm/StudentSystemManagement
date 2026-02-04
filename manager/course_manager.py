from typing import List, Dict, Any, Optional
from ..modules.course import Course
import os


class CourseManager:

    def __init__(self):
        self.courses_file = "File/courses_list.text"
        os.makedirs("File", exist_ok=True)

    def create_course(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        result = {
            'success': False,
            'message': '',
            'course_id': None
        }

        try:
            course = Course(**course_data)

            # Save to file
            with open(self.courses_file, 'a') as f:
                f.write(f"{course.to_dict()}\n")

            result['success'] = True
            result['message'] = 'Course created successfully'
            result['course_id'] = course.course_id

        except Exception as e:
            result['message'] = f'Failed to create course: {str(e)}'

        return result

    def get_all_courses(self) -> List[Course]:
        courses = []

        if not os.path.exists(self.courses_file):
            return courses

        try:
            with open(self.courses_file, 'r') as f:
                for line in f:
                    try:
                        data = eval(line.strip())
                        courses.append(Course(**data))
                    except:
                        continue
        except:
            pass

        return courses

    def get_course_by_id(self, course_id: str) -> Optional[Course]:
        courses = self.get_all_courses()
        for course in courses:
            if course.course_id == course_id:
                return course
        return None

    def enroll_student(self, course_id: str, student_id: str) -> Dict[str, Any]:
        result = {
            'success': False,
            'message': ''
        }

        course = self.get_course_by_id(course_id)
        if not course:
            result['message'] = f'Course {course_id} not found'
            return result

        if student_id in course.enrolled_students:
            result['message'] = f'Student {student_id} already enrolled'
            return result

        if len(course.enrolled_students) >= course.max_students:
            result['message'] = 'Course is full'
            return result

        course.enrolled_students.append(student_id)
        return self._update_course(course)

    def _update_course(self, course: Course) -> Dict[str, Any]:
        result = {
            'success': False,
            'message': ''
        }

        try:
            courses = self.get_all_courses()

            # Find and update the course
            for i, c in enumerate(courses):
                if c.course_id == course.course_id:
                    courses[i] = course
                    break

            # Save all courses
            with open(self.courses_file, 'w') as f:
                for c in courses:
                    f.write(f"{c.to_dict()}\n")

            result['success'] = True
            result['message'] = 'Course updated successfully'

        except Exception as e:
            result['message'] = f'Failed to update course: {str(e)}'

        return result
