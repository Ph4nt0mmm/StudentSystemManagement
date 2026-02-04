from typing import Dict, Any, Optional, Tuple
from ..DAL.user_repository import UserRepository
from ..modules.user import User
from ..modules.student import Student
from ..modules.lecturer import Lecturer
from ..modules.admin import Admin


class AuthManager:

    def __init__(self):
        self.user_repo = User()

    def login(self, username: str, password: str) -> Dict[str, Any]:

        result = {
            'success': False,
            'user_data': None,
            'role': None,
            'error_message': ''
        }

        # Validate input
        if not username or not password:
            result['error_message'] = 'Please enter both username and password'
            return result

        # Authenticate user
        user = self.user_repo.authenticate_user(username, password)

        if not user:
            result['error_message'] = 'Invalid username or password'
            return result

        # Prepare successful response
        result['success'] = True
        result['user_data'] = user
        result['role'] = user.role

        return result

    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:

        result = {
            'success': False,
            'user_data': None,
            'error_message': ''
        }

        # Validate required fields
        required_fields = ['username', 'password', 'email', 'firstname', 'lastname', 'role']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                result['error_message'] = f'Missing required field: {field}'
                return result

        # Check if username already exists
        existing_user = self.user_repo.get_user_by_username(user_data['username'])
        if existing_user:
            result['error_message'] = f'Username {user_data["username"]} already exists'
            return result

        # Create user object based on role
        role = user_data['role']
        try:
            if role == 'admin':
                user = Admin(
                    username=user_data['username'],
                    password=user_data['password'],
                    email=user_data['email'],
                    firstname=user_data['firstname'],
                    lastname=user_data['lastname']
                )
            elif role == 'lecturer':
                user = Lecturer(
                    username=user_data['username'],
                    password=user_data['password'],
                    email=user_data['email'],
                    firstname=user_data['firstname'],
                    lastname=user_data['lastname'],
                    employee_id=user_data.get('employee_id', ''),
                    department=user_data.get('department', ''),
                    specialization=user_data.get('specialization', '')
                )
            elif role == 'student':
                user = Student(
                    username=user_data['username'],
                    password=user_data['password'],
                    email=user_data.get('email', ''),
                    firstname=user_data['firstname'],
                    lastname=user_data['lastname'],
                    std_code=user_data.get('std_code', ''),
                    class_=user_data.get('class_', ''),
                    gender=user_data.get('gender', ''),
                    national_code=user_data.get('national_code', ''),
                    phone=user_data.get('phone', '')
                )
            else:
                result['error_message'] = f'Invalid role: {role}'
                return result

            # Save user
            if self.user_repo.save_user(user):
                result['success'] = True
                result['user_data'] = user
            else:
                result['error_message'] = 'Failed to save user data'

        except Exception as e:
            result['error_message'] = f'Registration failed: {str(e)}'

        return result

    def change_password(self, username: str, old_password: str, new_password: str) -> Dict[str, Any]:

        result = {
            'success': False,
            'error_message': ''
        }

        # Authenticate with old password
        user = self.user_repo.authenticate_user(username, old_password)
        if not user:
            result['error_message'] = 'Current password is incorrect'
            return result

        # Update password
        user.password = new_password
        if self.user_repo.update_user(user):
            result['success'] = True
        else:
            result['error_message'] = 'Failed to update password'

        return result

    def has_permission(self, role: str, permission: str) -> bool:

        permission_map = {
            'admin': ['all', 'manage_users', 'manage_courses', 'manage_classes',
                      'view_reports', 'system_settings', 'manage_lecturers', 'manage_students'],
            'lecturer': ['manage_students', 'manage_grades', 'view_schedule',
                         'upload_materials', 'create_assignments', 'take_attendance'],
            'student': ['view_grades', 'view_schedule', 'submit_assignments',
                        'view_courses', 'view_profile', 'update_profile']
        }

        if role not in permission_map:
            return False

        if permission == 'all' and role == 'admin':
            return True

        return permission in permission_map[role]

    def get_user_permissions(self, role: str) -> list:
        permission_map = {
            'admin': ['all', 'manage_users', 'manage_courses', 'manage_classes',
                      'view_reports', 'system_settings', 'manage_lecturers', 'manage_students'],
            'lecturer': ['manage_students', 'manage_grades', 'view_schedule',
                         'upload_materials', 'create_assignments', 'take_attendance'],
            'student': ['view_grades', 'view_schedule', 'submit_assignments',
                        'view_courses', 'view_profile', 'update_profile']
        }

        return permission_map.get(role, [])