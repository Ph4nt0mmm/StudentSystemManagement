import sys
import os
import json
from datetime import datetime, timedelta
class StudentManagementSystem:

    def __init__(self):
        self.current_user = None
        self.current_role = None
        self.data_files = {
            'admin': 'File/admin_list.text',
            'teacher': 'File/teacher_list.text',
            'student': 'File/student_list.text',
            'courses': 'File/courses_list.text',
            'classes': 'File/classes_list.text',
            'grades': 'File/grades_list.text',
            'assignments': 'File/assignments_list.text',
            'schedules': 'File/schedules_list.text',
            'attendance': 'File/attendance_list.text'
        }

        # Tạo thư mục File nếu chưa tồn tại
        os.makedirs("File", exist_ok=True)

    def clear_screen(self):
        """Xóa màn hình console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def read_file(self, filepath):
        """Đọc và phân tích dữ liệu từ file text"""
        data = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                # Chuyển đổi string dictionary thành dictionary
                                item = eval(line)
                                data.append(item)
                            except:
                                try:
                                    # Thử parse JSON
                                    item = json.loads(line.replace("'", '"'))
                                    data.append(item)
                                except:
                                    continue
            except:
                pass
        return data

    def save_to_file(self, filepath, data_list, mode='a'):
        """Lưu danh sách dictionary vào file"""
        try:
            with open(filepath, mode, encoding='utf-8') as f:
                for item in data_list:
                    f.write(f"{item}\n")
            return True
        except:
            return False

    def create_default_files(self):
        """Tạo file mặc định nếu chưa tồn tại"""
        print("\nĐang kiểm tra file dữ liệu...")

        # Tài khoản admin mặc định
        default_admin = {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@school.edu',
            'firstname': 'Quản trị',
            'lastname': 'Hệ thống',
            'role': 'admin',
            'admin_level': 'super',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': True
        }

        # Tạo các file nếu chưa tồn tại
        files_created = 0
        for file_type, filepath in self.data_files.items():
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    if file_type == 'admin':
                        f.write(f"{default_admin}\n")
                        files_created += 1
                    else:
                        f.write("")
                print(f"✓ Đã tạo: {filepath}")

        if files_created > 0:
            print(f"\nĐã tạo {files_created} file dữ liệu mới.")
            print("Tài khoản admin mặc định:")
            print("  Tên đăng nhập: admin")
            print("  Mật khẩu: admin123")
        else:
            print("✓ Tất cả file dữ liệu đã tồn tại.")

    def login(self):
        """Màn hình đăng nhập"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     HỆ THỐNG QUẢN LÝ SINH VIÊN")
        print("="*50)
        print("\nĐĂNG NHẬP HỆ THỐNG")
        print("-"*50)

        # Đọc tất cả người dùng
        all_users = []
        for role, filepath in [('admin', self.data_files['admin']),
                              ('teacher', self.data_files['teacher']),
                              ('student', self.data_files['student'])]:
            users = self.read_file(filepath)
            for user in users:
                user['role'] = role if role != 'teacher' else 'lecturer'
                all_users.append(user)

        while True:
            username = input("\nTên đăng nhập: ").strip()
            password = input("Mật khẩu: ").strip()

            # Tìm người dùng
            for user in all_users:
                if user.get('username') == username and user.get('password') == password:
                    self.current_user = user
                    self.current_role = user.get('role', 'student')

                    if self.current_role == 'teacher':
                        self.current_role = 'lecturer'

                    print(f"\n✓ Đăng nhập thành công!")
                    print(f"  Chào mừng: {user.get('firstname', '')} {user.get('lastname', '')}")
                    print(f"  Vai trò: {self.current_role.upper()}")
                    input("\nNhấn Enter để tiếp tục...")
                    return True

            print("\n✗ Tên đăng nhập hoặc mật khẩu không đúng!")
            retry = input("\nThử lại? (y/n): ").strip().lower()
            if retry != 'y':
                return False

    def admin_menu(self):
        """Menu quản trị viên"""
        while True:
            self.clear_screen()
            print("\n" + "="*50)
            print(f"     TRANG QUẢN TRỊ - {self.current_user.get('firstname', '')}")
            print("="*50)

            # Thống kê hệ thống
            admin_count = len(self.read_file(self.data_files['admin']))
            lecturer_count = len(self.read_file(self.data_files['teacher']))
            student_count = len(self.read_file(self.data_files['student']))
            course_count = len(self.read_file(self.data_files['courses']))
            class_count = len(self.read_file(self.data_files['classes']))

            print(f"\n📊 THỐNG KÊ HỆ THỐNG:")
            print(f"   Quản trị viên: {admin_count}")
            print(f"   Giảng viên: {lecturer_count}")
            print(f"   Sinh viên: {student_count}")
            print(f"   Môn học: {course_count}")
            print(f"   Lớp học: {class_count}")

            print("\n" + "-"*50)
            print("\n1. Quản lý người dùng")
            print("2. Quản lý sinh viên")
            print("3. Quản lý giảng viên")
            print("4. Quản lý môn học")
            print("5. Xem báo cáo")
            print("6. Sao lưu dữ liệu")
            print("7. Đăng xuất")
            print("8. Thoát chương trình")

            choice = input("\nChọn chức năng (1-8): ").strip()

            if choice == '1':
                self.manage_users()
            elif choice == '2':
                self.manage_students()
            elif choice == '3':
                self.manage_lecturers()
            elif choice == '4':
                self.manage_courses()
            elif choice == '5':
                self.view_reports()
            elif choice == '6':
                self.backup_data()
            elif choice == '7':
                self.current_user = None
                self.current_role = None
                print("\nĐã đăng xuất!")
                input("Nhấn Enter để tiếp tục...")
                break
            elif choice == '8':
                self.exit_program()
            else:
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")

    def lecturer_menu(self):
        """Menu giảng viên"""
        while True:
            self.clear_screen()
            print("\n" + "="*50)
            print(f"     TRANG GIẢNG VIÊN - {self.current_user.get('firstname', '')}")
            print("="*50)

            lecturer_id = self.current_user.get('username', '')

            # Lấy thông tin giảng viên
            courses = self.read_file(self.data_files['courses'])
            my_courses = [c for c in courses if c.get('lecturer_id') == lecturer_id]
            my_students = []
            for course in my_courses:
                my_students.extend(course.get('enrolled_students', []))
            my_students = list(set(my_students))

            print(f"\n📚 THÔNG TIN CÁ NHÂN:")
            print(f"   Tên: {self.current_user.get('firstname', '')} {self.current_user.get('lastname', '')}")
            print(f"   Khoa: {self.current_user.get('department', 'Chưa cập nhật')}")
            print(f"   Chuyên ngành: {self.current_user.get('specialization', 'Chưa cập nhật')}")
            print(f"\n📊 THỐNG KÊ:")
            print(f"   Số môn giảng dạy: {len(my_courses)}")
            print(f"   Tổng sinh viên: {len(my_students)}")

            print("\n" + "-"*50)
            print("\n1. Danh sách môn học")
            print("2. Danh sách sinh viên")
            print("3. Quản lý điểm")
            print("4. Tạo bài tập")
            print("5. Điểm danh")
            print("6. Xem lịch dạy")
            print("7. Đăng xuất")
            print("8. Thoát chương trình")

            choice = input("\nChọn chức năng (1-8): ").strip()

            if choice == '1':
                self.view_lecturer_courses()
            elif choice == '2':
                self.view_lecturer_students()
            elif choice == '3':
                self.manage_grades()
            elif choice == '4':
                self.create_assignment()
            elif choice == '5':
                self.take_attendance()
            elif choice == '6':
                self.view_lecturer_schedule()
            elif choice == '7':
                self.current_user = None
                self.current_role = None
                print("\nĐã đăng xuất!")
                input("Nhấn Enter để tiếp tục...")
                break
            elif choice == '8':
                self.exit_program()
            else:
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")

    def student_menu(self):
        """Menu sinh viên - Đã cập nhật"""
        while True:
            self.clear_screen()
            print("\n" + "=" * 50)
            print(f"     TRANG SINH VIÊN - {self.current_user.get('firstname', '')}")
            print("=" * 50)

            student_id = self.current_user.get('username', '')

            # Lấy thông tin sinh viên
            courses = self.read_file(self.data_files['courses'])
            my_courses = [c for c in courses if student_id in c.get('enrolled_students', [])]

            # Lấy điểm
            grades = self.read_file(self.data_files['grades'])
            my_grades = [g for g in grades if g.get('student_id') == student_id]

            print(f"\n📋 THÔNG TIN CÁ NHÂN:")
            print(f"   Mã SV: {self.current_user.get('std_code', 'N/A')}")
            print(f"   Lớp: {self.current_user.get('class_', 'N/A')}")
            print(f"   Email: {self.current_user.get('email', 'N/A')}")

            print(f"\n📊 THỐNG KÊ:")
            print(f"   Số môn đang học: {len(my_courses)}")
            print(f"   Số môn đã có điểm: {len(my_grades)}")

            if my_grades:
                # Tính GPA đơn giản
                total_credits = 0
                total_grade_points = 0
                for grade in my_grades:
                    course_id = grade.get('course_id')
                    course = next((c for c in courses if c.get('course_id') == course_id), None)
                    if course:
                        credits = course.get('credits', 3)
                        grade_letter = grade.get('grade_letter', 'F')
                        grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
                        grade_points = grade_map.get(grade_letter, 0.0)
                        total_grade_points += grade_points * credits
                        total_credits += credits

                if total_credits > 0:
                    gpa = total_grade_points / total_credits
                    print(f"   GPA hiện tại: {gpa:.2f}/4.0")

            print("\n" + "-" * 50)
            print("\n1. Xem môn học")
            print("2. Xem điểm")
            print("3. Đăng ký môn học")
            print("4. Xem lịch học")
            print("5. Quản lý bài tập")  # Đã sửa - gộp thành 1 chức năng
            print("6. Thông tin cá nhân")
            print("7. Đăng xuất")
            print("8. Thoát chương trình")

            choice = input("\nChọn chức năng (1-8): ").strip()

            if choice == '1':
                self.view_student_courses_detail()
            elif choice == '2':
                self.view_student_grades()
            elif choice == '3':
                self.register_courses()
            elif choice == '4':
                self.view_student_schedule()
            elif choice == '5':  # Chức năng mới - Quản lý bài tập
                self.view_student_assignments()
            elif choice == '6':
                self.view_student_profile()
            elif choice == '7':
                self.current_user = None
                self.current_role = None
                print("\nĐã đăng xuất!")
                input("Nhấn Enter để tiếp tục...")
                break
            elif choice == '8':
                self.exit_program()
            else:
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")

    # ========== QUẢN LÝ NGƯỜI DÙNG ==========

    def manage_users(self):
        """Quản lý người dùng (Admin)"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     QUẢN LÝ NGƯỜI DÙNG")
        print("="*50)

        print("\n1. Thêm người dùng")
        print("2. Xem danh sách người dùng")
        print("3. Tìm kiếm người dùng")
        print("4. Khóa/Mở tài khoản")
        print("5. Quay lại")

        choice = input("\nChọn chức năng (1-5): ").strip()

        if choice == '1':
            self.add_user()
        elif choice == '2':
            self.view_users()
        elif choice == '3':
            self.search_user()
        elif choice == '4':
            self.toggle_user_status()
        elif choice == '5':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def add_user(self):
        """Thêm người dùng mới"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THÊM NGƯỜI DÙNG MỚI")
        print("="*50)

        print("\nLoại người dùng:")
        print("1. Quản trị viên")
        print("2. Giảng viên")
        print("3. Sinh viên")

        role_choice = input("\nChọn loại người dùng (1-3): ").strip()
        role_map = {'1': 'admin', '2': 'lecturer', '3': 'student'}
        role = role_map.get(role_choice)

        if not role:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nNhập thông tin cho {role}:")
        username = input("Tên đăng nhập: ").strip()

        # Kiểm tra username đã tồn tại chưa
        if self.check_user_exists(username):
            print(f"\n✗ Tên đăng nhập '{username}' đã tồn tại!")
            input("\nNhấn Enter để tiếp tục...")
            return

        password = input("Mật khẩu: ").strip()
        email = input("Email: ").strip()
        firstname = input("Họ và tên đệm: ").strip()
        lastname = input("Tên: ").strip()

        # Tạo user dictionary
        user_data = {
            'username': username,
            'password': password,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'role': role,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': True
        }

        # Thêm thông tin bổ sung theo vai trò
        if role == 'admin':
            user_data['admin_level'] = 'normal'
            user_data['permissions'] = ['manage_users', 'manage_courses']
            filepath = self.data_files['admin']
        elif role == 'lecturer':
            employee_id = input("Mã giảng viên: ").strip()
            department = input("Khoa: ").strip()
            specialization = input("Chuyên ngành: ").strip()
            user_data.update({
                'employee_id': employee_id,
                'department': department,
                'specialization': specialization,
                'assigned_courses': [],
                'assigned_classes': []
            })
            filepath = self.data_files['teacher']
        elif role == 'student':
            std_code = input("Mã sinh viên: ").strip()
            class_ = input("Lớp: ").strip()
            gender = input("Giới tính (Nam/Nữ): ").strip()
            national_code = input("Mã số CMND/CCCD: ").strip()
            phone = input("Số điện thoại: ").strip()
            user_data.update({
                'std_code': std_code,
                'class_': class_,
                'gender': gender,
                'national_code': national_code,
                'phone': phone,
                'lecturer_id': ''
            })
            filepath = self.data_files['student']

        # Lưu vào file
        users = self.read_file(filepath)
        users.append(user_data)

        if self.save_to_file(filepath, users, 'w'):
            print(f"\n✓ Đã thêm {role} '{username}' thành công!")
        else:
            print(f"\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def check_user_exists(self, username):
        """Kiểm tra username đã tồn tại chưa"""
        for filepath in [self.data_files['admin'],
                        self.data_files['teacher'],
                        self.data_files['student']]:
            users = self.read_file(filepath)
            for user in users:
                if user.get('username') == username:
                    return True
        return False

    def view_users(self):
        """Xem danh sách người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     DANH SÁCH NGƯỜI DÙNG")
        print("="*50)

        # Đọc tất cả người dùng từ các file
        all_users = []

        # Đọc admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            admin['role'] = 'admin'
            all_users.append(admin)

        # Đọc giảng viên
        lecturers = self.read_file(self.data_files['teacher'])
        for lecturer in lecturers:
            lecturer['role'] = 'lecturer'
            all_users.append(lecturer)

        # Đọc sinh viên
        students = self.read_file(self.data_files['student'])
        for student in students:
            student['role'] = 'student'
            all_users.append(student)

        if not all_users:
            print("\nChưa có người dùng nào trong hệ thống!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Sắp xếp theo vai trò và username
        all_users.sort(key=lambda x: (x.get('role', ''), x.get('username', '')))

        print(f"\nTổng số người dùng: {len(all_users)}")
        print("\n" + "-"*100)
        print(f"{'STT':<5} {'Username':<15} {'Vai trò':<12} {'Họ và tên':<25} {'Email':<25} {'Trạng thái':<10}")
        print("-"*100)

        active_count = 0
        inactive_count = 0

        for i, user in enumerate(all_users, 1):
            username = user.get('username', 'N/A')
            role = user.get('role', 'N/A')
            fullname = f"{user.get('firstname', '')} {user.get('lastname', '')}"
            email = user.get('email', 'N/A')
            is_active = user.get('is_active', True)

            # Chuyển đổi tên vai trò
            role_names = {
                'admin': 'Quản trị',
                'lecturer': 'Giảng viên',
                'student': 'Sinh viên'
            }
            role_display = role_names.get(role, role)

            # Trạng thái
            status = "Hoạt động" if is_active else "Đã khóa"

            if is_active:
                active_count += 1
            else:
                inactive_count += 1

            print(f"{i:<5} {username:<15} {role_display:<12} {fullname:<25} {email:<25} {status:<10}")

        print("-"*100)
        print(f"\n📊 THỐNG KÊ:")
        print(f"  Tổng số: {len(all_users)} người dùng")
        print(f"  Đang hoạt động: {active_count}")
        print(f"  Đã khóa: {inactive_count}")

        # Thống kê theo vai trò
        admin_count = len([u for u in all_users if u.get('role') == 'admin'])
        lecturer_count = len([u for u in all_users if u.get('role') == 'lecturer'])
        student_count = len([u for u in all_users if u.get('role') == 'student'])

        print(f"\n📈 PHÂN BỔ VAI TRÒ:")
        print(f"  Quản trị viên: {admin_count}")
        print(f"  Giảng viên: {lecturer_count}")
        print(f"  Sinh viên: {student_count}")

        # Tùy chọn xem chi tiết
        print("\n1. Xem chi tiết người dùng")
        print("2. Quay lại")

        sub_choice = input("\nChọn chức năng (1-2): ").strip()

        if sub_choice == '1':
            try:
                stt = int(input("\nNhập STT người dùng: ").strip()) - 1
                if 0 <= stt < len(all_users):
                    self.view_user_detail(all_users[stt])
                else:
                    print("\nSTT không hợp lệ!")
            except ValueError:
                print("\nVui lòng nhập số!")
        elif sub_choice == '2':
            return

        input("\nNhấn Enter để tiếp tục...")

    def view_user_detail(self, user):
        """Xem chi tiết thông tin người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THÔNG TIN CHI TIẾT NGƯỜI DÙNG")
        print("="*50)

        username = user.get('username', 'N/A')
        role = user.get('role', 'N/A')
        fullname = f"{user.get('firstname', '')} {user.get('lastname', '')}"
        email = user.get('email', 'N/A')
        is_active = user.get('is_active', True)
        created_at = user.get('created_at', 'N/A')

        # Chuyển đổi tên vai trò
        role_names = {
            'admin': 'Quản trị viên',
            'lecturer': 'Giảng viên',
            'student': 'Sinh viên'
        }
        role_display = role_names.get(role, role)

        status = "Đang hoạt động" if is_active else "Đã bị khóa"

        print(f"\n👤 THÔNG TIN CƠ BẢN:")
        print(f"  Tên đăng nhập: {username}")
        print(f"  Họ và tên: {fullname}")
        print(f"  Vai trò: {role_display}")
        print(f"  Email: {email}")
        print(f"  Trạng thái: {status}")
        print(f"  Ngày tạo: {created_at}")

        # Hiển thị thông tin bổ sung theo vai trò
        if role == 'admin':
            print(f"\n👨‍💼 THÔNG TIN QUẢN TRỊ:")
            admin_level = user.get('admin_level', 'normal')
            permissions = user.get('permissions', [])

            admin_level_names = {
                'super': 'Siêu quản trị',
                'normal': 'Quản trị thường'
            }
            print(f"  Cấp bậc: {admin_level_names.get(admin_level, admin_level)}")
            print(f"  Quyền hạn: {', '.join(permissions) if permissions else 'Mặc định'}")

        elif role == 'lecturer':
            print(f"\n👨‍🏫 THÔNG TIN GIẢNG VIÊN:")
            employee_id = user.get('employee_id', 'N/A')
            department = user.get('department', 'N/A')
            specialization = user.get('specialization', 'N/A')
            phone = user.get('phone', 'Chưa cập nhật')

            # Lấy số môn đang dạy
            all_courses = self.read_file(self.data_files['courses'])
            teaching_courses = [c for c in all_courses if c.get('lecturer_id') == username]

            print(f"  Mã giảng viên: {employee_id}")
            print(f"  Khoa: {department}")
            print(f"  Chuyên ngành: {specialization}")
            print(f"  Số điện thoại: {phone}")
            print(f"  Số môn đang dạy: {len(teaching_courses)}")

            if teaching_courses:
                print(f"  Các môn đang dạy:")
                for i, course in enumerate(teaching_courses[:5], 1):
                    print(f"    {i}. {course.get('course_name')}")
                if len(teaching_courses) > 5:
                    print(f"    ... và {len(teaching_courses) - 5} môn khác")

        elif role == 'student':
            print(f"\n👨‍🎓 THÔNG TIN SINH VIÊN:")
            std_code = user.get('std_code', 'N/A')
            class_ = user.get('class_', 'N/A')
            gender = user.get('gender', 'N/A')
            national_code = user.get('national_code', 'Chưa cập nhật')
            phone = user.get('phone', 'Chưa cập nhật')

            # Lấy thông tin học tập
            all_courses = self.read_file(self.data_files['courses'])
            enrolled_courses = [c for c in all_courses if username in c.get('enrolled_students', [])]

            # Lấy điểm số
            all_grades = self.read_file(self.data_files['grades'])
            student_grades = [g for g in all_grades if g.get('student_id') == username]

            print(f"  Mã sinh viên: {std_code}")
            print(f"  Lớp: {class_}")
            print(f"  Giới tính: {gender}")
            print(f"  CMND/CCCD: {national_code}")
            print(f"  Số điện thoại: {phone}")
            print(f"  Số môn đang học: {len(enrolled_courses)}")
            print(f"  Số môn đã có điểm: {len(student_grades)}")

            if student_grades:
                # Tính GPA
                total_grade_points = 0
                total_credits = 0

                for grade in student_grades:
                    course_id = grade.get('course_id')
                    course = next((c for c in all_courses if c.get('course_id') == course_id), None)
                    if course:
                        credits = course.get('credits', 3)
                        grade_letter = grade.get('grade_letter', 'F')

                        # Chuyển đổi điểm chữ sang điểm số
                        grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
                        grade_points = grade_map.get(grade_letter, 0.0)

                        total_grade_points += grade_points * credits
                        total_credits += credits

                if total_credits > 0:
                    gpa = total_grade_points / total_credits
                    print(f"  GPA hiện tại: {gpa:.2f}/4.0")

        # Hiển thị tùy chọn
        print("\n" + "-"*50)
        print("1. Chỉnh sửa thông tin")
        print("2. Đổi mật khẩu")
        print("3. Khóa/Mở tài khoản")
        print("4. Quay lại")

        choice = input("\nChọn chức năng (1-4): ").strip()

        if choice == '1':
            self.edit_user_info(user)
        elif choice == '2':
            self.change_user_password(user)
        elif choice == '3':
            self.toggle_single_user_status(user)
        elif choice == '4':
            return
        else:
            print("\nLựa chọn không hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    def edit_user_info(self, user):
        """Chỉnh sửa thông tin người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHỈNH SỬA THÔNG TIN NGƯỜI DÙNG")
        print("="*50)

        username = user.get('username')
        role = user.get('role')

        # Xác định file dữ liệu
        if role == 'admin':
            filepath = self.data_files['admin']
        elif role == 'lecturer':
            filepath = self.data_files['teacher']
        else:  # student
            filepath = self.data_files['student']

        # Đọc dữ liệu
        users = self.read_file(filepath)

        # Tìm người dùng
        user_found = None
        for u in users:
            if u.get('username') == username:
                user_found = u
                break

        if not user_found:
            print("\nKhông tìm thấy người dùng!")
            return

        print(f"\nChỉnh sửa thông tin cho: {user_found.get('firstname')} {user_found.get('lastname')}")
        print(f"Vai trò: {role}")
        print("\nThông tin hiện tại:")

        if role == 'admin':
            print(f"1. Họ và tên đệm: {user_found.get('firstname', '')}")
            print(f"2. Tên: {user_found.get('lastname', '')}")
            print(f"3. Email: {user_found.get('email', '')}")
            print(f"4. Cấp bậc: {user_found.get('admin_level', 'normal')}")

            field_choice = input("\nChọn trường cần sửa (1-4, 0 để hủy): ").strip()

            if field_choice == '0':
                return
            elif field_choice == '1':
                new_value = input("Nhập họ và tên đệm mới: ").strip()
                if new_value:
                    user_found['firstname'] = new_value
            elif field_choice == '2':
                new_value = input("Nhập tên mới: ").strip()
                if new_value:
                    user_found['lastname'] = new_value
            elif field_choice == '3':
                new_value = input("Nhập email mới: ").strip()
                if new_value:
                    user_found['email'] = new_value
            elif field_choice == '4':
                new_value = input("Nhập cấp bậc mới (super/normal): ").strip()
                if new_value in ['super', 'normal']:
                    user_found['admin_level'] = new_value
                else:
                    print("\nCấp bậc không hợp lệ!")
                    return
            else:
                print("\nLựa chọn không hợp lệ!")
                return

        elif role == 'lecturer':
            print(f"1. Họ và tên đệm: {user_found.get('firstname', '')}")
            print(f"2. Tên: {user_found.get('lastname', '')}")
            print(f"3. Email: {user_found.get('email', '')}")
            print(f"4. Mã giảng viên: {user_found.get('employee_id', '')}")
            print(f"5. Khoa: {user_found.get('department', '')}")
            print(f"6. Chuyên ngành: {user_found.get('specialization', '')}")
            print(f"7. Số điện thoại: {user_found.get('phone', '')}")

            field_choice = input("\nChọn trường cần sửa (1-7, 0 để hủy): ").strip()

            if field_choice == '0':
                return
            elif field_choice == '1':
                new_value = input("Nhập họ và tên đệm mới: ").strip()
                if new_value:
                    user_found['firstname'] = new_value
            elif field_choice == '2':
                new_value = input("Nhập tên mới: ").strip()
                if new_value:
                    user_found['lastname'] = new_value
            elif field_choice == '3':
                new_value = input("Nhập email mới: ").strip()
                if new_value:
                    user_found['email'] = new_value
            elif field_choice == '4':
                new_value = input("Nhập mã giảng viên mới: ").strip()
                if new_value:
                    user_found['employee_id'] = new_value
            elif field_choice == '5':
                new_value = input("Nhập khoa mới: ").strip()
                if new_value:
                    user_found['department'] = new_value
            elif field_choice == '6':
                new_value = input("Nhập chuyên ngành mới: ").strip()
                if new_value:
                    user_found['specialization'] = new_value
            elif field_choice == '7':
                new_value = input("Nhập số điện thoại mới: ").strip()
                if new_value:
                    user_found['phone'] = new_value
            else:
                print("\nLựa chọn không hợp lệ!")
                return

        elif role == 'student':
            print(f"1. Họ và tên đệm: {user_found.get('firstname', '')}")
            print(f"2. Tên: {user_found.get('lastname', '')}")
            print(f"3. Email: {user_found.get('email', '')}")
            print(f"4. Mã sinh viên: {user_found.get('std_code', '')}")
            print(f"5. Lớp: {user_found.get('class_', '')}")
            print(f"6. Giới tính: {user_found.get('gender', '')}")
            print(f"7. Số điện thoại: {user_found.get('phone', '')}")
            print(f"8. CMND/CCCD: {user_found.get('national_code', '')}")

            field_choice = input("\nChọn trường cần sửa (1-8, 0 để hủy): ").strip()

            if field_choice == '0':
                return
            elif field_choice == '1':
                new_value = input("Nhập họ và tên đệm mới: ").strip()
                if new_value:
                    user_found['firstname'] = new_value
            elif field_choice == '2':
                new_value = input("Nhập tên mới: ").strip()
                if new_value:
                    user_found['lastname'] = new_value
            elif field_choice == '3':
                new_value = input("Nhập email mới: ").strip()
                if new_value:
                    user_found['email'] = new_value
            elif field_choice == '4':
                new_value = input("Nhập mã sinh viên mới: ").strip()
                if new_value:
                    user_found['std_code'] = new_value
            elif field_choice == '5':
                new_value = input("Nhập lớp mới: ").strip()
                if new_value:
                    user_found['class_'] = new_value
            elif field_choice == '6':
                new_value = input("Nhập giới tính mới (Nam/Nữ): ").strip()
                if new_value:
                    user_found['gender'] = new_value
            elif field_choice == '7':
                new_value = input("Nhập số điện thoại mới: ").strip()
                if new_value:
                    user_found['phone'] = new_value
            elif field_choice == '8':
                new_value = input("Nhập CMND/CCCD mới: ").strip()
                if new_value:
                    user_found['national_code'] = new_value
            else:
                print("\nLựa chọn không hợp lệ!")
                return

        # Lưu dữ liệu
        if self.save_to_file(filepath, users, 'w'):
            print("\n✓ Đã cập nhật thông tin thành công!")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

    def change_user_password(self, user):
        """Đổi mật khẩu cho người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     ĐỔI MẬT KHẨU NGƯỜI DÙNG")
        print("="*50)

        username = user.get('username')
        role = user.get('role')

        print(f"\nĐổi mật khẩu cho: {user.get('firstname')} {user.get('lastname')}")
        print(f"Username: {username}")

        new_password = input("\nNhập mật khẩu mới: ").strip()
        confirm_password = input("Nhập lại mật khẩu mới: ").strip()

        if new_password != confirm_password:
            print("\n✗ Mật khẩu mới không khớp!")
            input("\nNhấn Enter để tiếp tục...")
            return

        if len(new_password) < 6:
            print("\n✗ Mật khẩu phải có ít nhất 6 ký tự!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Xác định file dữ liệu
        if role == 'admin':
            filepath = self.data_files['admin']
        elif role == 'lecturer':
            filepath = self.data_files['teacher']
        else:  # student
            filepath = self.data_files['student']

        # Đọc và cập nhật dữ liệu
        users = self.read_file(filepath)
        updated = False

        for u in users:
            if u.get('username') == username:
                u['password'] = new_password
                updated = True
                break

        if updated:
            # Lưu dữ liệu
            if self.save_to_file(filepath, users, 'w'):
                print("\n✓ Đã đổi mật khẩu thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")
        else:
            print("\n✗ Không tìm thấy người dùng!")

        input("\nNhấn Enter để tiếp tục...")

    def toggle_single_user_status(self, user):
        """Khóa/Mở tài khoản người dùng cụ thể"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KHÓA/MỞ TÀI KHOẢN NGƯỜI DÙNG")
        print("="*50)

        username = user.get('username')
        current_status = user.get('is_active', True)
        role = user.get('role')

        print(f"\nThông tin người dùng:")
        print(f"  Tên đăng nhập: {username}")
        print(f"  Họ và tên: {user.get('firstname')} {user.get('lastname')}")
        print(f"  Vai trò: {role}")
        print(f"  Trạng thái hiện tại: {'Đang hoạt động' if current_status else 'Đã khóa'}")

        # Không cho phép khóa tài khoản admin hiện tại
        if username == self.current_user.get('username'):
            print("\n⚠️  KHÔNG THỂ KHÓA/MỞ TÀI KHOẢN CỦA CHÍNH BẠN!")
            input("\nNhấn Enter để tiếp tục...")
            return

        action = "khóa" if current_status else "mở"
        confirm = input(f"\nBạn có chắc chắn muốn {action} tài khoản này? (y/n): ").strip().lower()

        if confirm != 'y':
            print(f"\nĐã hủy thao tác {action} tài khoản.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Xác định file dữ liệu
        if role == 'admin':
            filepath = self.data_files['admin']
        elif role == 'lecturer':
            filepath = self.data_files['teacher']
        else:  # student
            filepath = self.data_files['student']

        # Đọc và cập nhật dữ liệu
        users = self.read_file(filepath)
        updated = False

        for u in users:
            if u.get('username') == username:
                u['is_active'] = not current_status
                updated = True
                break

        if updated:
            # Lưu dữ liệu
            if self.save_to_file(filepath, users, 'w'):
                new_status = "khóa" if current_status else "mở"
                print(f"\n✓ Đã {new_status} tài khoản thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")
        else:
            print("\n✗ Không tìm thấy người dùng!")

        input("\nNhấn Enter để tiếp tục...")

    def search_user(self):
        """Tìm kiếm người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM NGƯỜI DÙNG")
        print("="*50)

        print("\nTiêu chí tìm kiếm:")
        print("1. Theo tên đăng nhập")
        print("2. Theo họ tên")
        print("3. Theo email")
        print("4. Theo vai trò")
        print("5. Theo trạng thái")
        print("6. Quay lại")

        choice = input("\nChọn tiêu chí tìm kiếm (1-6): ").strip()

        if choice == '1':
            self.search_by_username()
        elif choice == '2':
            self.search_by_name()
        elif choice == '3':
            self.search_by_email()
        elif choice == '4':
            self.search_by_role()
        elif choice == '5':
            self.search_by_status()
        elif choice == '6':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def search_by_username(self):
        """Tìm kiếm theo tên đăng nhập"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM THEO TÊN ĐĂNG NHẬP")
        print("="*50)

        search_term = input("\nNhập tên đăng nhập (hoặc một phần): ").strip().lower()

        if not search_term:
            print("\nVui lòng nhập từ khóa tìm kiếm!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc tất cả người dùng
        all_users = []

        # Đọc admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            admin['role'] = 'admin'
            all_users.append(admin)

        # Đọc giảng viên
        lecturers = self.read_file(self.data_files['teacher'])
        for lecturer in lecturers:
            lecturer['role'] = 'lecturer'
            all_users.append(lecturer)

        # Đọc sinh viên
        students = self.read_file(self.data_files['student'])
        for student in students:
            student['role'] = 'student'
            all_users.append(student)

        # Tìm kiếm
        results = []
        for user in all_users:
            username = user.get('username', '').lower()
            if search_term in username:
                results.append(user)

        self.display_search_results(results, f"theo tên đăng nhập chứa '{search_term}'")

    def search_by_name(self):
        """Tìm kiếm theo họ tên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM THEO HỌ TÊN")
        print("="*50)

        search_term = input("\nNhập họ tên (hoặc một phần): ").strip().lower()

        if not search_term:
            print("\nVui lòng nhập từ khóa tìm kiếm!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc tất cả người dùng
        all_users = []

        # Đọc admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            admin['role'] = 'admin'
            all_users.append(admin)

        # Đọc giảng viên
        lecturers = self.read_file(self.data_files['teacher'])
        for lecturer in lecturers:
            lecturer['role'] = 'lecturer'
            all_users.append(lecturer)

        # Đọc sinh viên
        students = self.read_file(self.data_files['student'])
        for student in students:
            student['role'] = 'student'
            all_users.append(student)

        # Tìm kiếm
        results = []
        for user in all_users:
            firstname = user.get('firstname', '').lower()
            lastname = user.get('lastname', '').lower()
            fullname = f"{firstname} {lastname}"

            if (search_term in firstname or
                search_term in lastname or
                search_term in fullname):
                results.append(user)

        self.display_search_results(results, f"theo họ tên chứa '{search_term}'")

    def search_by_email(self):
        """Tìm kiếm theo email"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM THEO EMAIL")
        print("="*50)

        search_term = input("\nNhập email (hoặc một phần): ").strip().lower()

        if not search_term:
            print("\nVui lòng nhập từ khóa tìm kiếm!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc tất cả người dùng
        all_users = []

        # Đọc admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            admin['role'] = 'admin'
            all_users.append(admin)

        # Đọc giảng viên
        lecturers = self.read_file(self.data_files['teacher'])
        for lecturer in lecturers:
            lecturer['role'] = 'lecturer'
            all_users.append(lecturer)

        # Đọc sinh viên
        students = self.read_file(self.data_files['student'])
        for student in students:
            student['role'] = 'student'
            all_users.append(student)

        # Tìm kiếm
        results = []
        for user in all_users:
            email = user.get('email', '').lower()
            if search_term in email:
                results.append(user)

        self.display_search_results(results, f"theo email chứa '{search_term}'")

    def search_by_role(self):
        """Tìm kiếm theo vai trò"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM THEO VAI TRÒ")
        print("="*50)

        print("\nChọn vai trò:")
        print("1. Quản trị viên")
        print("2. Giảng viên")
        print("3. Sinh viên")
        print("4. Quay lại")

        choice = input("\nChọn vai trò (1-4): ").strip()

        if choice == '4':
            return

        role_map = {'1': 'admin', '2': 'lecturer', '3': 'student'}
        role = role_map.get(choice)

        if not role:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc tất cả người dùng
        all_users = []

        # Đọc admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            admin['role'] = 'admin'
            all_users.append(admin)

        # Đọc giảng viên
        lecturers = self.read_file(self.data_files['teacher'])
        for lecturer in lecturers:
            lecturer['role'] = 'lecturer'
            all_users.append(lecturer)

        # Đọc sinh viên
        students = self.read_file(self.data_files['student'])
        for student in students:
            student['role'] = 'student'
            all_users.append(student)

        # Tìm kiếm theo vai trò
        results = [user for user in all_users if user.get('role') == role]

        role_names = {
            'admin': 'Quản trị viên',
            'lecturer': 'Giảng viên',
            'student': 'Sinh viên'
        }
        role_display = role_names.get(role, role)

        self.display_search_results(results, f"theo vai trò '{role_display}'")

    def search_by_status(self):
        """Tìm kiếm theo trạng thái"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM THEO TRẠNG THÁI")
        print("="*50)

        print("\nChọn trạng thái:")
        print("1. Đang hoạt động")
        print("2. Đã khóa")
        print("3. Quay lại")

        choice = input("\nChọn trạng thái (1-3): ").strip()

        if choice == '3':
            return

        status_map = {'1': True, '2': False}
        status = status_map.get(choice)

        if status is None:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc tất cả người dùng
        all_users = []

        # Đọc admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            admin['role'] = 'admin'
            all_users.append(admin)

        # Đọc giảng viên
        lecturers = self.read_file(self.data_files['teacher'])
        for lecturer in lecturers:
            lecturer['role'] = 'lecturer'
            all_users.append(lecturer)

        # Đọc sinh viên
        students = self.read_file(self.data_files['student'])
        for student in students:
            student['role'] = 'student'
            all_users.append(student)

        # Tìm kiếm theo trạng thái
        results = [user for user in all_users if user.get('is_active', True) == status]

        status_display = "đang hoạt động" if status else "đã khóa"

        self.display_search_results(results, f"theo trạng thái '{status_display}'")

    def display_search_results(self, results, search_criteria):
        """Hiển thị kết quả tìm kiếm"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KẾT QUẢ TÌM KIẾM")
        print("="*50)

        if not results:
            print(f"\nKhông tìm thấy người dùng nào {search_criteria}!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nTìm thấy {len(results)} người dùng {search_criteria}:")
        print("\n" + "-"*100)
        print(f"{'STT':<5} {'Username':<15} {'Vai trò':<12} {'Họ và tên':<25} {'Email':<25} {'Trạng thái':<10}")
        print("-"*100)

        for i, user in enumerate(results, 1):
            username = user.get('username', 'N/A')
            role = user.get('role', 'N/A')
            fullname = f"{user.get('firstname', '')} {user.get('lastname', '')}"
            email = user.get('email', 'N/A')
            is_active = user.get('is_active', True)

            # Chuyển đổi tên vai trò
            role_names = {
                'admin': 'Quản trị',
                'lecturer': 'Giảng viên',
                'student': 'Sinh viên'
            }
            role_display = role_names.get(role, role)

            # Trạng thái
            status = "Hoạt động" if is_active else "Đã khóa"

            print(f"{i:<5} {username:<15} {role_display:<12} {fullname:<25} {email:<25} {status:<10}")

        print("-"*100)

        # Tùy chọn xem chi tiết
        print("\n1. Xem chi tiết người dùng")
        print("2. Quay lại")

        sub_choice = input("\nChọn chức năng (1-2): ").strip()

        if sub_choice == '1':
            try:
                stt = int(input("\nNhập STT người dùng: ").strip()) - 1
                if 0 <= stt < len(results):
                    self.view_user_detail(results[stt])
                else:
                    print("\nSTT không hợp lệ!")
            except ValueError:
                print("\nVui lòng nhập số!")
        elif sub_choice == '2':
            return

        input("\nNhấn Enter để tiếp tục...")

    def toggle_user_status(self):
        """Khóa/Mở tài khoản người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KHÓA/MỞ TÀI KHOẢN NGƯỜI DÙNG")
        print("="*50)

        print("\n1. Khóa tài khoản")
        print("2. Mở tài khoản")
        print("3. Khóa/Mở nhiều tài khoản")
        print("4. Quay lại")

        choice = input("\nChọn chức năng (1-4): ").strip()

        if choice == '1':
            self.lock_user_account()
        elif choice == '2':
            self.unlock_user_account()
        elif choice == '3':
            self.batch_toggle_user_status()
        elif choice == '4':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def lock_user_account(self):
        """Khóa tài khoản người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KHÓA TÀI KHOẢN NGƯỜI DÙNG")
        print("="*50)

        username = input("\nNhập tên đăng nhập cần khóa: ").strip()

        if not username:
            print("\nVui lòng nhập tên đăng nhập!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Không cho phép khóa tài khoản admin hiện tại
        if username == self.current_user.get('username'):
            print("\n⚠️  KHÔNG THỂ KHÓA TÀI KHOẢN CỦA CHÍNH BẠN!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Tìm người dùng
        user = None
        role = None
        filepath = None

        # Tìm trong admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            if admin.get('username') == username:
                user = admin
                role = 'admin'
                filepath = self.data_files['admin']
                break

        # Tìm trong giảng viên
        if not user:
            lecturers = self.read_file(self.data_files['teacher'])
            for lecturer in lecturers:
                if lecturer.get('username') == username:
                    user = lecturer
                    role = 'lecturer'
                    filepath = self.data_files['teacher']
                    break

        # Tìm trong sinh viên
        if not user:
            students = self.read_file(self.data_files['student'])
            for student in students:
                if student.get('username') == username:
                    user = student
                    role = 'student'
                    filepath = self.data_files['student']
                    break

        if not user:
            print(f"\n✗ Không tìm thấy người dùng với username: {username}")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Kiểm tra trạng thái hiện tại
        current_status = user.get('is_active', True)
        if not current_status:
            print(f"\n✗ Tài khoản '{username}' đã bị khóa trước đó!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nThông tin người dùng:")
        print(f"  Tên đăng nhập: {username}")
        print(f"  Họ và tên: {user.get('firstname')} {user.get('lastname')}")
        print(f"  Vai trò: {role}")
        print(f"  Trạng thái hiện tại: Đang hoạt động")

        confirm = input("\nBạn có chắc chắn muốn khóa tài khoản này? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\nĐã hủy thao tác khóa tài khoản.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc và cập nhật dữ liệu
        users = self.read_file(filepath)
        updated = False

        for u in users:
            if u.get('username') == username:
                u['is_active'] = False
                updated = True
                break

        if updated:
            # Lưu dữ liệu
            if self.save_to_file(filepath, users, 'w'):
                print(f"\n✓ Đã khóa tài khoản '{username}' thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")
        else:
            print("\n✗ Không tìm thấy người dùng!")

        input("\nNhấn Enter để tiếp tục...")

    def unlock_user_account(self):
        """Mở tài khoản người dùng"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     MỞ TÀI KHOẢN NGƯỜI DÙNG")
        print("="*50)

        username = input("\nNhập tên đăng nhập cần mở: ").strip()

        if not username:
            print("\nVui lòng nhập tên đăng nhập!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Tìm người dùng
        user = None
        role = None
        filepath = None

        # Tìm trong admin
        admins = self.read_file(self.data_files['admin'])
        for admin in admins:
            if admin.get('username') == username:
                user = admin
                role = 'admin'
                filepath = self.data_files['admin']
                break

        # Tìm trong giảng viên
        if not user:
            lecturers = self.read_file(self.data_files['teacher'])
            for lecturer in lecturers:
                if lecturer.get('username') == username:
                    user = lecturer
                    role = 'lecturer'
                    filepath = self.data_files['teacher']
                    break

        # Tìm trong sinh viên
        if not user:
            students = self.read_file(self.data_files['student'])
            for student in students:
                if student.get('username') == username:
                    user = student
                    role = 'student'
                    filepath = self.data_files['student']
                    break

        if not user:
            print(f"\n✗ Không tìm thấy người dùng với username: {username}")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Kiểm tra trạng thái hiện tại
        current_status = user.get('is_active', True)
        if current_status:
            print(f"\n✗ Tài khoản '{username}' đang hoạt động, không cần mở!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nThông tin người dùng:")
        print(f"  Tên đăng nhập: {username}")
        print(f"  Họ và tên: {user.get('firstname')} {user.get('lastname')}")
        print(f"  Vai trò: {role}")
        print(f"  Trạng thái hiện tại: Đã khóa")

        confirm = input("\nBạn có chắc chắn muốn mở tài khoản này? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\nĐã hủy thao tác mở tài khoản.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc và cập nhật dữ liệu
        users = self.read_file(filepath)
        updated = False

        for u in users:
            if u.get('username') == username:
                u['is_active'] = True
                updated = True
                break

        if updated:
            # Lưu dữ liệu
            if self.save_to_file(filepath, users, 'w'):
                print(f"\n✓ Đã mở tài khoản '{username}' thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")
        else:
            print("\n✗ Không tìm thấy người dùng!")

        input("\nNhấn Enter để tiếp tục...")

    def batch_toggle_user_status(self):
        """Khóa/Mở nhiều tài khoản cùng lúc"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KHÓA/MỞ NHIỀU TÀI KHOẢN")
        print("="*50)

        print("\n1. Khóa tất cả tài khoản sinh viên")
        print("2. Khóa tất cả tài khoản giảng viên")
        print("3. Mở tất cả tài khoản sinh viên")
        print("4. Mở tất cả tài khoản giảng viên")
        print("5. Khóa tài khoản không hoạt động trong X ngày")
        print("6. Quay lại")

        choice = input("\nChọn chức năng (1-6): ").strip()

        if choice == '1':
            self.lock_all_students()
        elif choice == '2':
            self.lock_all_lecturers()
        elif choice == '3':
            self.unlock_all_students()
        elif choice == '4':
            self.unlock_all_lecturers()
        elif choice == '5':
            self.lock_inactive_accounts()
        elif choice == '6':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def lock_all_students(self):
        """Khóa tất cả tài khoản sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KHÓA TẤT CẢ TÀI KHOẢN SINH VIÊN")
        print("="*50)

        confirm = input("\n⚠️ CẢNH BÁO: Bạn có chắc chắn muốn khóa TẤT CẢ tài khoản sinh viên? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\nĐã hủy thao tác.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc dữ liệu sinh viên
        students = self.read_file(self.data_files['student'])

        if not students:
            print("\nKhông có sinh viên nào trong hệ thống!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Khóa tất cả sinh viên
        locked_count = 0
        already_locked = 0

        for student in students:
            if student.get('is_active', True):
                student['is_active'] = False
                locked_count += 1
            else:
                already_locked += 1

        # Lưu dữ liệu
        if self.save_to_file(self.data_files['student'], students, 'w'):
            print(f"\n✓ Đã khóa {locked_count} tài khoản sinh viên!")
            if already_locked > 0:
                print(f"  Có {already_locked} tài khoản đã bị khóa trước đó.")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def unlock_all_students(self):
        """Mở tất cả tài khoản sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     MỞ TẤT CẢ TÀI KHOẢN SINH VIÊN")
        print("="*50)

        confirm = input("\nBạn có chắc chắn muốn mở TẤT CẢ tài khoản sinh viên? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\nĐã hủy thao tác.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc dữ liệu sinh viên
        students = self.read_file(self.data_files['student'])

        if not students:
            print("\nKhông có sinh viên nào trong hệ thống!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Mở tất cả sinh viên
        unlocked_count = 0
        already_active = 0

        for student in students:
            if not student.get('is_active', True):
                student['is_active'] = True
                unlocked_count += 1
            else:
                already_active += 1

        # Lưu dữ liệu
        if self.save_to_file(self.data_files['student'], students, 'w'):
            print(f"\n✓ Đã mở {unlocked_count} tài khoản sinh viên!")
            if already_active > 0:
                print(f"  Có {already_active} tài khoản đang hoạt động trước đó.")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def lock_all_lecturers(self):
        """Khóa tất cả tài khoản giảng viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KHÓA TẤT CẢ TÀI KHOẢN GIẢNG VIÊN")
        print("="*50)

        confirm = input("\n⚠️ CẢNH BÁO: Bạn có chắc chắn muốn khóa TẤT CẢ tài khoản giảng viên? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\nĐã hủy thao tác.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc dữ liệu giảng viên
        lecturers = self.read_file(self.data_files['teacher'])

        if not lecturers:
            print("\nKhông có giảng viên nào trong hệ thống!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Khóa tất cả giảng viên
        locked_count = 0
        already_locked = 0

        for lecturer in lecturers:
            if lecturer.get('is_active', True):
                lecturer['is_active'] = False
                locked_count += 1
            else:
                already_locked += 1

        # Lưu dữ liệu
        if self.save_to_file(self.data_files['teacher'], lecturers, 'w'):
            print(f"\n✓ Đã khóa {locked_count} tài khoản giảng viên!")
            if already_locked > 0:
                print(f"  Có {already_locked} tài khoản đã bị khóa trước đó.")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def unlock_all_lecturers(self):
        """Mở tất cả tài khoản giảng viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     MỞ TẤT CẢ TÀI KHOẢN GIẢNG VIÊN")
        print("="*50)

        confirm = input("\nBạn có chắc chắn muốn mở TẤT CẢ tài khoản giảng viên? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\nĐã hủy thao tác.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Đọc dữ liệu giảng viên
        lecturers = self.read_file(self.data_files['teacher'])

        if not lecturers:
            print("\nKhông có giảng viên nào trong hệ thống!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Mở tất cả giảng viên
        unlocked_count = 0
        already_active = 0

        for lecturer in lecturers:
            if not lecturer.get('is_active', True):
                lecturer['is_active'] = True
                unlocked_count += 1
            else:
                already_active += 1

        # Lưu dữ liệu
        if self.save_to_file(self.data_files['teacher'], lecturers, 'w'):
            print(f"\n✓ Đã mở {unlocked_count} tài khoản giảng viên!")
            if already_active > 0:
                print(f"  Có {already_active} tài khoản đang hoạt động trước đó.")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def lock_inactive_accounts(self):
        """Khóa tài khoản không hoạt động trong X ngày"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     KHÓA TÀI KHOẢN KHÔNG HOẠT ĐỘNG")
        print("="*50)

        try:
            days = int(input("\nNhập số ngày không hoạt động để khóa: ").strip())

            if days <= 0:
                print("\nSố ngày phải lớn hơn 0!")
                input("\nNhấn Enter để tiếp tục...")
                return
        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        confirm = input(f"\nBạn có chắc chắn muốn khóa tài khoản không đăng nhập trong {days} ngày? (y/n): ").strip().lower()

        if confirm != 'y':
            print("\nĐã hủy thao tác.")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Tính ngày giới hạn
        limit_date = datetime.now() - timedelta(days=days)
        limit_date_str = limit_date.strftime('%Y-%m-%d %H:%M:%S')

        print(f"\nĐang tìm tài khoản không hoạt động từ: {limit_date_str}")

        # Lưu ý: Chức năng này yêu cầu có trường last_login trong dữ liệu người dùng
        # Để đơn giản, chúng ta sẽ giả sử tất cả tài khoản đều có trường last_login
        # Trong thực tế, cần cập nhật trường last_login mỗi khi người dùng đăng nhập

        print("\n⚠️  CHỨC NĂNG NÀY CẦN BỔ SUNG TRƯỜNG 'last_login' TRONG DỮ LIỆU NGƯỜI DÙNG")
        print("   VÀ CẬP NHẬT MỖI KHI NGƯỜI DÙNG ĐĂNG NHẬP THÀNH CÔNG.")

        # Đây là phần code mẫu, cần điều chỉnh cho phù hợp với cấu trúc dữ liệu thực tế
        locked_count = 0

        # Khóa tài khoản sinh viên không hoạt động
        students = self.read_file(self.data_files['student'])
        for student in students:
            last_login = student.get('last_login')
            if last_login:
                try:
                    last_login_date = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
                    if last_login_date < limit_date and student.get('is_active', True):
                        student['is_active'] = False
                        locked_count += 1
                except:
                    pass

        # Khóa tài khoản giảng viên không hoạt động
        lecturers = self.read_file(self.data_files['teacher'])
        for lecturer in lecturers:
            last_login = lecturer.get('last_login')
            if last_login:
                try:
                    last_login_date = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
                    if last_login_date < limit_date and lecturer.get('is_active', True):
                        lecturer['is_active'] = False
                        locked_count += 1
                except:
                    pass

        # Khóa tài khoản admin không hoạt động (trừ admin hiện tại)
        admins = self.read_file(self.data_files['admin'])
        current_username = self.current_user.get('username')
        for admin in admins:
            if admin.get('username') == current_username:
                continue

            last_login = admin.get('last_login')
            if last_login:
                try:
                    last_login_date = datetime.strptime(last_login, '%Y-%m-%d %H:%M:%S')
                    if last_login_date < limit_date and admin.get('is_active', True):
                        admin['is_active'] = False
                        locked_count += 1
                except:
                    pass

        # Lưu dữ liệu
        if (self.save_to_file(self.data_files['student'], students, 'w') and
            self.save_to_file(self.data_files['teacher'], lecturers, 'w') and
            self.save_to_file(self.data_files['admin'], admins, 'w')):
            print(f"\n✓ Đã khóa {locked_count} tài khoản không hoạt động trong {days} ngày!")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    # ========== QUẢN LÝ SINH VIÊN ==========

    def manage_students(self):
        """Quản lý sinh viên (Admin)"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     QUẢN LÝ SINH VIÊN")
        print("="*50)

        students = self.read_file(self.data_files['student'])

        if not students:
            print("\nChưa có sinh viên nào trong hệ thống!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nTổng số sinh viên: {len(students)}")
        print("\n1. Xem danh sách sinh viên")
        print("2. Thêm sinh viên")
        print("3. Chỉnh sửa thông tin")
        print("4. Xóa sinh viên")
        print("5. Tìm kiếm sinh viên")
        print("6. Xuất danh sách")
        print("7. Quay lại")

        choice = input("\nChọn chức năng (1-7): ").strip()

        if choice == '1':
            self.view_student_list(students)
        elif choice == '2':
            self.add_student()
        elif choice == '3':
            self.edit_student(students)
        elif choice == '4':
            self.delete_student(students)
        elif choice == '5':
            self.search_student(students)
        elif choice == '6':
            self.export_student_list(students)
        elif choice == '7':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def view_student_list(self, students):
        """Xem danh sách sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     DANH SÁCH SINH VIÊN")
        print("="*50)

        if not students:
            print("\nChưa có sinh viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Sắp xếp theo mã sinh viên
        students.sort(key=lambda x: x.get('std_code', ''))

        print("\n" + "-"*80)
        print(f"{'STT':<5} {'Mã SV':<10} {'Họ và tên':<25} {'Lớp':<10} {'Giới tính':<10} {'SĐT':<15}")
        print("-"*80)

        for i, student in enumerate(students, 1):
            std_code = student.get('std_code', 'N/A')
            fullname = f"{student.get('firstname', '')} {student.get('lastname', '')}"
            class_ = student.get('class_', 'N/A')
            gender = student.get('gender', 'N/A')
            phone = student.get('phone', 'N/A')

            print(f"{i:<5} {std_code:<10} {fullname:<25} {class_:<10} {gender:<10} {phone:<15}")

        print(f"\nTổng cộng: {len(students)} sinh viên")

        # Thêm các tùy chọn
        print("\n1. Xem chi tiết sinh viên")
        print("2. Quay lại")

        sub_choice = input("\nChọn (1-2): ").strip()

        if sub_choice == '1':
            try:
                stt = int(input("\nNhập STT sinh viên: ").strip()) - 1
                if 0 <= stt < len(students):
                    self.view_student_detail(students[stt])
                else:
                    print("\nSTT không hợp lệ!")
            except ValueError:
                print("\nVui lòng nhập số!")

        input("\nNhấn Enter để tiếp tục...")

    def add_student(self):
        """Thêm sinh viên mới"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THÊM SINH VIÊN MỚI")
        print("="*50)

        print("\nNhập thông tin sinh viên:")

        username = input("Tên đăng nhập: ").strip()

        # Kiểm tra username đã tồn tại chưa
        if self.check_user_exists(username):
            print(f"\n✗ Tên đăng nhập '{username}' đã tồn tại!")
            input("\nNhấn Enter để tiếp tục...")
            return

        password = input("Mật khẩu: ").strip()
        email = input("Email: ").strip()
        firstname = input("Họ và tên đệm: ").strip()
        lastname = input("Tên: ").strip()
        std_code = input("Mã sinh viên: ").strip()
        class_ = input("Lớp: ").strip()
        gender = input("Giới tính (Nam/Nữ): ").strip()
        phone = input("Số điện thoại: ").strip()
        national_code = input("CMND/CCCD: ").strip()

        student_data = {
            'username': username,
            'password': password,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'std_code': std_code,
            'class_': class_,
            'gender': gender,
            'phone': phone,
            'national_code': national_code,
            'role': 'student',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': True
        }

        # Lưu vào file
        students = self.read_file(self.data_files['student'])
        students.append(student_data)

        if self.save_to_file(self.data_files['student'], students, 'w'):
            print(f"\n✓ Đã thêm sinh viên '{firstname} {lastname}' thành công!")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def view_student_detail(self, student):
        """Xem chi tiết thông tin sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THÔNG TIN CHI TIẾT SINH VIÊN")
        print("="*50)

        print(f"\n📋 THÔNG TIN CÁ NHÂN:")
        print(f"  Mã sinh viên: {student.get('std_code', 'N/A')}")
        print(f"  Họ và tên: {student.get('firstname', '')} {student.get('lastname', '')}")
        print(f"  Lớp: {student.get('class_', 'N/A')}")
        print(f"  Giới tính: {student.get('gender', 'N/A')}")
        print(f"  Ngày sinh: {student.get('date_of_birth', 'Chưa cập nhật')}")
        print(f"  CMND/CCCD: {student.get('national_code', 'Chưa cập nhật')}")
        print(f"  Số điện thoại: {student.get('phone', 'Chưa cập nhật')}")
        print(f"  Email: {student.get('email', 'N/A')}")
        print(f"  Địa chỉ: {student.get('address', 'Chưa cập nhật')}")
        print(f"  Ngày nhập học: {student.get('enrollment_date', 'Chưa cập nhật')}")

        # Lấy thông tin học tập
        student_id = student.get('username')

        # Môn học đang học
        courses = self.read_file(self.data_files['courses'])
        enrolled_courses = [c for c in courses if student_id in c.get('enrolled_students', [])]

        # Điểm số
        grades = self.read_file(self.data_files['grades'])
        student_grades = [g for g in grades if g.get('student_id') == student_id]

        print(f"\n📚 THÔNG TIN HỌC TẬP:")
        print(f"  Số môn đang học: {len(enrolled_courses)}")
        print(f"  Số môn đã có điểm: {len(student_grades)}")

        if student_grades:
            # Tính GPA
            total_grade_points = 0
            total_credits = 0

            for grade in student_grades:
                course_id = grade.get('course_id')
                course = next((c for c in courses if c.get('course_id') == course_id), None)
                if course:
                    credits = course.get('credits', 3)
                    grade_letter = grade.get('grade_letter', 'F')

                    # Chuyển đổi điểm chữ sang điểm số
                    grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
                    grade_points = grade_map.get(grade_letter, 0.0)

                    total_grade_points += grade_points * credits
                    total_credits += credits

            if total_credits > 0:
                gpa = total_grade_points / total_credits
                print(f"  GPA hiện tại: {gpa:.2f}")

        input("\n\nNhấn Enter để tiếp tục...")

    def edit_student(self, students):
        """Chỉnh sửa thông tin sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHỈNH SỬA THÔNG TIN SINH VIÊN")
        print("="*50)

        if not students:
            print("\nChưa có sinh viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nDanh sách sinh viên:")
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.get('std_code')} - {student.get('firstname')} {student.get('lastname')}")

        try:
            choice = int(input("\nChọn sinh viên cần sửa (số): ").strip()) - 1
            if choice < 0 or choice >= len(students):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            student = students[choice]
            print(f"\nThông tin hiện tại của {student.get('firstname')} {student.get('lastname')}:")
            print(f"1. Mã sinh viên: {student.get('std_code')}")
            print(f"2. Họ và tên đệm: {student.get('firstname')}")
            print(f"3. Tên: {student.get('lastname')}")
            print(f"4. Lớp: {student.get('class_')}")
            print(f"5. Giới tính: {student.get('gender')}")
            print(f"6. Email: {student.get('email')}")
            print(f"7. Số điện thoại: {student.get('phone')}")

            field = input("\nChọn trường cần sửa (1-7, 0 để hủy): ").strip()

            if field == '0':
                return
            elif field == '1':
                new_value = input("Nhập mã sinh viên mới: ").strip()
                student['std_code'] = new_value
            elif field == '2':
                new_value = input("Nhập họ và tên đệm mới: ").strip()
                student['firstname'] = new_value
            elif field == '3':
                new_value = input("Nhập tên mới: ").strip()
                student['lastname'] = new_value
            elif field == '4':
                new_value = input("Nhập lớp mới: ").strip()
                student['class_'] = new_value
            elif field == '5':
                new_value = input("Nhập giới tính mới (Nam/Nữ): ").strip()
                student['gender'] = new_value
            elif field == '6':
                new_value = input("Nhập email mới: ").strip()
                student['email'] = new_value
            elif field == '7':
                new_value = input("Nhập số điện thoại mới: ").strip()
                student['phone'] = new_value
            else:
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            # Lưu dữ liệu
            if self.save_to_file(self.data_files['student'], students, 'w'):
                print("\n✓ Đã cập nhật thông tin sinh viên thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    def delete_student(self, students):
        """Xóa sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     XÓA SINH VIÊN")
        print("="*50)

        if not students:
            print("\nChưa có sinh viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nDanh sách sinh viên:")
        for i, student in enumerate(students, 1):
            print(f"{i}. {student.get('std_code')} - {student.get('firstname')} {student.get('lastname')}")

        try:
            choice = int(input("\nChọn sinh viên cần xóa (số): ").strip()) - 1
            if choice < 0 or choice >= len(students):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            student = students[choice]
            print(f"\nThông tin sinh viên sẽ bị xóa:")
            print(f"  Mã SV: {student.get('std_code')}")
            print(f"  Họ tên: {student.get('firstname')} {student.get('lastname')}")
            print(f"  Lớp: {student.get('class_')}")

            confirm = input("\nBạn có chắc chắn muốn xóa sinh viên này? (y/n): ").strip().lower()

            if confirm == 'y':
                # Xóa sinh viên khỏi danh sách
                del students[choice]

                # Xóa sinh viên khỏi các môn học
                courses = self.read_file(self.data_files['courses'])
                student_id = student.get('username')

                for course in courses:
                    if 'enrolled_students' in course and student_id in course['enrolled_students']:
                        course['enrolled_students'].remove(student_id)

                # Xóa điểm của sinh viên
                grades = self.read_file(self.data_files['grades'])
                grades = [g for g in grades if g.get('student_id') != student_id]

                # Lưu dữ liệu
                if (self.save_to_file(self.data_files['student'], students, 'w') and
                    self.save_to_file(self.data_files['courses'], courses, 'w') and
                    self.save_to_file(self.data_files['grades'], grades, 'w')):
                    print("\n✓ Đã xóa sinh viên thành công!")
                else:
                    print("\n✗ Lỗi khi lưu dữ liệu!")
            else:
                print("\nĐã hủy thao tác xóa.")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    def search_student(self, students):
        """Tìm kiếm sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM SINH VIÊN")
        print("="*50)

        if not students:
            print("\nChưa có sinh viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nTiêu chí tìm kiếm:")
        print("1. Theo mã sinh viên")
        print("2. Theo họ tên")
        print("3. Theo lớp")
        print("4. Quay lại")

        choice = input("\nChọn tiêu chí (1-4): ").strip()

        if choice == '1':
            search_term = input("\nNhập mã sinh viên: ").strip().lower()
            results = [s for s in students if search_term in s.get('std_code', '').lower()]
        elif choice == '2':
            search_term = input("\nNhập họ tên (hoặc một phần): ").strip().lower()
            results = []
            for s in students:
                fullname = f"{s.get('firstname', '')} {s.get('lastname', '')}".lower()
                if search_term in fullname:
                    results.append(s)
        elif choice == '3':
            search_term = input("\nNhập tên lớp: ").strip().lower()
            results = [s for s in students if search_term in s.get('class_', '').lower()]
        elif choice == '4':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Hiển thị kết quả
        print(f"\nTìm thấy {len(results)} sinh viên:")
        if results:
            print("\n" + "-"*80)
            print(f"{'STT':<5} {'Mã SV':<10} {'Họ và tên':<25} {'Lớp':<10} {'Giới tính':<10} {'SĐT':<15}")
            print("-"*80)

            for i, student in enumerate(results, 1):
                std_code = student.get('std_code', 'N/A')
                fullname = f"{student.get('firstname', '')} {student.get('lastname', '')}"
                class_ = student.get('class_', 'N/A')
                gender = student.get('gender', 'N/A')
                phone = student.get('phone', 'N/A')

                print(f"{i:<5} {std_code:<10} {fullname:<25} {class_:<10} {gender:<10} {phone:<15}")

        input("\n\nNhấn Enter để tiếp tục...")

    def export_student_list(self, students):
        """Xuất danh sách sinh viên ra file"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     XUẤT DANH SÁCH SINH VIÊN")
        print("="*50)

        if not students:
            print("\nChưa có sinh viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nChọn định dạng xuất:")
        print("1. Text file (.txt)")
        print("2. CSV file (.csv)")
        print("3. Quay lại")

        choice = input("\nChọn định dạng (1-3): ").strip()

        if choice == '1':
            filename = "students_list.txt"
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("DANH SÁCH SINH VIÊN\n")
                    f.write("="*80 + "\n")
                    f.write(f"{'STT':<5} {'Mã SV':<10} {'Họ và tên':<25} {'Lớp':<10} {'Giới tính':<10} {'Email':<25}\n")
                    f.write("-"*80 + "\n")

                    for i, student in enumerate(students, 1):
                        std_code = student.get('std_code', 'N/A')
                        fullname = f"{student.get('firstname', '')} {student.get('lastname', '')}"
                        class_ = student.get('class_', 'N/A')
                        gender = student.get('gender', 'N/A')
                        email = student.get('email', 'N/A')

                        f.write(f"{i:<5} {std_code:<10} {fullname:<25} {class_:<10} {gender:<10} {email:<25}\n")

                    f.write("="*80 + "\n")
                    f.write(f"Tổng số: {len(students)} sinh viên\n")
                    f.write(f"Ngày xuất: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")

                print(f"\n✓ Đã xuất danh sách sinh viên ra file: {filename}")

            except Exception as e:
                print(f"\n✗ Lỗi khi xuất file: {e}")

        elif choice == '2':
            filename = "students_list.csv"
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['STT', 'Mã SV', 'Họ và tên', 'Lớp', 'Giới tính', 'Email', 'SĐT'])

                    for i, student in enumerate(students, 1):
                        std_code = student.get('std_code', 'N/A')
                        fullname = f"{student.get('firstname', '')} {student.get('lastname', '')}"
                        class_ = student.get('class_', 'N/A')
                        gender = student.get('gender', 'N/A')
                        email = student.get('email', 'N/A')
                        phone = student.get('phone', 'N/A')

                        writer.writerow([i, std_code, fullname, class_, gender, email, phone])

                print(f"\n✓ Đã xuất danh sách sinh viên ra file: {filename}")

            except Exception as e:
                print(f"\n✗ Lỗi khi xuất file: {e}")

        elif choice == '3':
            return
        else:
            print("\nLựa chọn không hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    # ========== QUẢN LÝ GIẢNG VIÊN (ADMIN) ==========

    def manage_lecturers(self):
        """Quản lý giảng viên (Admin)"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     QUẢN LÝ GIẢNG VIÊN")
        print("="*50)

        lecturers = self.read_file(self.data_files['teacher'])

        if not lecturers:
            print("\nChưa có giảng viên nào trong hệ thống!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nTổng số giảng viên: {len(lecturers)}")
        print("\n1. Xem danh sách giảng viên")
        print("2. Thêm giảng viên")
        print("3. Chỉnh sửa thông tin")
        print("4. Xóa giảng viên")
        print("5. Tìm kiếm giảng viên")
        print("6. Phân công môn học")
        print("7. Quay lại")

        choice = input("\nChọn chức năng (1-7): ").strip()

        if choice == '1':
            self.view_lecturer_list(lecturers)
        elif choice == '2':
            self.add_lecturer()
        elif choice == '3':
            self.edit_lecturer(lecturers)
        elif choice == '4':
            self.delete_lecturer(lecturers)
        elif choice == '5':
            self.search_lecturer(lecturers)
        elif choice == '6':
            self.assign_course_to_lecturer()
        elif choice == '7':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def view_lecturer_list(self, lecturers):
        """Xem danh sách giảng viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     DANH SÁCH GIẢNG VIÊN")
        print("="*50)

        if not lecturers:
            print("\nChưa có giảng viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Sắp xếp theo mã giảng viên
        lecturers.sort(key=lambda x: x.get('employee_id', ''))

        print("\n" + "-"*80)
        print(f"{'STT':<5} {'Mã GV':<10} {'Họ và tên':<25} {'Khoa':<15} {'Chuyên ngành':<20}")
        print("-"*80)

        for i, lecturer in enumerate(lecturers, 1):
            employee_id = lecturer.get('employee_id', 'N/A')
            fullname = f"{lecturer.get('firstname', '')} {lecturer.get('lastname', '')}"
            department = lecturer.get('department', 'N/A')
            specialization = lecturer.get('specialization', 'N/A')

            print(f"{i:<5} {employee_id:<10} {fullname:<25} {department:<15} {specialization:<20}")

        print(f"\nTổng cộng: {len(lecturers)} giảng viên")
        input("\nNhấn Enter để tiếp tục...")

    def add_lecturer(self):
        """Thêm giảng viên mới"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THÊM GIẢNG VIÊN MỚI")
        print("="*50)

        print("\nNhập thông tin giảng viên:")

        username = input("Tên đăng nhập: ").strip()

        # Kiểm tra username đã tồn tại chưa
        if self.check_user_exists(username):
            print(f"\n✗ Tên đăng nhập '{username}' đã tồn tại!")
            input("\nNhấn Enter để tiếp tục...")
            return

        password = input("Mật khẩu: ").strip()
        email = input("Email: ").strip()
        firstname = input("Họ và tên đệm: ").strip()
        lastname = input("Tên: ").strip()
        employee_id = input("Mã giảng viên: ").strip()
        department = input("Khoa: ").strip()
        specialization = input("Chuyên ngành: ").strip()
        phone = input("Số điện thoại: ").strip()

        lecturer_data = {
            'username': username,
            'password': password,
            'email': email,
            'firstname': firstname,
            'lastname': lastname,
            'employee_id': employee_id,
            'department': department,
            'specialization': specialization,
            'phone': phone,
            'role': 'lecturer',
            'assigned_courses': [],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': True
        }

        # Lưu vào file
        lecturers = self.read_file(self.data_files['teacher'])
        lecturers.append(lecturer_data)

        if self.save_to_file(self.data_files['teacher'], lecturers, 'w'):
            print(f"\n✓ Đã thêm giảng viên '{firstname} {lastname}' thành công!")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def edit_lecturer(self, lecturers):
        """Chỉnh sửa thông tin giảng viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHỈNH SỬA THÔNG TIN GIẢNG VIÊN")
        print("="*50)

        if not lecturers:
            print("\nChưa có giảng viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nDanh sách giảng viên:")
        for i, lecturer in enumerate(lecturers, 1):
            print(f"{i}. {lecturer.get('employee_id')} - {lecturer.get('firstname')} {lecturer.get('lastname')}")

        try:
            choice = int(input("\nChọn giảng viên cần sửa (số): ").strip()) - 1
            if choice < 0 or choice >= len(lecturers):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            lecturer = lecturers[choice]
            print(f"\nThông tin hiện tại của {lecturer.get('firstname')} {lecturer.get('lastname')}:")
            print(f"1. Mã giảng viên: {lecturer.get('employee_id')}")
            print(f"2. Họ và tên đệm: {lecturer.get('firstname')}")
            print(f"3. Tên: {lecturer.get('lastname')}")
            print(f"4. Email: {lecturer.get('email')}")
            print(f"5. Khoa: {lecturer.get('department')}")
            print(f"6. Chuyên ngành: {lecturer.get('specialization')}")
            print(f"7. Số điện thoại: {lecturer.get('phone')}")

            field = input("\nChọn trường cần sửa (1-7, 0 để hủy): ").strip()

            if field == '0':
                return

            if field == '1':
                new_value = input("Nhập mã giảng viên mới: ").strip()
                lecturer['employee_id'] = new_value
            elif field == '2':
                new_value = input("Nhập họ và tên đệm mới: ").strip()
                lecturer['firstname'] = new_value
            elif field == '3':
                new_value = input("Nhập tên mới: ").strip()
                lecturer['lastname'] = new_value
            elif field == '4':
                new_value = input("Nhập email mới: ").strip()
                lecturer['email'] = new_value
            elif field == '5':
                new_value = input("Nhập khoa mới: ").strip()
                lecturer['department'] = new_value
            elif field == '6':
                new_value = input("Nhập chuyên ngành mới: ").strip()
                lecturer['specialization'] = new_value
            elif field == '7':
                new_value = input("Nhập số điện thoại mới: ").strip()
                lecturer['phone'] = new_value
            else:
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            # Lưu dữ liệu
            if self.save_to_file(self.data_files['teacher'], lecturers, 'w'):
                print("\n✓ Đã cập nhật thông tin giảng viên thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    def delete_lecturer(self, lecturers):
        """Xóa giảng viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     XÓA GIẢNG VIÊN")
        print("="*50)

        if not lecturers:
            print("\nChưa có giảng viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nDanh sách giảng viên:")
        for i, lecturer in enumerate(lecturers, 1):
            print(f"{i}. {lecturer.get('employee_id')} - {lecturer.get('firstname')} {lecturer.get('lastname')}")

        try:
            choice = int(input("\nChọn giảng viên cần xóa (số): ").strip()) - 1
            if choice < 0 or choice >= len(lecturers):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            lecturer = lecturers[choice]
            lecturer_id = lecturer.get('username')

            # Kiểm tra xem giảng viên có đang dạy môn nào không
            courses = self.read_file(self.data_files['courses'])
            teaching_courses = [c for c in courses if c.get('lecturer_id') == lecturer_id]

            if teaching_courses:
                print(f"\n⚠️  KHÔNG THỂ XÓA GIẢNG VIÊN!")
                print(f"Giảng viên này đang dạy {len(teaching_courses)} môn:")
                for course in teaching_courses:
                    print(f"  • {course.get('course_name')}")
                print("\nHãy phân công lại các môn học trước khi xóa giảng viên.")
                input("\nNhấn Enter để tiếp tục...")
                return

            print(f"\nThông tin giảng viên sẽ bị xóa:")
            print(f"  Mã GV: {lecturer.get('employee_id')}")
            print(f"  Họ tên: {lecturer.get('firstname')} {lecturer.get('lastname')}")
            print(f"  Khoa: {lecturer.get('department')}")

            confirm = input("\nBạn có chắc chắn muốn xóa giảng viên này? (y/n): ").strip().lower()

            if confirm == 'y':
                # Xóa giảng viên
                del lecturers[choice]

                # Lưu dữ liệu
                if self.save_to_file(self.data_files['teacher'], lecturers, 'w'):
                    print("\n✓ Đã xóa giảng viên thành công!")
                else:
                    print("\n✗ Lỗi khi lưu dữ liệu!")
            else:
                print("\nĐã hủy thao tác xóa.")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    def search_lecturer(self, lecturers):
        """Tìm kiếm giảng viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TÌM KIẾM GIẢNG VIÊN")
        print("="*50)

        if not lecturers:
            print("\nChưa có giảng viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nTiêu chí tìm kiếm:")
        print("1. Theo mã giảng viên")
        print("2. Theo họ tên")
        print("3. Theo khoa")
        print("4. Quay lại")

        choice = input("\nChọn tiêu chí (1-4): ").strip()

        if choice == '1':
            search_term = input("\nNhập mã giảng viên: ").strip().lower()
            results = [l for l in lecturers if search_term in l.get('employee_id', '').lower()]
        elif choice == '2':
            search_term = input("\nNhập họ tên (hoặc một phần): ").strip().lower()
            results = []
            for l in lecturers:
                fullname = f"{l.get('firstname', '')} {l.get('lastname', '')}".lower()
                if search_term in fullname:
                    results.append(l)
        elif choice == '3':
            search_term = input("\nNhập tên khoa: ").strip().lower()
            results = [l for l in lecturers if search_term in l.get('department', '').lower()]
        elif choice == '4':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Hiển thị kết quả
        print(f"\nTìm thấy {len(results)} giảng viên:")
        if results:
            print("\n" + "-"*80)
            print(f"{'STT':<5} {'Mã GV':<10} {'Họ và tên':<25} {'Khoa':<15} {'Chuyên ngành':<20}")
            print("-"*80)

            for i, lecturer in enumerate(results, 1):
                employee_id = lecturer.get('employee_id', 'N/A')
                fullname = f"{lecturer.get('firstname', '')} {lecturer.get('lastname', '')}"
                department = lecturer.get('department', 'N/A')
                specialization = lecturer.get('specialization', 'N/A')

                print(f"{i:<5} {employee_id:<10} {fullname:<25} {department:<15} {specialization:<20}")

        input("\n\nNhấn Enter để tiếp tục...")

    def assign_course_to_lecturer(self):
        """Phân công môn học cho giảng viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     PHÂN CÔNG MÔN HỌC CHO GIẢNG VIÊN")
        print("="*50)

        # Lấy danh sách giảng viên
        lecturers = self.read_file(self.data_files['teacher'])
        if not lecturers:
            print("\nChưa có giảng viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Lấy danh sách môn học
        courses = self.read_file(self.data_files['courses'])
        if not courses:
            print("\nChưa có môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nChọn giảng viên:")
        for i, lecturer in enumerate(lecturers, 1):
            employee_id = lecturer.get('employee_id', 'N/A')
            fullname = f"{lecturer.get('firstname')} {lecturer.get('lastname')}"
            assigned_courses = len(lecturer.get('assigned_courses', []))
            print(f"{i}. {fullname} ({employee_id}) - {assigned_courses} môn")

        try:
            lecturer_idx = int(input("\nChọn giảng viên (số): ").strip()) - 1
            if lecturer_idx < 0 or lecturer_idx >= len(lecturers):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            selected_lecturer = lecturers[lecturer_idx]
            lecturer_id = selected_lecturer.get('username')

            print(f"\nChọn môn học cho giảng viên {selected_lecturer.get('firstname')} {selected_lecturer.get('lastname')}:")
            print("-"*60)

            available_courses = [c for c in courses if c.get('lecturer_id') == '' or c.get('lecturer_id') == lecturer_id]

            if not available_courses:
                print("\nKhông có môn học nào có thể phân công!")
                input("\nNhấn Enter để tiếp tục...")
                return

            for i, course in enumerate(available_courses, 1):
                current_lecturer = course.get('lecturer_id', 'Chưa phân công')
                if current_lecturer == lecturer_id:
                    status = "✓ Đã phân công"
                else:
                    status = "Chưa phân công"
                print(f"{i}. {course.get('course_code')} - {course.get('course_name')} ({status})")

            course_idx = int(input("\nChọn môn học (số): ").strip()) - 1
            if course_idx < 0 or course_idx >= len(available_courses):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            selected_course = available_courses[course_idx]
            course_id = selected_course.get('course_id')

            # Cập nhật môn học
            for course in courses:
                if course.get('course_id') == course_id:
                    course['lecturer_id'] = lecturer_id
                    break

            # Cập nhật giảng viên
            for lecturer in lecturers:
                if lecturer.get('username') == lecturer_id:
                    assigned = lecturer.get('assigned_courses', [])
                    if course_id not in assigned:
                        assigned.append(course_id)
                    lecturer['assigned_courses'] = assigned
                    break

            # Lưu dữ liệu
            if (self.save_to_file(self.data_files['courses'], courses, 'w') and
                self.save_to_file(self.data_files['teacher'], lecturers, 'w')):
                print(f"\n✓ Đã phân công môn học '{selected_course.get('course_name')}' cho giảng viên thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    # ========== QUẢN LÝ MÔN HỌC ==========

    def manage_courses(self):
        """Quản lý môn học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     QUẢN LÝ MÔN HỌC")
        print("="*50)

        print("\n1. Thêm môn học mới")
        print("2. Xem danh sách môn học")
        print("3. Chỉnh sửa môn học")
        print("4. Phân công giảng viên")
        print("5. Quay lại")

        choice = input("\nChọn chức năng (1-5): ").strip()

        if choice == '1':
            self.add_course()
        elif choice == '2':
            self.view_courses()
        elif choice == '3':
            self.edit_course()
        elif choice == '4':
            self.assign_lecturer_to_course()
        elif choice == '5':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def add_course(self):
        """Thêm môn học mới"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THÊM MÔN HỌC MỚI")
        print("="*50)

        print("\nNhập thông tin môn học:")

        course_id = input("Mã môn học: ").strip()

        # Kiểm tra mã môn học đã tồn tại chưa
        courses = self.read_file(self.data_files['courses'])
        for course in courses:
            if course.get('course_id') == course_id:
                print(f"\n✗ Mã môn học '{course_id}' đã tồn tại!")
                input("\nNhấn Enter để tiếp tục...")
                return

        course_code = input("Mã môn (viết tắt): ").strip()
        course_name = input("Tên môn học: ").strip()
        credits = input("Số tín chỉ: ").strip()
        department = input("Khoa quản lý: ").strip()
        semester = input("Học kỳ (Fall/Spring/Summer): ").strip()
        year = input("Năm học: ").strip()
        max_students = input("Số SV tối đa (mặc định 50): ").strip() or "50"
        description = input("Mô tả môn học: ").strip()

        try:
            credits = int(credits)
            year = int(year)
            max_students = int(max_students)
        except ValueError:
            print("\n✗ Giá trị số không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        course_data = {
            'course_id': course_id,
            'course_code': course_code,
            'course_name': course_name,
            'credits': credits,
            'department': department,
            'semester': semester,
            'year': year,
            'lecturer_id': '',
            'max_students': max_students,
            'enrolled_students': [],
            'prerequisites': [],
            'description': description,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        courses.append(course_data)

        if self.save_to_file(self.data_files['courses'], courses, 'w'):
            print(f"\n✓ Đã thêm môn học '{course_name}' thành công!")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

        input("\nNhấn Enter để tiếp tục...")

    def view_courses(self):
        """Xem danh sách môn học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     DANH SÁCH MÔN HỌC")
        print("="*50)

        courses = self.read_file(self.data_files['courses'])

        if not courses:
            print("\nChưa có môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\n" + "-"*120)
        print(f"{'STT':<5} {'Mã môn':<10} {'Tên môn học':<30} {'Số TC':<8} {'Khoa':<15} {'Giảng viên':<20} {'Số SV':<8}")
        print("-"*120)

        all_lecturers = self.read_file(self.data_files['teacher'])

        for i, course in enumerate(courses, 1):
            course_code = course.get('course_code', 'N/A')
            course_name = course.get('course_name', 'N/A')
            credits = course.get('credits', 0)
            department = course.get('department', 'N/A')
            lecturer_id = course.get('lecturer_id', '')
            student_count = len(course.get('enrolled_students', []))

            # Lấy tên giảng viên
            lecturer_name = "Chưa phân công"
            if lecturer_id:
                lecturer = next((l for l in all_lecturers if l.get('username') == lecturer_id), None)
                if lecturer:
                    lecturer_name = f"{lecturer.get('firstname')} {lecturer.get('lastname')}"

            print(f"{i:<5} {course_code:<10} {course_name:<30} {credits:<8} {department:<15} {lecturer_name:<20} {student_count:<8}")

        print(f"\nTổng số môn học: {len(courses)}")

        input("\n\nNhấn Enter để tiếp tục...")

    def edit_course(self):
        """Chỉnh sửa thông tin môn học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHỈNH SỬA MÔN HỌC")
        print("="*50)

        courses = self.read_file(self.data_files['courses'])

        if not courses:
            print("\nChưa có môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nDanh sách môn học:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course.get('course_code')} - {course.get('course_name')}")

        try:
            choice = int(input("\nChọn môn học cần sửa (số): ").strip()) - 1
            if choice < 0 or choice >= len(courses):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            course = courses[choice]
            print(f"\nThông tin hiện tại của môn học:")
            print(f"1. Mã môn học: {course.get('course_id')}")
            print(f"2. Mã môn (viết tắt): {course.get('course_code')}")
            print(f"3. Tên môn học: {course.get('course_name')}")
            print(f"4. Số tín chỉ: {course.get('credits')}")
            print(f"5. Khoa quản lý: {course.get('department')}")
            print(f"6. Học kỳ: {course.get('semester')}")
            print(f"7. Năm học: {course.get('year')}")
            print(f"8. Số SV tối đa: {course.get('max_students')}")
            print(f"9. Mô tả: {course.get('description')}")

            field = input("\nChọn trường cần sửa (1-9, 0 để hủy): ").strip()

            if field == '0':
                return

            if field == '1':
                new_value = input("Nhập mã môn học mới: ").strip()
                course['course_id'] = new_value
            elif field == '2':
                new_value = input("Nhập mã môn (viết tắt) mới: ").strip()
                course['course_code'] = new_value
            elif field == '3':
                new_value = input("Nhập tên môn học mới: ").strip()
                course['course_name'] = new_value
            elif field == '4':
                new_value = input("Nhập số tín chỉ mới: ").strip()
                course['credits'] = int(new_value)
            elif field == '5':
                new_value = input("Nhập khoa quản lý mới: ").strip()
                course['department'] = new_value
            elif field == '6':
                new_value = input("Nhập học kỳ mới: ").strip()
                course['semester'] = new_value
            elif field == '7':
                new_value = input("Nhập năm học mới: ").strip()
                course['year'] = int(new_value)
            elif field == '8':
                new_value = input("Nhập số SV tối đa mới: ").strip()
                course['max_students'] = int(new_value)
            elif field == '9':
                new_value = input("Nhập mô tả mới: ").strip()
                course['description'] = new_value
            else:
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            # Lưu dữ liệu
            if self.save_to_file(self.data_files['courses'], courses, 'w'):
                print("\n✓ Đã cập nhật thông tin môn học thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    def assign_lecturer_to_course(self):
        """Phân công giảng viên cho môn học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     PHÂN CÔNG GIẢNG VIÊN CHO MÔN HỌC")
        print("="*50)

        courses = self.read_file(self.data_files['courses'])
        lecturers = self.read_file(self.data_files['teacher'])

        if not courses:
            print("\nChưa có môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        if not lecturers:
            print("\nChưa có giảng viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nDanh sách môn học chưa có giảng viên:")
        available_courses = []

        for i, course in enumerate(courses):
            if not course.get('lecturer_id'):
                available_courses.append((i, course))
                print(f"{len(available_courses)}. {course.get('course_code')} - {course.get('course_name')}")

        if not available_courses:
            print("\nTất cả môn học đã có giảng viên!")
            input("\nNhấn Enter để tiếp tục...")
            return

        try:
            course_choice = int(input("\nChọn môn học (số): ").strip()) - 1
            if course_choice < 0 or course_choice >= len(available_courses):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            original_index, selected_course = available_courses[course_choice]

            print(f"\nChọn giảng viên cho môn: {selected_course.get('course_name')}")
            print("\nDanh sách giảng viên:")

            for i, lecturer in enumerate(lecturers, 1):
                assigned_count = len(lecturer.get('assigned_courses', []))
                print(f"{i}. {lecturer.get('employee_id')} - {lecturer.get('firstname')} {lecturer.get('lastname')} ({assigned_count} môn)")

            lecturer_choice = int(input("\nChọn giảng viên (số): ").strip()) - 1
            if lecturer_choice < 0 or lecturer_choice >= len(lecturers):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            selected_lecturer = lecturers[lecturer_choice]

            # Cập nhật môn học
            courses[original_index]['lecturer_id'] = selected_lecturer.get('username')

            # Cập nhật giảng viên
            if 'assigned_courses' not in selected_lecturer:
                selected_lecturer['assigned_courses'] = []

            if selected_course.get('course_id') not in selected_lecturer['assigned_courses']:
                selected_lecturer['assigned_courses'].append(selected_course.get('course_id'))

            # Lưu dữ liệu
            if (self.save_to_file(self.data_files['courses'], courses, 'w') and
                self.save_to_file(self.data_files['teacher'], lecturers, 'w')):
                print(f"\n✓ Đã phân công giảng viên thành công!")
                print(f"  Môn: {selected_course.get('course_name')}")
                print(f"  Giảng viên: {selected_lecturer.get('firstname')} {selected_lecturer.get('lastname')}")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    # ========== XEM MÔN HỌC (SINH VIÊN) ==========

    def view_student_courses_detail(self):
        """Sinh viên xem chi tiết môn học đã đăng ký"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     MÔN HỌC CỦA TÔI")
        print("="*50)

        student_id = self.current_user.get('username', '')

        # Lấy môn học sinh viên đã đăng ký
        all_courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in all_courses if student_id in c.get('enrolled_students', [])]

        if not my_courses:
            print("\nBạn chưa đăng ký môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nDanh sách môn học của {self.current_user.get('firstname')} {self.current_user.get('lastname')}:")
        print("-"*100)
        print(f"{'STT':<5} {'Mã môn':<10} {'Tên môn học':<30} {'Số TC':<8} {'Giảng viên':<25} {'Trạng thái':<15}")
        print("-"*100)

        for i, course in enumerate(my_courses, 1):
            course_code = course.get('course_code', 'N/A')
            course_name = course.get('course_name', 'N/A')
            credits = course.get('credits', 0)
            lecturer_id = course.get('lecturer_id', '')

            # Lấy tên giảng viên
            lecturer_name = "Chưa phân công"
            if lecturer_id:
                all_lecturers = self.read_file(self.data_files['teacher'])
                lecturer = next((l for l in all_lecturers if l.get('username') == lecturer_id), None)
                if lecturer:
                    lecturer_name = f"{lecturer.get('firstname')} {lecturer.get('lastname')}"

            # Kiểm tra trạng thái môn học
            enrolled_count = len(course.get('enrolled_students', []))
            max_students = course.get('max_students', 50)
            status = "Đang học" if enrolled_count <= max_students else "Quá tải"

            print(f"{i:<5} {course_code:<10} {course_name:<30} {credits:<8} {lecturer_name:<25} {status:<15}")

        print(f"\nTổng số môn: {len(my_courses)}")
        print(f"Tổng số tín chỉ: {sum(c.get('credits', 0) for c in my_courses)}")

        # Xem chi tiết môn học
        try:
            choice = input("\nNhập STT môn học để xem chi tiết (0 để quay lại): ").strip()
            if choice == '0':
                return

            idx = int(choice) - 1
            if 0 <= idx < len(my_courses):
                self.view_course_detail(my_courses[idx])
        except ValueError:
            pass

        input("\nNhấn Enter để tiếp tục...")

    def view_course_detail(self, course):
        """Xem chi tiết môn học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHI TIẾT MÔN HỌC")
        print("="*50)

        print(f"\n📚 THÔNG TIN MÔN HỌC:")
        print(f"  Mã môn: {course.get('course_code', 'N/A')}")
        print(f"  Tên môn: {course.get('course_name', 'N/A')}")
        print(f"  Số tín chỉ: {course.get('credits', 0)}")
        print(f"  Khoa: {course.get('department', 'N/A')}")
        print(f"  Học kỳ: {course.get('semester', 'N/A')}")
        print(f"  Năm học: {course.get('year', 'N/A')}")
        print(f"  Số SV tối đa: {course.get('max_students', 50)}")
        print(f"  Số SV đã đăng ký: {len(course.get('enrolled_students', []))}")

        # Thông tin giảng viên
        lecturer_id = course.get('lecturer_id', '')
        if lecturer_id:
            all_lecturers = self.read_file(self.data_files['teacher'])
            lecturer = next((l for l in all_lecturers if l.get('username') == lecturer_id), None)
            if lecturer:
                print(f"\n👨‍🏫 THÔNG TIN GIẢNG VIÊN:")
                print(f"  Tên: {lecturer.get('firstname')} {lecturer.get('lastname')}")
                print(f"  Khoa: {lecturer.get('department', 'N/A')}")
                print(f"  Chuyên ngành: {lecturer.get('specialization', 'N/A')}")
                print(f"  Email: {lecturer.get('email', 'N/A')}")

        # Mô tả môn học
        description = course.get('description', '')
        if description:
            print(f"\n📝 MÔ TẢ MÔN HỌC:")
            print(f"  {description}")

        input("\n\nNhấn Enter để tiếp tục...")
    # ========== QUẢN LÍ BÀI TẬP BÀI TẬP (SINH VIÊN) ==========
    def view_student_assignments(self):
        """Quản lý bài tập cho sinh viên"""
        while True:
            self.clear_screen()
            print("\n" + "=" * 50)
            print("        QUẢN LÝ BÀI TẬP SINH VIÊN")
            print("=" * 50)

            student_id = self.current_user.get('username')

            assignments = self.read_file(self.data_files['assignments'])
            courses = self.read_file(self.data_files['courses'])

            # Lấy các môn sinh viên đang học
            my_courses = [
                c.get('course_id') for c in courses
                if student_id in c.get('enrolled_students', [])
            ]

            # Lọc bài tập theo môn học
            my_assignments = [
                a for a in assignments
                if a.get('course_id') in my_courses
            ]

            if not my_assignments:
                print("\n📭 Bạn chưa có bài tập nào.")
                input("\nNhấn Enter để quay lại...")
                return

            print(f"\n📚 Tổng số bài tập: {len(my_assignments)}")
            print("-" * 80)
            print(f"{'STT':<5} {'Môn học':<20} {'Tên bài tập':<25} {'Hạn nộp':<20}")
            print("-" * 80)

            for i, a in enumerate(my_assignments, 1):
                print(f"{i:<5} {a.get('course_name', ''):<20} "
                      f"{a.get('title', ''):<25} {a.get('deadline', ''):<20}")

            print("-" * 80)
            print("\n1. Xem chi tiết bài tập")
            print("2. Nộp bài")
            print("3. Xem trạng thái / điểm")
            print("4. Quay lại")

            choice = input("\nChọn chức năng (1-4): ").strip()

            if choice == '1':
                self.student_view_assignment_detail(my_assignments)
            elif choice == '2':
                self.student_submit_assignment(my_assignments)
            elif choice == '3':
                self.student_view_assignment_status(my_assignments)
            elif choice == '4':
                return
            else:
                print("\nLựa chọn không hợp lệ!")
                input("Nhấn Enter để tiếp tục...")

    def student_view_assignment_detail(self, assignments):
        try:
            idx = int(input("\nNhập STT bài tập: ")) - 1
            if idx < 0 or idx >= len(assignments):
                raise ValueError
        except:
            print("\n✗ STT không hợp lệ!")
            input("Nhấn Enter...")
            return

        a = assignments[idx]
        self.clear_screen()

        print("\n" + "=" * 50)
        print("        CHI TIẾT BÀI TẬP")
        print("=" * 50)
        print(f"\n📘 Môn học: {a.get('course_name')}")
        print(f"📝 Tên bài tập: {a.get('title')}")
        print(f"⏰ Hạn nộp: {a.get('deadline')}")
        print(f"\n📄 Mô tả:\n{a.get('description')}")
        input("\nNhấn Enter để quay lại...")

    def student_submit_assignment(self, assignments):
        student_id = self.current_user.get('username')

        try:
            idx = int(input("\nNhập STT bài tập cần nộp: ")) - 1
            if idx < 0 or idx >= len(assignments):
                raise ValueError
        except:
            print("\n✗ STT không hợp lệ!")
            input("Nhấn Enter...")
            return

        assignment = assignments[idx]

        # Kiểm tra đã nộp chưa
        for sub in assignment.get('submissions', []):
            if sub.get('student_id') == student_id:
                print("\n⚠️ Bạn đã nộp bài này rồi!")
                input("Nhấn Enter...")
                return

        content = input("\nNhập nội dung bài nộp (link/file/mô tả): ").strip()

        submission = {
            'student_id': student_id,
            'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'content': content,
            'score': None,
            'feedback': ''
        }

        assignment.setdefault('submissions', []).append(submission)

        # Lưu lại file
        all_assignments = self.read_file(self.data_files['assignments'])
        for a in all_assignments:
            if a.get('assignment_id') == assignment.get('assignment_id'):
                a['submissions'] = assignment['submissions']
                break

        self.save_to_file(self.data_files['assignments'], all_assignments, 'w')

        print("\n✓ Nộp bài thành công!")
        input("Nhấn Enter để tiếp tục...")

    def student_view_assignment_status(self, assignments):
        student_id = self.current_user.get('username')

        self.clear_screen()
        print("\n" + "=" * 50)
        print("        TRẠNG THÁI BÀI TẬP")
        print("=" * 50)

        found = False

        for a in assignments:
            for sub in a.get('submissions', []):
                if sub.get('student_id') == student_id:
                    found = True
                    print(f"\n📘 {a.get('course_name')} - {a.get('title')}")
                    print(f"⏰ Nộp lúc: {sub.get('submitted_at')}")
                    print(f"⭐ Điểm: {sub.get('score') if sub.get('score') is not None else 'Chưa chấm'}")
                    print(f"💬 Nhận xét: {sub.get('feedback', 'Chưa có')}")

        if not found:
            print("\n📭 Bạn chưa nộp bài nào.")

        input("\nNhấn Enter để quay lại...")

    # ========== XEM THÔNG TIN CÁ NHÂN (SINH VIÊN) ==========

    def view_student_profile(self):
        """Sinh viên xem thông tin cá nhân"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THÔNG TIN CÁ NHÂN")
        print("="*50)

        student = self.current_user

        print(f"\n👤 THÔNG TIN CÁ NHÂN:")
        print(f"  Mã sinh viên: {student.get('std_code', 'N/A')}")
        print(f"  Họ và tên: {student.get('firstname', '')} {student.get('lastname', '')}")
        print(f"  Lớp: {student.get('class_', 'N/A')}")
        print(f"  Giới tính: {student.get('gender', 'N/A')}")
        print(f"  Email: {student.get('email', 'N/A')}")
        print(f"  Số điện thoại: {student.get('phone', 'Chưa cập nhật')}")
        print(f"  CMND/CCCD: {student.get('national_code', 'Chưa cập nhật')}")
        print(f"  Ngày tạo tài khoản: {student.get('created_at', 'N/A')}")

        # Thông tin học tập
        student_id = student.get('username')

        # Môn học đang học
        courses = self.read_file(self.data_files['courses'])
        enrolled_courses = [c for c in courses if student_id in c.get('enrolled_students', [])]

        # Điểm số
        grades = self.read_file(self.data_files['grades'])
        student_grades = [g for g in grades if g.get('student_id') == student_id]

        print(f"\n📚 THÔNG TIN HỌC TẬP:")
        print(f"  Số môn đang học: {len(enrolled_courses)}")
        print(f"  Số môn đã có điểm: {len(student_grades)}")

        if student_grades:
            # Tính GPA
            total_grade_points = 0
            total_credits = 0
            passed_credits = 0

            print(f"\n📊 CHI TIẾT ĐIỂM:")
            print("-"*70)
            print(f"{'Môn học':<25} {'Số TC':<8} {'Điểm':<10} {'Điểm chữ':<10} {'Kết quả':<10}")
            print("-"*70)

            for grade in student_grades:
                course_id = grade.get('course_id')
                course = next((c for c in courses if c.get('course_id') == course_id), None)

                if course:
                    course_name = course.get('course_name', 'N/A')
                    credits = course.get('credits', 3)
                    total_score = grade.get('total', 0)
                    grade_letter = grade.get('grade_letter', 'F')

                    # Chuyển đổi điểm chữ sang điểm số
                    grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
                    grade_points = grade_map.get(grade_letter, 0.0)

                    total_grade_points += grade_points * credits
                    total_credits += credits

                    # Kiểm tra qua môn
                    result = "ĐẠT" if grade_letter != 'F' else "KHÔNG ĐẠT"
                    if result == "ĐẠT":
                        passed_credits += credits

                    print(f"{course_name:<25} {credits:<8} {total_score:<10.1f} {grade_letter:<10} {result:<10}")

            if total_credits > 0:
                gpa = total_grade_points / total_credits
                print("-"*70)
                print(f"\n📈 TỔNG KẾT:")
                print(f"  GPA hiện tại: {gpa:.2f}/4.0")
                print(f"  Tổng số tín chỉ: {total_credits}")
                print(f"  Số tín chỉ đã đạt: {passed_credits}")
                print(f"  Tỉ lệ hoàn thành: {(passed_credits/total_credits*100):.1f}%" if total_credits > 0 else "0%")

        print("\n1. Chỉnh sửa thông tin")
        print("2. Đổi mật khẩu")
        print("3. Quay lại")

        choice = input("\nChọn chức năng (1-3): ").strip()

        if choice == '1':
            self.edit_student_profile()
        elif choice == '2':
            self.change_password()
        elif choice == '3':
            return
        else:
            print("\nLựa chọn không hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    def edit_student_profile(self):
        """Sinh viên chỉnh sửa thông tin cá nhân"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHỈNH SỬA THÔNG TIN CÁ NHÂN")
        print("="*50)

        student_id = self.current_user.get('username')
        all_students = self.read_file(self.data_files['student'])

        # Tìm sinh viên
        student = None
        for s in all_students:
            if s.get('username') == student_id:
                student = s
                break

        if not student:
            print("\nKhông tìm thấy thông tin sinh viên!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nThông tin hiện tại:")
        print(f"1. Họ và tên đệm: {student.get('firstname', '')}")
        print(f"2. Tên: {student.get('lastname', '')}")
        print(f"3. Số điện thoại: {student.get('phone', '')}")
        print(f"4. Email: {student.get('email', '')}")
        print(f"5. Giới tính: {student.get('gender', '')}")

        choice = input("\nChọn thông tin cần sửa (1-5, 0 để hủy): ").strip()

        if choice == '0':
            return

        if choice == '1':
            new_value = input("Nhập họ và tên đệm mới: ").strip()
            if new_value:
                student['firstname'] = new_value
        elif choice == '2':
            new_value = input("Nhập tên mới: ").strip()
            if new_value:
                student['lastname'] = new_value
        elif choice == '3':
            new_value = input("Nhập số điện thoại mới: ").strip()
            if new_value:
                student['phone'] = new_value
        elif choice == '4':
            new_value = input("Nhập email mới: ").strip()
            if new_value:
                student['email'] = new_value
        elif choice == '5':
            new_value = input("Nhập giới tính mới (Nam/Nữ): ").strip()
            if new_value:
                student['gender'] = new_value
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Cập nhật current_user
        for key, value in student.items():
            self.current_user[key] = value

        # Lưu dữ liệu
        if self.save_to_file(self.data_files['student'], all_students, 'w'):
            print("\n✓ Đã cập nhật thông tin thành công!")
        else:
            print("\n✗ Lỗi khi lưu dữ liệu!")

    def change_password(self):
        """Đổi mật khẩu"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     ĐỔI MẬT KHẨU")
        print("="*50)

        current_password = input("\nNhập mật khẩu hiện tại: ").strip()

        if current_password != self.current_user.get('password'):
            print("\n✗ Mật khẩu hiện tại không đúng!")
            input("\nNhấn Enter để tiếp tục...")
            return

        new_password = input("Nhập mật khẩu mới: ").strip()
        confirm_password = input("Nhập lại mật khẩu mới: ").strip()

        if new_password != confirm_password:
            print("\n✗ Mật khẩu mới không khớp!")
            input("\nNhấn Enter để tiếp tục...")
            return

        if len(new_password) < 6:
            print("\n✗ Mật khẩu phải có ít nhất 6 ký tự!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Cập nhật mật khẩu
        user_id = self.current_user.get('username')
        role = self.current_role

        # Xác định file dữ liệu
        if role == 'admin':
            filepath = self.data_files['admin']
        elif role == 'lecturer':
            filepath = self.data_files['teacher']
        else:  # student
            filepath = self.data_files['student']

        # Đọc và cập nhật dữ liệu
        users = self.read_file(filepath)
        updated = False

        for user in users:
            if user.get('username') == user_id:
                user['password'] = new_password
                updated = True
                break

        if updated:
            # Cập nhật current_user
            self.current_user['password'] = new_password

            # Lưu dữ liệu
            if self.save_to_file(filepath, users, 'w'):
                print("\n✓ Đã đổi mật khẩu thành công!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")
        else:
            print("\n✗ Không tìm thấy người dùng!")

        input("\nNhấn Enter để tiếp tục...")

    # ========== DANH SÁCH MÔN HỌC (GIẢNG VIÊN) ==========

    def view_lecturer_courses(self):
        """Giảng viên xem danh sách môn học đang dạy"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     DANH SÁCH MÔN HỌC CỦA TÔI")
        print("="*50)

        lecturer_id = self.current_user.get('username', '')
        lecturer_name = f"{self.current_user.get('firstname')} {self.current_user.get('lastname')}"

        # Lấy môn học của giảng viên
        all_courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in all_courses if c.get('lecturer_id') == lecturer_id]

        if not my_courses:
            print(f"\nGiảng viên {lecturer_name} chưa được phân công môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nDanh sách môn học của giảng viên {lecturer_name}:")
        print("-"*100)
        print(f"{'STT':<5} {'Mã môn':<10} {'Tên môn học':<30} {'Số TC':<8} {'Số SV':<8} {'Học kỳ':<10} {'Năm học':<10}")
        print("-"*100)

        total_students = 0
        total_credits = 0

        for i, course in enumerate(my_courses, 1):
            course_code = course.get('course_code', 'N/A')
            course_name = course.get('course_name', 'N/A')
            credits = course.get('credits', 0)
            student_count = len(course.get('enrolled_students', []))
            semester = course.get('semester', 'N/A')
            year = course.get('year', 'N/A')

            total_students += student_count
            total_credits += credits

            print(f"{i:<5} {course_code:<10} {course_name:<30} {credits:<8} {student_count:<8} {semester:<10} {year:<10}")

        print("-"*100)
        print(f"\n📊 TỔNG KẾT:")
        print(f"  Tổng số môn: {len(my_courses)}")
        print(f"  Tổng số tín chỉ: {total_credits}")
        print(f"  Tổng số sinh viên: {total_students}")
        print(f"  Số SV trung bình/môn: {total_students/len(my_courses):.1f}" if my_courses else "0")

        # Xem chi tiết môn học
        try:
            choice = input("\nNhập STT môn học để xem chi tiết (0 để quay lại): ").strip()
            if choice == '0':
                return

            idx = int(choice) - 1
            if 0 <= idx < len(my_courses):
                self.view_lecturer_course_detail(my_courses[idx])
        except ValueError:
            pass

        input("\nNhấn Enter để tiếp tục...")

    def view_lecturer_course_detail(self, course):
        """Giảng viên xem chi tiết môn học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHI TIẾT MÔN HỌC")
        print("="*50)

        print(f"\n📚 THÔNG TIN MÔN HỌC:")
        print(f"  Mã môn: {course.get('course_code', 'N/A')}")
        print(f"  Tên môn: {course.get('course_name', 'N/A')}")
        print(f"  Số tín chỉ: {course.get('credits', 0)}")
        print(f"  Khoa: {course.get('department', 'N/A')}")
        print(f"  Học kỳ: {course.get('semester', 'N/A')}")
        print(f"  Năm học: {course.get('year', 'N/A')}")
        print(f"  Số SV tối đa: {course.get('max_students', 50)}")
        print(f"  Số SV đã đăng ký: {len(course.get('enrolled_students', []))}")

        # Thông tin sinh viên
        enrolled_students = course.get('enrolled_students', [])
        if enrolled_students:
            print(f"\n👥 DANH SÁCH SINH VIÊN ({len(enrolled_students)} SV):")
            print("-"*60)
            print(f"{'STT':<5} {'Mã SV':<10} {'Họ và tên':<25} {'Lớp':<10}")
            print("-"*60)

            all_students = self.read_file(self.data_files['student'])

            for i, student_id in enumerate(enrolled_students, 1):
                student = next((s for s in all_students if s.get('username') == student_id), None)
                if student:
                    std_code = student.get('std_code', 'N/A')
                    fullname = f"{student.get('firstname', '')} {student.get('lastname', '')}"
                    class_ = student.get('class_', 'N/A')
                    print(f"{i:<5} {std_code:<10} {fullname:<25} {class_:<10}")

        # Thông tin bài tập
        all_assignments = self.read_file(self.data_files['assignments'])
        course_assignments = [a for a in all_assignments if a.get('course_id') == course.get('course_id')]

        if course_assignments:
            print(f"\n📝 BÀI TẬP ({len(course_assignments)} bài):")
            print("-"*70)
            print(f"{'STT':<5} {'Tên bài tập':<30} {'Hạn nộp':<15} {'Đã nộp':<10} {'Chưa nộp':<10}")
            print("-"*70)

            for i, assignment in enumerate(course_assignments, 1):
                assignment_name = assignment.get('assignment_name', 'N/A')
                deadline = assignment.get('deadline', 'N/A')
                submissions = assignment.get('submissions', [])
                submitted_count = len(submissions)
                not_submitted_count = len(enrolled_students) - submitted_count

                print(f"{i:<5} {assignment_name:<30} {deadline:<15} {submitted_count:<10} {not_submitted_count:<10}")

        input("\n\nNhấn Enter để tiếp tục...")

    # ========== DANH SÁCH SINH VIÊN (GIẢNG VIÊN) ==========

    def view_lecturer_students(self):
        """Giảng viên xem danh sách sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     DANH SÁCH SINH VIÊN CỦA TÔI")
        print("="*50)

        lecturer_id = self.current_user.get('username', '')
        lecturer_name = f"{self.current_user.get('firstname')} {self.current_user.get('lastname')}"

        # Lấy môn học của giảng viên
        all_courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in all_courses if c.get('lecturer_id') == lecturer_id]

        if not my_courses:
            print(f"\nGiảng viên {lecturer_name} chưa được phân công môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Lấy tất cả sinh viên của giảng viên
        all_students = self.read_file(self.data_files['student'])
        my_students_dict = {}

        for course in my_courses:
            enrolled_students = course.get('enrolled_students', [])
            for student_id in enrolled_students:
                if student_id not in my_students_dict:
                    student = next((s for s in all_students if s.get('username') == student_id), None)
                    if student:
                        my_students_dict[student_id] = {
                            'student': student,
                            'courses': []
                        }
                my_students_dict[student_id]['courses'].append(course.get('course_name'))

        if not my_students_dict:
            print(f"\nChưa có sinh viên nào đăng ký các môn của giảng viên {lecturer_name}!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nDanh sách sinh viên của giảng viên {lecturer_name}:")
        print("-"*100)
        print(f"{'STT':<5} {'Mã SV':<10} {'Họ và tên':<25} {'Lớp':<10} {'Số môn':<8} {'Các môn học':<40}")
        print("-"*100)

        my_students_list = list(my_students_dict.values())
        my_students_list.sort(key=lambda x: x['student'].get('std_code', ''))

        for i, item in enumerate(my_students_list, 1):
            student = item['student']
            courses = item['courses']

            std_code = student.get('std_code', 'N/A')
            fullname = f"{student.get('firstname', '')} {student.get('lastname', '')}"
            class_ = student.get('class_', 'N/A')
            course_count = len(courses)
            course_names = ", ".join(courses[:2])  # Hiển thị tối đa 2 môn
            if len(courses) > 2:
                course_names += f"... (+{len(courses)-2})"

            print(f"{i:<5} {std_code:<10} {fullname:<25} {class_:<10} {course_count:<8} {course_names:<40}")

        print(f"\nTổng số sinh viên: {len(my_students_list)}")
        print(f"Tổng số môn học: {len(my_courses)}")

        # Xem chi tiết sinh viên
        try:
            choice = input("\nNhập STT sinh viên để xem chi tiết (0 để quay lại): ").strip()
            if choice == '0':
                return

            idx = int(choice) - 1
            if 0 <= idx < len(my_students_list):
                self.view_lecturer_student_detail(my_students_list[idx])
        except ValueError:
            pass

        input("\nNhấn Enter để tiếp tục...")

    def view_lecturer_student_detail(self, student_item):
        """Giảng viên xem chi tiết sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     CHI TIẾT SINH VIÊN")
        print("="*50)

        student = student_item['student']
        courses = student_item['courses']

        print(f"\n👤 THÔNG TIN SINH VIÊN:")
        print(f"  Mã sinh viên: {student.get('std_code', 'N/A')}")
        print(f"  Họ và tên: {student.get('firstname', '')} {student.get('lastname', '')}")
        print(f"  Lớp: {student.get('class_', 'N/A')}")
        print(f"  Giới tính: {student.get('gender', 'N/A')}")
        print(f"  Email: {student.get('email', 'N/A')}")
        print(f"  Số điện thoại: {student.get('phone', 'Chưa cập nhật')}")

        print(f"\n📚 MÔN HỌC ĐANG HỌC VỚI TÔI ({len(courses)} môn):")
        for i, course_name in enumerate(courses, 1):
            print(f"  {i}. {course_name}")

        # Xem điểm của sinh viên trong các môn của giảng viên
        student_id = student.get('username')
        lecturer_id = self.current_user.get('username', '')

        all_grades = self.read_file(self.data_files['grades'])
        student_grades = [g for g in all_grades
                         if g.get('student_id') == student_id
                         and g.get('lecturer_id') == lecturer_id]

        if student_grades:
            print(f"\n📊 ĐIỂM CỦA SINH VIÊN:")
            print("-"*70)
            print(f"{'Môn học':<25} {'Chuyên cần':<12} {'Giữa kỳ':<10} {'Cuối kỳ':<10} {'Tổng':<10} {'Điểm chữ':<10}")
            print("-"*70)

            all_courses = self.read_file(self.data_files['courses'])

            for grade in student_grades:
                course_id = grade.get('course_id')
                course = next((c for c in all_courses if c.get('course_id') == course_id), None)

                if course:
                    course_name = course.get('course_name', 'N/A')
                    attendance = grade.get('attendance', 0)
                    midterm = grade.get('midterm', 0)
                    final = grade.get('final', 0)
                    total = grade.get('total', 0)
                    grade_letter = grade.get('grade_letter', 'N/A')

                    print(f"{course_name:<25} {attendance:<12.1f} {midterm:<10.1f} {final:<10.1f} {total:<10.1f} {grade_letter:<10}")

        input("\n\nNhấn Enter để tiếp tục...")

    # ========== XEM LỊCH DẠY (GIẢNG VIÊN) ==========

    def view_lecturer_schedule(self):
        """Giảng viên xem lịch dạy"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     LỊCH DẠY CỦA TÔI")
        print("="*50)

        lecturer_id = self.current_user.get('username', '')
        lecturer_name = f"{self.current_user.get('firstname')} {self.current_user.get('lastname')}"

        # Lấy môn học của giảng viên
        all_courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in all_courses if c.get('lecturer_id') == lecturer_id]

        if not my_courses:
            print(f"\nGiảng viên {lecturer_name} chưa được phân công môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Lấy lịch dạy từ file schedules hoặc từ thông tin môn học
        all_schedules = self.read_file(self.data_files['schedules'])

        # Tạo dict lịch dạy
        schedule_dict = {}

        for course in my_courses:
            course_id = course.get('course_id')
            course_name = course.get('course_name', 'N/A')
            course_code = course.get('course_code', 'N/A')

            # Tìm lịch trong file schedules
            course_schedules = [s for s in all_schedules if s.get('course_id') == course_id]

            if course_schedules:
                for schedule in course_schedules:
                    day = schedule.get('day', 'N/A')
                    time = schedule.get('time', 'N/A')
                    classroom = schedule.get('classroom', 'N/A')

                    if day not in schedule_dict:
                        schedule_dict[day] = []

                    schedule_dict[day].append({
                        'time': time,
                        'course': f"{course_code} - {course_name}",
                        'classroom': classroom
                    })
            else:
                # Nếu không có lịch trong file, sử dụng thông tin từ course
                schedule = course.get('schedule', 'Chưa có lịch')
                classroom = course.get('classroom', 'Chưa xếp')

                if schedule != 'Chưa có lịch':
                    # Giả sử schedule có dạng "Thứ X, Tiết Y-Z"
                    if 'Thứ' in schedule:
                        day = schedule.split(',')[0].strip()
                        time = schedule.split(',')[1].strip() if ',' in schedule else 'N/A'

                        if day not in schedule_dict:
                            schedule_dict[day] = []

                        schedule_dict[day].append({
                            'time': time,
                            'course': f"{course_code} - {course_name}",
                            'classroom': classroom
                        })

        if not schedule_dict:
            print(f"\nChưa có lịch dạy cho giảng viên {lecturer_name}!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\n📅 LỊCH DẠY CỦA GIẢNG VIÊN {lecturer_name}:")

        # Sắp xếp các ngày trong tuần
        day_order = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']

        for day in day_order:
            if day in schedule_dict:
                print(f"\n{day.upper()}:")
                print("-"*80)
                print(f"{'Thời gian':<15} {'Môn học':<40} {'Phòng':<15}")
                print("-"*80)

                # Sắp xếp theo thời gian
                schedule_dict[day].sort(key=lambda x: x['time'])

                for item in schedule_dict[day]:
                    print(f"{item['time']:<15} {item['course']:<40} {item['classroom']:<15}")

        # Hiển thị thống kê
        total_classes = sum(len(schedules) for schedules in schedule_dict.values())
        print(f"\n📊 THỐNG KÊ LỊCH DẠY:")
        print(f"  Tổng số tiết dạy/tuần: {total_classes}")
        print(f"  Số ngày có lịch/tuần: {len(schedule_dict)}")
        print(f"  Số môn học: {len(my_courses)}")

        # Hiển thị các môn chưa có lịch
        courses_without_schedule = []
        for course in my_courses:
            course_id = course.get('course_id')
            course_schedules = [s for s in all_schedules if s.get('course_id') == course_id]
            if not course_schedules and course.get('schedule') == 'Chưa có lịch':
                courses_without_schedule.append(course.get('course_name'))

        if courses_without_schedule:
            print(f"\n⚠️  CÁC MÔN CHƯA CÓ LỊCH:")
            for course_name in courses_without_schedule:
                print(f"  • {course_name}")

        input("\n\nNhấn Enter để tiếp tục...")

    # ========== QUẢN LÝ ĐIỂM ==========

    def manage_grades(self):
        """Quản lý điểm (Giảng viên)"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     QUẢN LÝ ĐIỂM")
        print("="*50)

        lecturer_id = self.current_user.get('username', '')

        # Lấy môn học của giảng viên
        courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in courses if c.get('lecturer_id') == lecturer_id]

        if not my_courses:
            print("\nBạn chưa được phân công giảng dạy môn nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nDanh sách môn học của bạn:")
        for i, course in enumerate(my_courses, 1):
            enrolled = len(course.get('enrolled_students', []))
            print(f"{i}. {course.get('course_code')} - {course.get('course_name')} ({enrolled} SV)")

        try:
            choice = int(input("\nChọn môn học (số): ").strip()) - 1
            if choice < 0 or choice >= len(my_courses):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            selected_course = my_courses[choice]
            course_id = selected_course.get('course_id')

            # Lấy danh sách sinh viên
            enrolled_students = selected_course.get('enrolled_students', [])

            if not enrolled_students:
                print("\nChưa có sinh viên đăng ký môn học này!")
                input("\nNhấn Enter để tiếp tục...")
                return

            all_students = self.read_file(self.data_files['student'])
            course_students = [s for s in all_students if s.get('username') in enrolled_students]

            # Lấy điểm hiện tại
            all_grades = self.read_file(self.data_files['grades'])
            course_grades = {g.get('student_id'): g for g in all_grades
                           if g.get('course_id') == course_id}

            print(f"\nNhập điểm cho môn: {selected_course.get('course_name')}")
            print("-"*80)

            for student in course_students:
                student_id = student.get('username')
                fullname = f"{student.get('firstname')} {student.get('lastname')}"
                std_code = student.get('std_code', 'N/A')

                grade_record = course_grades.get(student_id, {})
                current_total = grade_record.get('total', 0)

                print(f"\nSinh viên: {fullname} ({std_code})")
                print(f"Điểm hiện tại: {current_total:.1f}")

                # Nhập điểm thành phần
                try:
                    attendance = float(input("  Điểm chuyên cần (0-10): ") or grade_record.get('attendance', 0))
                    midterm = float(input("  Điểm giữa kỳ (0-100): ") or grade_record.get('midterm', 0))
                    final = float(input("  Điểm cuối kỳ (0-100): ") or grade_record.get('final', 0))

                    # Tính điểm tổng (có thể thay đổi công thức)
                    total = attendance + (midterm * 0.3) + (final * 0.6)

                    # Xác định điểm chữ
                    if total >= 90:
                        grade_letter = "A"
                    elif total >= 80:
                        grade_letter = "B"
                    elif total >= 70:
                        grade_letter = "C"
                    elif total >= 60:
                        grade_letter = "D"
                    else:
                        grade_letter = "F"

                    # Tạo/Tạo lại bản ghi điểm
                    new_grade = {
                        'grade_id': grade_record.get('grade_id', f'GR{datetime.now().strftime("%Y%m%d%H%M%S")}'),
                        'student_id': student_id,
                        'course_id': course_id,
                        'semester': selected_course.get('semester', 'Spring'),
                        'year': selected_course.get('year', 2024),
                        'lecturer_id': lecturer_id,
                        'attendance': attendance,
                        'midterm': midterm,
                        'final': final,
                        'total': total,
                        'grade_letter': grade_letter,
                        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }

                    # Xóa bản ghi cũ nếu có
                    all_grades = [g for g in all_grades
                                if not (g.get('student_id') == student_id and g.get('course_id') == course_id)]

                    # Thêm bản ghi mới
                    all_grades.append(new_grade)

                except ValueError:
                    print("  ✗ Giá trị không hợp lệ! Bỏ qua sinh viên này.")
                    continue

            # Lưu tất cả điểm
            if self.save_to_file(self.data_files['grades'], all_grades, 'w'):
                print(f"\n✓ Đã lưu điểm cho {len(course_students)} sinh viên!")
            else:
                print("\n✗ Lỗi khi lưu điểm!")

        except ValueError:
            print("\nVui lòng nhập số!")
        except Exception as e:
            print(f"\nLỗi: {e}")

        input("\nNhấn Enter để tiếp tục...")

    # ========== TẠO BÀI TẬP (GIẢNG VIÊN) ==========

    def create_assignment(self):
        """Giảng viên tạo bài tập mới"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     TẠO BÀI TẬP MỚI")
        print("="*50)

        lecturer_id = self.current_user.get('username', '')

        # Lấy môn học của giảng viên
        courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in courses if c.get('lecturer_id') == lecturer_id]

        if not my_courses:
            print("\nBạn chưa được phân công giảng dạy môn nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nChọn môn học để tạo bài tập:")
        for i, course in enumerate(my_courses, 1):
            print(f"{i}. {course.get('course_code')} - {course.get('course_name')}")

        try:
            course_choice = int(input("\nChọn môn học (số): ").strip()) - 1
            if course_choice < 0 or course_choice >= len(my_courses):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            selected_course = my_courses[course_choice]
            course_id = selected_course.get('course_id')

            print(f"\nTạo bài tập cho môn: {selected_course.get('course_name')}")
            print("-"*50)

            assignment_name = input("\nTên bài tập: ").strip()
            if not assignment_name:
                print("\n✗ Tên bài tập không được để trống!")
                input("\nNhấn Enter để tiếp tục...")
                return

            description = input("Mô tả bài tập: ").strip()

            # Nhập deadline
            while True:
                deadline = input("Hạn nộp (YYYY-MM-DD): ").strip()
                try:
                    datetime.strptime(deadline, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Định dạng ngày không hợp lệ! Vui lòng nhập đúng định dạng YYYY-MM-DD")

            try:
                max_score = float(input("Điểm tối đa (default: 100): ").strip() or "100")
            except ValueError:
                print("\n✗ Điểm phải là số!")
                input("\nNhấn Enter để tiếp tục...")
                return

            assignment_type = input("Loại bài tập (Bài tập/Báo cáo/Đồ án/Khác): ").strip() or "Bài tập"

            # Tạo ID cho bài tập
            assignment_id = f"ASS{datetime.now().strftime('%Y%m%d%H%M%S')}"

            assignment_data = {
                'assignment_id': assignment_id,
                'course_id': course_id,
                'assignment_name': assignment_name,
                'description': description,
                'deadline': deadline,
                'max_score': max_score,
                'type': assignment_type,
                'created_by': lecturer_id,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'submissions': []
            }

            # Lưu bài tập
            all_assignments = self.read_file(self.data_files['assignments'])
            all_assignments.append(assignment_data)

            if self.save_to_file(self.data_files['assignments'], all_assignments, 'w'):
                print(f"\n✓ Đã tạo bài tập '{assignment_name}' thành công!")
                print(f"  Mã bài tập: {assignment_id}")
                print(f"  Hạn nộp: {deadline}")
                print(f"  Điểm tối đa: {max_score}")
            else:
                print("\n✗ Lỗi khi lưu bài tập!")

        except ValueError:
            print("\nVui lòng nhập số hợp lệ!")

        input("\nNhấn Enter để tiếp tục...")

    # ========== ĐIỂM DANH ==========

    def take_attendance(self):
        """Điểm danh sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     ĐIỂM DANH SINH VIÊN")
        print("="*50)

        lecturer_id = self.current_user.get('username', '')

        # Lấy môn học của giảng viên
        courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in courses if c.get('lecturer_id') == lecturer_id]

        if not my_courses:
            print("\nBạn chưa được phân công giảng dạy môn nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print("\nChọn môn học:")
        for i, course in enumerate(my_courses, 1):
            print(f"{i}. {course.get('course_code')} - {course.get('course_name')}")

        try:
            choice = int(input("\nChọn môn học (số): ").strip()) - 1
            if choice < 0 or choice >= len(my_courses):
                print("\nLựa chọn không hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            selected_course = my_courses[choice]
            course_id = selected_course.get('course_id')

            # Lấy danh sách sinh viên
            enrolled_students = selected_course.get('enrolled_students', [])

            if not enrolled_students:
                print("\nChưa có sinh viên đăng ký môn học này!")
                input("\nNhấn Enter để tiếp tục...")
                return

            all_students = self.read_file(self.data_files['student'])
            course_students = [s for s in all_students if s.get('username') in enrolled_students]

            print(f"\nĐiểm danh môn: {selected_course.get('course_name')}")
            print("Ngày: " + datetime.now().strftime('%d/%m/%Y'))
            print("\nNhập trạng thái điểm danh:")
            print("  C: Có mặt, V: Vắng, M: Muộn, P: Phép")
            print("-"*60)

            attendance_records = []
            present_count = 0
            absent_count = 0

            for student in course_students:
                student_id = student.get('username')
                fullname = f"{student.get('firstname')} {student.get('lastname')}"
                std_code = student.get('std_code', 'N/A')

                while True:
                    status = input(f"{fullname} ({std_code}): [C/V/M/P] ").strip().upper()
                    if status in ['C', 'V', 'M', 'P']:
                        break
                    print("Vui lòng nhập C, V, M hoặc P!")

                # Chuyển đổi sang mã đầy đủ
                status_map = {'C': 'present', 'V': 'absent', 'M': 'late', 'P': 'excused'}

                attendance_record = {
                    'attendance_id': f'ATT{datetime.now().strftime("%Y%m%d%H%M%S")}',
                    'course_id': course_id,
                    'student_id': student_id,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'time': datetime.now().strftime('%H:%M'),
                    'status': status_map[status],
                    'taken_by': lecturer_id,
                    'taken_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                attendance_records.append(attendance_record)

                if status == 'C':
                    present_count += 1
                elif status == 'V':
                    absent_count += 1

            # Lưu điểm danh
            all_attendance = self.read_file(self.data_files['attendance'])
            all_attendance.extend(attendance_records)

            if self.save_to_file(self.data_files['attendance'], all_attendance, 'w'):
                print(f"\n✓ Điểm danh hoàn tất!")
                print(f"  Có mặt: {present_count}")
                print(f"  Vắng: {absent_count}")
                print(f"  Tỉ lệ có mặt: {(present_count/len(course_students)*100):.1f}%")
            else:
                print("\n✗ Lỗi khi lưu điểm danh!")

        except ValueError:
            print("\nVui lòng nhập số!")
        except Exception as e:
            print(f"\nLỗi: {e}")

        input("\nNhấn Enter để tiếp tục...")

    # ========== XEM ĐIỂM (SINH VIÊN) ==========

    def view_student_grades(self):
        """Sinh viên xem điểm của mình"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     ĐIỂM CỦA TÔI")
        print("="*50)

        student_id = self.current_user.get('username', '')

        # Lấy điểm của sinh viên
        all_grades = self.read_file(self.data_files['grades'])
        my_grades = [g for g in all_grades if g.get('student_id') == student_id]

        if not my_grades:
            print("\nChưa có điểm cho môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        # Lấy thông tin môn học
        all_courses = self.read_file(self.data_files['courses'])

        print(f"\nĐiểm của {self.current_user.get('firstname')} {self.current_user.get('lastname')}:")
        print("-"*100)
        print(f"{'STT':<5} {'Môn học':<25} {'Chuyên cần':<12} {'Giữa kỳ':<10} {'Cuối kỳ':<10} {'Tổng':<10} {'Điểm chữ':<10}")
        print("-"*100)

        total_gpa = 0
        total_credits = 0

        for i, grade in enumerate(my_grades, 1):
            course_id = grade.get('course_id')
            course = next((c for c in all_courses if c.get('course_id') == course_id), None)

            if course:
                course_name = course.get('course_name', 'N/A')
                credits = course.get('credits', 3)
                attendance = grade.get('attendance', 0)
                midterm = grade.get('midterm', 0)
                final = grade.get('final', 0)
                total = grade.get('total', 0)
                grade_letter = grade.get('grade_letter', 'N/A')

                print(f"{i:<5} {course_name:<25} {attendance:<12.1f} {midterm:<10.1f} {final:<10.1f} {total:<10.1f} {grade_letter:<10}")

                # Tính GPA
                grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
                grade_points = grade_map.get(grade_letter, 0.0)

                total_gpa += grade_points * credits
                total_credits += credits

        if total_credits > 0:
            gpa = total_gpa / total_credits
            print(f"\n📊 GPA hiện tại: {gpa:.2f}/4.0")
            print(f"   Tổng số tín chỉ: {total_credits}")

        input("\n\nNhấn Enter để tiếp tục...")

    # ========== ĐĂNG KÝ MÔN HỌC (SINH VIÊN) ==========

    def register_courses(self):
        """Sinh viên đăng ký môn học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     ĐĂNG KÝ MÔN HỌC")
        print("="*50)

        student_id = self.current_user.get('username', '')

        # Lấy môn học sinh viên đã đăng ký
        all_courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in all_courses if student_id in c.get('enrolled_students', [])]

        # Lấy danh sách môn học có thể đăng ký
        available_courses = []

        for course in all_courses:
            # Kiểm tra sinh viên chưa đăng ký môn này
            if student_id not in course.get('enrolled_students', []):
                # Kiểm tra số lượng sinh viên đã đăng ký
                enrolled_count = len(course.get('enrolled_students', []))
                max_students = course.get('max_students', 50)

                if enrolled_count < max_students:
                    available_courses.append(course)

        if not available_courses:
            print("\nHiện không có môn học nào để đăng ký!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nCác môn học có thể đăng ký ({len(available_courses)} môn):")
        print("-"*100)
        print(f"{'STT':<5} {'Mã môn':<10} {'Tên môn học':<30} {'Số TC':<8} {'Giảng viên':<25} {'Đã đăng ký':<12}")
        print("-"*100)

        # Lấy danh sách giảng viên
        all_lecturers = self.read_file(self.data_files['teacher'])

        for i, course in enumerate(available_courses, 1):
            course_code = course.get('course_code', 'N/A')
            course_name = course.get('course_name', 'N/A')
            credits = course.get('credits', 0)
            lecturer_id = course.get('lecturer_id', '')
            enrolled_count = len(course.get('enrolled_students', []))
            max_students = course.get('max_students', 50)

            # Lấy tên giảng viên
            lecturer_name = "Chưa phân công"
            if lecturer_id:
                lecturer = next((l for l in all_lecturers if l.get('username') == lecturer_id), None)
                if lecturer:
                    lecturer_name = f"{lecturer.get('firstname')} {lecturer.get('lastname')}"

            enrollment_status = f"{enrolled_count}/{max_students}"

            print(f"{i:<5} {course_code:<10} {course_name:<30} {credits:<8} {lecturer_name:<25} {enrollment_status:<12}")

        print(f"\nBạn đã đăng ký {len(my_courses)} môn học")

        try:
            choices = input("\nNhập số thứ tự các môn muốn đăng ký (cách nhau bằng dấu phẩy): ").strip()

            if not choices:
                print("\nKhông có môn học nào được chọn!")
                input("\nNhấn Enter để tiếp tục...")
                return

            # Chuyển đổi lựa chọn thành danh sách
            selected_indices = []
            for choice in choices.split(','):
                try:
                    idx = int(choice.strip()) - 1
                    if 0 <= idx < len(available_courses):
                        selected_indices.append(idx)
                except ValueError:
                    pass

            if not selected_indices:
                print("\nKhông có lựa chọn hợp lệ!")
                input("\nNhấn Enter để tiếp tục...")
                return

            # Đăng ký môn học
            enrolled_count = 0

            for idx in selected_indices:
                course = available_courses[idx]
                course_id = course.get('course_id')

                # Tìm course trong all_courses
                for c in all_courses:
                    if c.get('course_id') == course_id:
                        if 'enrolled_students' not in c:
                            c['enrolled_students'] = []

                        if student_id not in c['enrolled_students']:
                            c['enrolled_students'].append(student_id)
                            enrolled_count += 1
                            break

            # Lưu dữ liệu
            if self.save_to_file(self.data_files['courses'], all_courses, 'w'):
                print(f"\n✓ Đã đăng ký thành công {enrolled_count} môn học!")
            else:
                print("\n✗ Lỗi khi lưu dữ liệu!")

        except Exception as e:
            print(f"\nLỗi: {e}")

        input("\nNhấn Enter để tiếp tục...")

    # ========== XEM LỊCH HỌC ==========

    def view_student_schedule(self):
        """Sinh viên xem lịch học"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     LỊCH HỌC CỦA TÔI")
        print("="*50)

        student_id = self.current_user.get('username', '')

        # Lấy môn học sinh viên đã đăng ký
        all_courses = self.read_file(self.data_files['courses'])
        my_courses = [c for c in all_courses if student_id in c.get('enrolled_students', [])]

        if not my_courses:
            print("\nBạn chưa đăng ký môn học nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nLịch học của {self.current_user.get('firstname')} {self.current_user.get('lastname')}:")
        print("-"*80)
        print(f"{'Thứ/Tiết':<15} {'Môn học':<25} {'Phòng':<10} {'Giảng viên':<20}")
        print("-"*80)

        # Giả sử mỗi môn có schedule là "Thứ X, Tiết Y-Z" hoặc tương tự
        for course in my_courses:
            course_name = course.get('course_name', 'N/A')
            schedule = course.get('schedule', 'Chưa có lịch')
            classroom = course.get('classroom', 'Chưa xếp')
            lecturer_id = course.get('lecturer_id', '')

            # Lấy tên giảng viên
            lecturer_name = "Chưa phân công"
            if lecturer_id:
                all_lecturers = self.read_file(self.data_files['teacher'])
                lecturer = next((l for l in all_lecturers if l.get('username') == lecturer_id), None)
                if lecturer:
                    lecturer_name = f"{lecturer.get('firstname')} {lecturer.get('lastname')}"

            print(f"{schedule:<15} {course_name:<25} {classroom:<10} {lecturer_name:<20}")

        print(f"\nTổng số môn: {len(my_courses)}")

        input("\n\nNhấn Enter để tiếp tục...")

    # ========== SAO LƯU DỮ LIỆU ==========

    def backup_data(self):
        """Sao lưu toàn bộ dữ liệu"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     SAO LƯU DỮ LIỆU")
        print("="*50)

        # Tạo thư mục Backups nếu chưa có
        backup_dir = "Backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_folder)

        print(f"\nĐang sao lưu dữ liệu vào: {backup_folder}")

        try:
            import shutil
            files_copied = 0

            for file_type, filepath in self.data_files.items():
                if os.path.exists(filepath):
                    shutil.copy2(filepath, os.path.join(backup_folder, f"{file_type}.text"))
                    files_copied += 1
                    print(f"  ✓ {file_type}")

            # Tạo file thông tin backup
            backup_info = {
                'backup_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'files_copied': files_copied,
                'backup_by': self.current_user.get('username'),
                'system': 'Student Management System'
            }

            with open(os.path.join(backup_folder, 'backup_info.txt'), 'w', encoding='utf-8') as f:
                f.write(str(backup_info))

            print(f"\n✓ Sao lưu hoàn tất!")
            print(f"  Đã sao lưu {files_copied} file")
            print(f"  Thư mục: {backup_folder}")

        except Exception as e:
            print(f"\n✗ Lỗi khi sao lưu: {e}")

        input("\nNhấn Enter để tiếp tục...")

    # ========== XEM BÁO CÁO ==========

    def view_reports(self):
        """Xem các báo cáo thống kê"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     BÁO CÁO THỐNG KÊ")
        print("="*50)

        print("\n1. Báo cáo tổng quan hệ thống")
        print("2. Báo cáo học tập sinh viên")
        print("3. Báo cáo giảng dạy")
        print("4. Thống kê điểm")
        print("5. Quay lại")

        choice = input("\nChọn loại báo cáo (1-5): ").strip()

        if choice == '1':
            self.system_overview_report()
        elif choice == '2':
            self.student_learning_report()
        elif choice == '3':
            self.teaching_report()
        elif choice == '4':
            self.grade_statistics_report()
        elif choice == '5':
            return
        else:
            print("\nLựa chọn không hợp lệ!")
            input("\nNhấn Enter để tiếp tục...")

    def system_overview_report(self):
        """Báo cáo tổng quan hệ thống"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     BÁO CÁO TỔNG QUAN HỆ THỐNG")
        print("="*50)

        # Đếm số lượng
        admin_count = len(self.read_file(self.data_files['admin']))
        lecturer_count = len(self.read_file(self.data_files['teacher']))
        student_count = len(self.read_file(self.data_files['student']))
        course_count = len(self.read_file(self.data_files['courses']))
        class_count = len(self.read_file(self.data_files['classes']))
        grade_count = len(self.read_file(self.data_files['grades']))
        assignment_count = len(self.read_file(self.data_files['assignments']))

        total_users = admin_count + lecturer_count + student_count

        print(f"\n📊 THỐNG KÊ HỆ THỐNG:")
        print(f"  Tổng người dùng: {total_users}")
        print(f"    • Quản trị viên: {admin_count}")
        print(f"    • Giảng viên: {lecturer_count}")
        print(f"    • Sinh viên: {student_count}")
        print(f"  Số môn học: {course_count}")
        print(f"  Số lớp học: {class_count}")
        print(f"  Số bản ghi điểm: {grade_count}")
        print(f"  Số bài tập: {assignment_count}")

        # Tính tỉ lệ
        if student_count > 0 and lecturer_count > 0:
            student_per_lecturer = student_count / lecturer_count
            print(f"\n📈 TỈ LỆ:")
            print(f"  Số SV/giảng viên: {student_per_lecturer:.1f}")

        if course_count > 0:
            all_courses = self.read_file(self.data_files['courses'])
            avg_students_per_course = sum(len(c.get('enrolled_students', [])) for c in all_courses) / course_count
            print(f"  Số SV trung bình/môn: {avg_students_per_course:.1f}")

        input("\n\nNhấn Enter để tiếp tục...")

    def student_learning_report(self):
        """Báo cáo học tập sinh viên"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     BÁO CÁO HỌC TẬP SINH VIÊN")
        print("="*50)

        # Lấy tất cả sinh viên
        all_students = self.read_file(self.data_files['student'])
        all_courses = self.read_file(self.data_files['courses'])
        all_grades = self.read_file(self.data_files['grades'])

        if not all_students:
            print("\nChưa có sinh viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nTổng số sinh viên: {len(all_students)}")

        # Tính số sinh viên theo lớp
        class_distribution = {}
        for student in all_students:
            class_ = student.get('class_', 'Không xác định')
            if class_ not in class_distribution:
                class_distribution[class_] = 0
            class_distribution[class_] += 1

        print("\n📊 PHÂN BỐ SINH VIÊN THEO LỚP:")
        for class_, count in sorted(class_distribution.items()):
            print(f"  {class_}: {count} SV ({count/len(all_students)*100:.1f}%)")

        # Tính số môn học trung bình mỗi sinh viên
        total_enrolled_courses = 0
        for course in all_courses:
            total_enrolled_courses += len(course.get('enrolled_students', []))

        if all_students:
            avg_courses_per_student = total_enrolled_courses / len(all_students)
            print(f"\n📚 SỐ MÔN HỌC TRUNG BÌNH/SINH VIÊN: {avg_courses_per_student:.1f}")

        # Tính phân loại điểm
        grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for grade in all_grades:
            grade_letter = grade.get('grade_letter', '')
            if grade_letter in grade_distribution:
                grade_distribution[grade_letter] += 1

        total_grades = sum(grade_distribution.values())
        if total_grades > 0:
            print("\n📈 PHÂN PHỐI ĐIỂM:")
            for letter, count in grade_distribution.items():
                percentage = (count / total_grades) * 100
                print(f"  Điểm {letter}: {count} ({percentage:.1f}%)")

        # Tìm sinh viên xuất sắc (GPA cao nhất)
        student_gpas = []
        for student in all_students:
            student_id = student.get('username')
            student_grades = [g for g in all_grades if g.get('student_id') == student_id]

            if student_grades:
                total_grade_points = 0
                total_credits = 0

                for grade in student_grades:
                    course_id = grade.get('course_id')
                    course = next((c for c in all_courses if c.get('course_id') == course_id), None)

                    if course:
                        credits = course.get('credits', 3)
                        grade_letter = grade.get('grade_letter', 'F')

                        grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
                        grade_points = grade_map.get(grade_letter, 0.0)

                        total_grade_points += grade_points * credits
                        total_credits += credits

                if total_credits > 0:
                    gpa = total_grade_points / total_credits
                    student_gpas.append({
                        'student': student,
                        'gpa': gpa,
                        'credits': total_credits
                    })

        if student_gpas:
            # Sắp xếp theo GPA
            student_gpas.sort(key=lambda x: x['gpa'], reverse=True)

            print(f"\n🏆 TOP 5 SINH VIÊN XUẤT SẮC:")
            for i, item in enumerate(student_gpas[:5], 1):
                student = item['student']
                gpa = item['gpa']
                credits = item['credits']

                fullname = f"{student.get('firstname')} {student.get('lastname')}"
                std_code = student.get('std_code', 'N/A')
                class_ = student.get('class_', 'N/A')

                print(f"  {i}. {fullname} ({std_code}) - Lớp {class_}")
                print(f"     GPA: {gpa:.2f}/4.0 | Số TC: {credits}")

        input("\n\nNhấn Enter để tiếp tục...")

    def teaching_report(self):
        """Báo cáo giảng dạy"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     BÁO CÁO GIẢNG DẠY")
        print("="*50)

        # Lấy tất cả giảng viên
        all_lecturers = self.read_file(self.data_files['teacher'])
        all_courses = self.read_file(self.data_files['courses'])

        if not all_lecturers:
            print("\nChưa có giảng viên nào!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nTổng số giảng viên: {len(all_lecturers)}")

        # Tính số môn mỗi giảng viên
        lecturer_stats = []
        for lecturer in all_lecturers:
            lecturer_id = lecturer.get('username')
            teaching_courses = [c for c in all_courses if c.get('lecturer_id') == lecturer_id]

            total_students = 0
            for course in teaching_courses:
                total_students += len(course.get('enrolled_students', []))

            lecturer_stats.append({
                'lecturer': lecturer,
                'course_count': len(teaching_courses),
                'student_count': total_students
            })

        # Sắp xếp theo số môn
        lecturer_stats.sort(key=lambda x: x['course_count'], reverse=True)

        print(f"\n🏆 TOP GIẢNG VIÊN CÓ NHIỀU MÔN NHẤT:")
        for i, stats in enumerate(lecturer_stats[:5], 1):
            lecturer = stats['lecturer']
            course_count = stats['course_count']
            student_count = stats['student_count']

            fullname = f"{lecturer.get('firstname')} {lecturer.get('lastname')}"
            employee_id = lecturer.get('employee_id', 'N/A')
            department = lecturer.get('department', 'N/A')

            print(f"  {i}. {fullname} ({employee_id})")
            print(f"     Khoa: {department} | Số môn: {course_count} | Tổng SV: {student_count}")

        # Tính số giảng viên chưa có môn
        lecturers_without_courses = []
        for stats in lecturer_stats:
            if stats['course_count'] == 0:
                lecturers_without_courses.append(stats['lecturer'])

        if lecturers_without_courses:
            print(f"\n⚠️  GIẢNG VIÊN CHƯA ĐƯỢC PHÂN CÔNG MÔN ({len(lecturers_without_courses)} người):")
            for lecturer in lecturers_without_courses[:5]:
                fullname = f"{lecturer.get('firstname')} {lecturer.get('lastname')}"
                print(f"  • {fullname}")

            if len(lecturers_without_courses) > 5:
                print(f"  ... và {len(lecturers_without_courses) - 5} giảng viên khác")

        # Thống kê theo khoa
        department_stats = {}
        for lecturer in all_lecturers:
            department = lecturer.get('department', 'Không xác định')
            if department not in department_stats:
                department_stats[department] = {
                    'lecturer_count': 0,
                    'course_count': 0,
                    'student_count': 0
                }

            department_stats[department]['lecturer_count'] += 1

            # Đếm số môn của giảng viên trong khoa
            lecturer_id = lecturer.get('username')
            teaching_courses = [c for c in all_courses if c.get('lecturer_id') == lecturer_id]

            department_stats[department]['course_count'] += len(teaching_courses)

            for course in teaching_courses:
                department_stats[department]['student_count'] += len(course.get('enrolled_students', []))

        print(f"\n📊 THỐNG KÊ THEO KHOA:")
        for department, stats in department_stats.items():
            print(f"\n  {department.upper()}:")
            print(f"    Số giảng viên: {stats['lecturer_count']}")
            print(f"    Số môn học: {stats['course_count']}")
            print(f"    Tổng số SV: {stats['student_count']}")

            if stats['lecturer_count'] > 0:
                avg_courses = stats['course_count'] / stats['lecturer_count']
                print(f"    Số môn trung bình/GV: {avg_courses:.1f}")

        input("\n\nNhấn Enter để tiếp tục...")

    def grade_statistics_report(self):
        """Thống kê điểm"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     THỐNG KÊ ĐIỂM")
        print("="*50)

        all_grades = self.read_file(self.data_files['grades'])
        all_courses = self.read_file(self.data_files['courses'])

        if not all_grades:
            print("\nChưa có dữ liệu điểm!")
            input("\nNhấn Enter để tiếp tục...")
            return

        print(f"\nTổng số bản ghi điểm: {len(all_grades)}")

        # Thống kê điểm theo môn học
        course_stats = {}
        for grade in all_grades:
            course_id = grade.get('course_id')
            if course_id not in course_stats:
                course_stats[course_id] = {
                    'grades': [],
                    'total_score': 0,
                    'count': 0
                }

            total_score = grade.get('total', 0)
            course_stats[course_id]['grades'].append(total_score)
            course_stats[course_id]['total_score'] += total_score
            course_stats[course_id]['count'] += 1

        print(f"\n📊 THỐNG KÊ ĐIỂM THEO MÔN HỌC:")
        print("-"*80)
        print(f"{'STT':<5} {'Môn học':<25} {'Số SV':<8} {'Điểm TB':<10} {'Điểm cao nhất':<15} {'Điểm thấp nhất':<15}")
        print("-"*80)

        for i, (course_id, stats) in enumerate(course_stats.items(), 1):
            # Tìm thông tin môn học
            course = next((c for c in all_courses if c.get('course_id') == course_id), None)
            course_name = course.get('course_name', 'N/A') if course else 'N/A'

            count = stats['count']
            avg_score = stats['total_score'] / count if count > 0 else 0
            max_score = max(stats['grades']) if stats['grades'] else 0
            min_score = min(stats['grades']) if stats['grades'] else 0

            print(f"{i:<5} {course_name:<25} {count:<8} {avg_score:<10.1f} {max_score:<15.1f} {min_score:<15.1f}")

        # Phân loại điểm
        grade_categories = {
            'Xuất sắc (90-100)': 0,
            'Giỏi (80-89)': 0,
            'Khá (70-79)': 0,
            'Trung bình (60-69)': 0,
            'Yếu (50-59)': 0,
            'Kém (<50)': 0
        }

        for grade in all_grades:
            total_score = grade.get('total', 0)

            if total_score >= 90:
                grade_categories['Xuất sắc (90-100)'] += 1
            elif total_score >= 80:
                grade_categories['Giỏi (80-89)'] += 1
            elif total_score >= 70:
                grade_categories['Khá (70-79)'] += 1
            elif total_score >= 60:
                grade_categories['Trung bình (60-69)'] += 1
            elif total_score >= 50:
                grade_categories['Yếu (50-59)'] += 1
            else:
                grade_categories['Kém (<50)'] += 1

        print(f"\n📈 PHÂN LOẠI ĐIỂM:")
        total_students = sum(grade_categories.values())

        for category, count in grade_categories.items():
            percentage = (count / total_students * 100) if total_students > 0 else 0
            print(f"  {category}: {count} SV ({percentage:.1f}%)")

        input("\n\nNhấn Enter để tiếp tục...")

    # ========== THOÁT CHƯƠNG TRÌNH ==========

    def exit_program(self):
        """Thoát chương trình"""
        self.clear_screen()
        print("\n" + "="*50)
        print("     HỆ THỐNG QUẢN LÝ SINH VIÊN")
        print("="*50)
        print("\nCảm ơn bạn đã sử dụng chương trình!")
        print("Chương trình sẽ thoát...")
        print("\n" + "="*50)
        sys.exit(0)

    # ========== CHẠY CHƯƠNG TRÌNH ==========

    def run(self):
        """Chạy chương trình chính"""
        self.clear_screen()
        print("\n" + "="*60)
        print("           HỆ THỐNG QUẢN LÝ SINH VIÊN")
        print("="*60)
        print("\nPhiên bản: 4.0")
        print("Chức năng chính:")
        print("  • Quản trị: Quản lý người dùng, sinh viên, giảng viên, môn học")
        print("  • Giảng viên: Quản lý điểm, điểm danh, bài tập")
        print("  • Sinh viên: Xem điểm, lịch học, đăng ký môn học")
        print("\n" + "="*60)

        input("Nhấn Enter để tiếp tục...")

        # Tạo file mặc định nếu cần
        self.create_default_files()

        # Vòng lặp chính
        while True:
            if not self.current_user:
                if not self.login():
                    continue
            else:
                if self.current_role == 'admin':
                    self.admin_menu()
                elif self.current_role == 'lecturer':
                    self.lecturer_menu()
                elif self.current_role == 'student':
                    self.student_menu()
                else:
                    print(f"\nVai trò không xác định: {self.current_role}")
                    self.current_user = None
                    self.current_role = None


# ========== CHẠY CHƯƠNG TRÌNH ==========

def main():
    try:
        system = StudentManagementSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\nChương trình bị ngắt bởi người dùng.")
    except Exception as e:
        print(f"\nLỗi không mong muốn: {e}")
        import traceback
        traceback.print_exc()
        input("\nNhấn Enter để thoát...")

    print("\n" + "="*60)
    print("Cảm ơn đã sử dụng Hệ thống Quản lý Sinh viên!")
    print("="*60)


if __name__ == "__main__":
    main()