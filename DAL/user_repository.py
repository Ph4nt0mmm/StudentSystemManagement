
import os
from typing import List, Dict, Any, Optional
from ..modules.user import User
from ..modules.student import Student
from ..modules.lecturer import Lecturer
from ..modules.admin import Admin
from .data import load_data, save_data, save_data_list


class UserRepository:

    def __init__(self):
        self.base_path = "File"
        self.admin_file = os.path.join(self.base_path, "admin_list.text")
        self.teacher_file = os.path.join(self.base_path, "teacher_list.text")
        self.student_file = os.path.join(self.base_path, "student_list.text")

        # Ensure File directory exists
        os.makedirs(self.base_path, exist_ok=True)

    def _convert_to_user_object(self, data: Dict[str, Any]) -> Optional[User]:
        role = data.get('role', 'user')

        if role == 'admin':
            return Admin.from_dict(data)
        elif role == 'lecturer':
            return Lecturer.from_dict(data)
        elif role == 'student':
            return Student.from_dict(data)
        else:
            return User.from_dict(data)

    def get_all_users(self, role: str = None) -> List[User]:
        users = []

        # Load admins
        if role is None or role == 'admin':
            result = load_data(self.admin_file)
            if result['success']:
                for line in result['returndata']:
                    try:
                        data = eval(line.strip())
                        users.append(self._convert_to_user_object(data))
                    except:
                        continue

        # Load lecturers
        if role is None or role == 'lecturer':
            result = load_data(self.teacher_file)
            if result['success']:
                for line in result['returndata']:
                    try:
                        data = eval(line.strip())
                        data['role'] = 'lecturer'
                        users.append(self._convert_to_user_object(data))
                    except:
                        continue

        # Load students
        if role is None or role == 'student':
            result = load_data(self.student_file)
            if result['success']:
                for line in result['returndata']:
                    try:
                        data = eval(line.strip())
                        data['role'] = 'student'
                        users.append(self._convert_to_user_object(data))
                    except:
                        continue

        return users

    def get_user_by_username(self, username: str) -> Optional[User]:
        users = self.get_all_users()
        for user in users:
            if user.username == username:
                return user
        return None

    def save_user(self, user: User) -> bool:
        user_dict = user.to_dict()

        if isinstance(user, Admin):
            file_path = self.admin_file
        elif isinstance(user, Lecturer):
            file_path = self.teacher_file
        elif isinstance(user, Student):
            file_path = self.student_file
        else:
            file_path = self.admin_file  # Default

        result = save_data(data=f"{user_dict}\n", file_path=file_path)
        return result['success']

    def update_user(self, user: User) -> bool:

        # First, remove the old user record
        self.delete_user(user.username)

        # Then save the updated user
        return self.save_user(user)

    def delete_user(self, username: str) -> bool:

        user = self.get_user_by_username(username)
        if not user:
            return False

        if isinstance(user, Admin):
            file_path = self.admin_file
        elif isinstance(user, Lecturer):
            file_path = self.teacher_file
        elif isinstance(user, Student):
            file_path = self.student_file
        else:
            return False

        # Load all users from file
        result = load_data(file_path)
        if not result['success']:
            return False

        # Filter out the user to delete
        updated_lines = []
        for line in result['returndata']:
            try:
                data = eval(line.strip())
                if data.get('username') != username:
                    updated_lines.append(line)
            except:
                updated_lines.append(line)

        # Save updated list
        save_result = save_data_list(data=updated_lines, file_path=file_path, mode='w')
        return save_result['success']

    def authenticate_user(self, username: str, password: str) -> Optional[User]:

        user = self.get_user_by_username(username)
        if user and user.password == password and user.is_active:
            return user
        return None