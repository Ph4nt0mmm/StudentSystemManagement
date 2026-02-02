# StudentSystemManagement
Hệ Thống Quản Lý Sinh Viên (Student Management System)
📋 Giới thiệu
Hệ thống quản lý sinh viên là một ứng dụng console được xây dựng bằng Python, cho phép quản lý toàn diện thông tin sinh viên, giảng viên, môn học, điểm số và các hoạt động liên quan trong môi trường giáo dục.

✨ Tính năng chính
👨‍💼 Quản trị viên (Admin)
-	Quản lý người dùng (thêm, sửa, xóa, tìm kiếm)
-	Quản lý sinh viên
-	Quản lý giảng viên
-	Quản lý môn học
-	Xem báo cáo thống kê
-	Sao lưu dữ liệu
-	Khóa/mở tài khoản người dùng

👨‍🏫 Giảng viên (Lecturer)
-	Xem danh sách môn học đang dạy
-	Quản lý sinh viên trong lớp
-	Nhập và quản lý điểm số
-	Tạo bài tập mới
-	Điểm danh sinh viên
-	Xem lịch dạy

👨‍🎓 Sinh viên (Student)
-	Xem thông tin môn học đã đăng ký
-	Xem điểm số cá nhân
-	Đăng ký môn học mới
-	Xem lịch học
-	Quản lý bài tập (xem, nộp bài, xem trạng thái)
-	Xem và chỉnh sửa thông tin cá nhân

🚀 Hướng dẫn sử dụng
1. Khởi động hệ thống
-	Chạy file main.py
-	Hệ thống tự động tạo file dữ liệu nếu chưa có
-	Đăng nhập với tài khoản admin mặc định hoặc tài khoản đã tạo
2. Quản lý người dùng (Admin)
-	Thêm người dùng: Chọn loại người dùng → Nhập thông tin
-	Tìm kiếm: Theo username, họ tên, email, vai trò, trạng thái
-	Chỉnh sửa: Sửa thông tin cá nhân, đổi mật khẩu
- Khóa/mở tài khoản: Quản lý trạng thái hoạt động
3. Quản lý sinh viên
-	Thêm sinh viên: Nhập đầy đủ thông tin cá nhân
-	Xem danh sách: Hiển thị theo lớp, khoa
-	Xuất danh sách: Ra file .txt hoặc .csv
-	Tìm kiếm: Theo mã SV, họ tên, lớp
4. Quản lý giảng viên
-	Thêm giảng viên: Nhập thông tin chuyên môn
-	Phân công môn học: Gán môn học cho giảng viên
-	Thống kê: Số môn đang dạy, tổng sinh viên
5. Quản lý môn học
-	Thêm môn học: Mã môn, tên, số tín chỉ, mô tả
-	Phân công giảng viên: Gán giảng viên phụ trách
-	Quản lý đăng ký: Theo dõi số lượng sinh viên đăng ký
6. Quản lý điểm (Giảng viên)
-	Nhập điểm: Điểm chuyên cần, giữa kỳ, cuối kỳ
-	Tính điểm tự động: Chuyển đổi sang điểm chữ (A, B, C, D, F)
-	Xem thống kê: Điểm trung bình, phân phối điểm

7. Bài tập (Sinh viên)
-	Xem bài tập: Danh sách bài tập theo môn
-	Nộp bài: Nhập nội dung hoặc link bài nộp
-	Xem trạng thái: Điểm, nhận xét từ giảng viên

📊 Báo cáo và thống kê
1. Báo cáo tổng quan
-	Thống kê số lượng người dùng
-	Số môn học, lớp học
-	Tỉ lệ sinh viên/giảng viên
2. Báo cáo học tập
-	Phân bố sinh viên theo lớp
-	Top sinh viên xuất sắc
-	Phân phối điểm theo môn
3. Báo cáo giảng dạy
-	Top giảng viên có nhiều môn nhất
-	Thống kê theo khoa
-	Giảng viên chưa được phân công
4. Thống kê điểm
-	Điểm trung bình theo môn
-	Phân loại điểm (Xuất sắc, Giỏi, Khá, ...)
-	Điểm cao nhất/thấp nhất

🔒 Bảo mật và sao lưu
  Tính năng bảo mật
-	Mật khẩu được lưu trữ dạng plaintext (có thể nâng cấp)
-	Phân quyền theo vai trò
-	Khóa tài khoản không hoạt động
   Sao lưu dữ liệu
-	Tự động: Tạo thư mục Backups/
-	Thủ công: Chọn từ menu Admin
-	Định dạng: Lưu toàn bộ file dữ liệu
-	Thông tin: Kèm metadata về thời gian sao lưu

- Phiên bản: 4.0
- Cập nhật: Tháng 1, 2024
- Tác giả: Student Management System Team
