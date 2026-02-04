# 🎓 HỆ THỐNG QUẢN LÝ SINH VIÊN

## 📌 Giới thiệu

Hệ thống quản lý sinh viên là một ứng dụng console-based được phát triển bằng Python, cung cấp đầy đủ các chức năng quản lý cho trường học với 3 vai trò người dùng: Quản trị viên, Giảng viên và Sinh viên.

---

## 🎯 Mục tiêu

* Quản lý thông tin sinh viên, giảng viên và quản trị viên
* Lưu trữ dữ liệu bằng **file text** (không cần CSDL)
* Phân quyền rõ ràng theo vai trò người dùng
* Áp dụng kiến thức lập trình hướng đối tượng

---

## 👥 Các vai trò trong hệ thống

### 🔑 Admin (Quản trị viên)

✅ Quản lý người dùng (thêm, sửa, xóa, tìm kiếm)

✅ Quản lý sinh viên toàn diện

✅ Quản lý giảng viên và phân công môn học

✅ Quản lý môn học (thêm, chỉnh sửa, phân công giảng viên)

✅ Xem báo cáo thống kê chi tiết

✅ Sao lưu và phục hồi dữ liệu

✅ Khóa/mở tài khoản người dùng

### 👨‍🏫 Giảng viên

✅ Xem danh sách môn học đang dạy

✅ Xem danh sách sinh viên theo môn

✅ Quản lý điểm (nhập điểm, sửa điểm)

✅ Tạo và quản lý bài tập

✅ Điểm danh sinh viên

✅ Xem lịch dạy hàng tuần

### 👨‍🎓 Sinh viên

✅ Xem môn học đã đăng ký

✅ Xem điểm chi tiết theo môn

✅ Đăng ký môn học mới

✅ Xem lịch học cá nhân

✅ Quản lý bài tập (xem, nộp, xem trạng thái)

✅ Xem và chỉnh sửa thông tin cá nhân

✅ Đổi mật khẩu

---

📝 HƯỚNG DẪN SỬ DỤNG
🔐 Đăng nhập

Chạy chương trình:

python main.py

Nhập tên đăng nhập và mật khẩu

Hệ thống tự động nhận diện vai trò và hiển thị menu phù hợp

🗂️ Quản lý dữ liệu


➕ Tạo mới: Sử dụng chức năng Thêm trong các menu quản lý

✏️ Chỉnh sửa: Chọn Chỉnh sửa / Sửa thông tin

❌ Xóa: Chọn Xóa (có bước xác nhận)

🔍 Tìm kiếm: Hỗ trợ tìm theo nhiều tiêu chí

💾 Sao lưu dữ liệu

Truy cập: Admin → Sao lưu dữ liệu

Dữ liệu được lưu tại thư mục Backups/ kèm timestamp

📊 TÍNH NĂNG BÁO CÁO

1️⃣ Báo cáo tổng quan

Thống kê số lượng người dùng

Số lượng môn học, lớp học

Tỉ lệ sinh viên / giảng viên

2️⃣ Báo cáo học tập

Phân bố sinh viên theo lớp

Thống kê điểm trung bình

Top sinh viên xuất sắc

3️⃣ Báo cáo giảng dạy

Thống kê giảng viên theo khoa

Số môn học mỗi giảng viên phụ trách

Danh sách giảng viên chưa được phân công

4️⃣ Thống kê điểm

Phân loại điểm: Xuất sắc / Giỏi / Khá / Trung bình / Yếu

Điểm trung bình theo môn

Điểm cao nhất / thấp nhất

🔧 TÍNH NĂNG BẢO MẬT

🔑 Xác thực người dùng: Đăng nhập bằng username/password

👥 Phân quyền: Menu riêng cho từng vai trò

🔒 Mật khẩu: Mã hóa cơ bản trong file dữ liệu

🚫 Khóa tài khoản: Admin có thể khóa/mở tài khoản

⚠️ An toàn: Admin không thể tự khóa chính mình

📈 TÍNH NĂNG HỌC TẬP

🧮 Quản lý điểm

Hệ thống tính điểm tự động

Chuyển đổi: Điểm số → Điểm chữ → GPA

Công thức: Chuyên cần (10%) + Giữa kỳ (30%) + Cuối kỳ (60%)

📝 Quản lý bài tập

Giảng viên: Tạo bài tập kèm deadline

Sinh viên: Nộp bài, xem phản hồi

Theo dõi trạng thái nộp bài

🧾 Điểm danh

Trạng thái: Có mặt / Vắng / Muộn / Có phép

Tính tỉ lệ điểm danh tự động

Lưu lịch sử điểm danh

💽 LƯU TRỮ DỮ LIỆU

Định dạng: Mỗi bản ghi là một dictionary Python

Mã hóa: UTF-8

Backup: Tự động tạo thư mục sao lưu

Khôi phục: Sao chép file từ thư mục backup

🐛 XỬ LÝ LỖI


❗ Đăng nhập sai: Thông báo rõ ràng, cho phép thử lại

⚠️ Nhập liệu sai: Kiểm tra định dạng & giá trị hợp lệ

📁 Lỗi file: Tự tạo file mới nếu chưa tồn tại

🛡️ Exception handling: Bắt và xử lý ngoại lệ an toàn

🔄 PHIÊN BẢN
Phiên bản hiện tại: 4.0
