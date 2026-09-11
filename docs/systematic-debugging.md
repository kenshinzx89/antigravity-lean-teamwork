# Cẩm Nang Systematic Debugging (Sửa Bug Có Hệ Thống)

Quy trình 4 pha bắt buộc khi xử lý bất kỳ lỗi kỹ thuật, test failure, hoặc hành vi bất thường nào trong hệ thống Antigravity.

---

## 1. Pha 1: Điều Tra Nguyên Nhân Gốc (Root Cause Investigation)

**Trước khi viết bất kỳ dòng mã sửa lỗi nào:**

1. **Đọc kỹ thông báo lỗi và Stack Trace**:
   - Không lướt qua các cảnh báo.
   - Ghi nhận chính xác số dòng, đường dẫn file, kiểu ngoại lệ (`TypeError`, `NullPointer`, `KeyError`, `Deadlock`).
2. **Tái hiện lỗi ổn định (Reproduce Consistently)**:
   - Các bước kích hoạt lỗi là gì?
   - Lỗi có xuất hiện 100% các lần chạy không?
   - Nếu không tái hiện được, thu thập thêm log thực tế, tuyệt đối không đoán mò.
3. **Kiểm tra thay đổi gần nhất (Recent Changes)**:
   - Chạy `git diff` hoặc kiểm tra commit gần đây để xem đoạn code nào mới thay đổi có thể là nguồn cơn.
4. **Cô lập ranh giới trong hệ thống nhiều tầng (Multi-Component Isolation)**:
   - Thêm log chẩn đoán tại ranh giới dữ liệu vào/ra giữa các component (Frontend -> API -> Service -> Database) để xác định chính xác tầng nào gây ra lỗi.

---

## 2. Pha 2: Phân Tích Mẫu & Đối Chiếu (Pattern Analysis)

1. **Tìm kiếm các đoạn mã hoạt động tốt (Working Examples)**:
   - Trong repo có hàm hoặc module nào tương tự đang hoạt động ổn định không?
   - Đoạn code bị lỗi khác biệt ở điểm nào so với đoạn code chuẩn?
2. **Kiểm tra điều kiện biên (Edge Cases)**:
   - Dữ liệu rỗng (`null`, `empty`, `undefined`)?
   - Giá trị cực đại, số âm, hoặc vấn đề encoding Unicode?

---

## 3. Pha 3: Giả Thuyết & Kiểm Thử Tối Thiểu (Hypothesis & Minimal Test)

1. **Đưa ra giả thuyết khoa học**:
   - *"Lỗi xảy ra vì biến X bị null khi hàm Y trả về kết quả rỗng trong trường hợp Z."*
2. **Kiểm chứng giả thuyết bằng test case trước khi sửa mã nguồn**:
   - Tạo unit test nhỏ thể hiện giả thuyết này.
   - Chạy test và xác nhận test FAIL đúng như dự đoán (Red Phase).

---

## 4. Pha 4: Sửa Tối Thiểu & Nghiệm Thu Khách Quan (Minimal Fix & Verification)

1. **Minimal Compatible Diff**:
   - Chỉ sửa đúng 1–3 dòng mã để triệt tiêu nguyên nhân gốc.
   - Giữ nguyên toàn bộ cấu trúc và quy ước code xung quanh.
2. **Kiểm chứng lại (Green Phase)**:
   - Chạy lại test tái hiện lỗi -> Xác nhận PASS (exit code 0).
   - Chạy toàn bộ test suite hồi quy (regression suite) -> Xác nhận không gây ra lỗi phụ.
3. **Tự vấn Quota**:
   - Tự hỏi: Có thể gom lệnh test hoặc dọn dẹp log chẩn đoán vừa thêm không?
