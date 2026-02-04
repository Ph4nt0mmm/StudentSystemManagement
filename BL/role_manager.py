
from typing import List, Dict, Any

import Student
from ..DAL.user_repository import UserRepository
from ..modules.user import User

class Lecturer:
    pass

class RoleManager:

    def __init__(self):
        self.user_repo = UserRepository()

    def get_users_by_role(self, role: str) -> List[User]:

        return self.user_repo.get_all_users(role)

    def get_role_statistics(self) -> Dict[str, Any]:

        stats = {
            'admin': 0,
            'lecturer': 0,
            'student': 0,
            'total': 0
        }

        users = self.user_repo.get_all_users()
        for user in users:
            if user.role in stats:
                stats[user.role] += 1
            stats['total'] += 1

        return stats

    def promote_to_admin(self, username: str, admin_level: str = "normal") -> Dict[str, Any]:

        result = {
            'success': False,
            'error_message': ''
        }

        
        if not user:
            result['error_message'] = f'User {username} not found'
            return result

        # Import here to avoid circular import
        from ..modules.admin import Admin

        # Create admin from user
        admin = Admin(
            username=user.username,
            password=user.password,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            admin_level=admin_level
        )

        # Delete old user and save as admin
        if self.user_repo.delete_user(username) and self.user_repo.save_user(admin):
            result['success'] = True
        else:
            result['error_message'] = 'Failed to promote user to admin'

        return result

    def assign_lecturer_to_student(self, student_username: str, lecturer_username: str) -> Dict[str, Any]:

        result = {
            'success': False,
            'error_message': ''
        }

        student = self.user_repo.get_user_by_username(student_username)
        lecturer = self.user_repo.get_user_by_username(lecturer_username)

        if not student:
            result['error_message'] = f'Student {student_username} not found'
            return result

        if not lecturer:
            result['error_message'] = f'Lecturer {lecturer_username} not found'
            return result

        if not isinstance(student, Student):
            result['error_message'] = f'{student_username} is not a student'
            return result

        if not isinstance(lecturer, Lecturer):
            result['error_message'] = f'{lecturer_username} is not a lecturer'
            return result

        # Update student's lecturer_id
        student.lecturer_id = lecturer_username
        if self.user_repo.update_user(student):
            result['success'] = True
        else:
            result['error_message'] = 'Failed to assign lecturer to student'

        return result

    def get_students_by_lecturer(self, lecturer_username: str) -> List[Student]:

        from ..modules.student import Student

        students = []
        all_students = self.get_users_by_role('student')

        for student in all_students:
            if isinstance(student, Student) and student.lecturer_id == lecturer_username:
                students.append(student)

        return students