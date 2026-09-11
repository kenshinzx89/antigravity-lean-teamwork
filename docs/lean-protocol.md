# Giao Thức Lean Teamwork (Lean Multi-Agent Protocol)

Tài liệu quy định 4 nguyên tắc cốt lõi nhằm kiểm soát token, tối ưu hóa quota API và ngăn chặn bùng nổ agent trong hệ thống Antigravity.

---

## 1. Subagent Cap (Giới Hạn Số Lượng Subagent)

- Mỗi phiên làm việc tối đa chỉ kích hoạt từ **2–4 subagents thiết yếu**:
  - 1 Lead Orchestrator
  - Tối đa 2 Specialized Workers chạy song song cho các module độc lập không phụ thuộc file
  - 1 Independent Gatekeeper / Auditor
- **Nghiêm cấm**: Chia nhỏ nhiệm vụ li ti thành hàng chục subagents hoặc lập hội đồng thẩm định nhiều tầng quá 2 người.

---

## 2. Model Tiering (Phân Tầng Mô Hình)

Chi phí token và hạn ngạch phụ thuộc lớn vào model được chọn:
- `Model: "flash"` hoặc `Model: "flash_lite"`: Bắt buộc sử dụng cho:
  - Khảo sát mã nguồn (Repo Explorer, Codebase Survey)
  - Đọc log, rà soát CSDL thô
  - Chạy test runner và tổng hợp kết quả exit code
  - Gatekeeper & Code Audit
- `Model: "inherit"` hoặc `Model: "pro"`: Chỉ dành riêng cho:
  - Lead Orchestrator thiết kế kế hoạch
  - Worker trực tiếp viết thuật toán phức tạp hoặc xử lý logic cốt lõi.

---

## 3. Compact Handoff (Giao Thức Bàn Giao Ngắn Gọn)

Khi trao đổi thông điệp giữa các agent hoặc tạo báo cáo trung gian:
- Nội dung báo cáo bắt buộc **dưới 20 dòng**.
- Cấu trúc gồm 4 phần ngắn gọn:
  1. `Trạng thái`: Done / Failed / Blocked
  2. `File đã sửa/tạo`: Danh sách file cụ thể
  3. `Kiểm chứng & Exit Code`: Lệnh đã chạy kèm exit code thực tế
  4. `Rủi ro / Điểm cần lưu ý`: 1-2 gạch đầu dòng
- **Tuyệt đối không**: Dump toàn bộ log kiểm thử 1000 dòng, schema CSDL thô hay văn xuôi giải thích dài dòng vào context.

---

## 4. Zero-Spawn Minor Remediation (Sửa Lỗi Vi Mô Không Sinh Subagent)

- Khi phát hiện lỗi cú pháp vi mô (thiếu import, sai kiểu dữ liệu, thiếu tham số nhỏ, typo):
  - Agent hiện tại hoặc Worker sẵn có tự sửa trực tiếp trong 1 thao tác diff tối thiểu (*Minimal Diff*).
  - **Nghiêm cấm**: Sinh thêm subagent mới (Fixer, Corrector, Challenger) chỉ để sửa vài dòng mã.
- **Bounded Repair Loop**: Tối đa 2 chu kỳ sửa lỗi cho mỗi tiêu chí nghiệm thu. Nếu sau 2 lần vẫn thất bại, dừng lại báo cáo người dùng thay vì lặp vô tận.
