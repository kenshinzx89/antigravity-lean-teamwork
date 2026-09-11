# Tích Hợp Tri Thức & Kinh Nghiệm Từ Superpowers Vào Lean Teamwork

Tài liệu đúc kết các tinh hoa kỹ thuật từ repository `superpowers`, chuyển hóa thành các nguyên lý vận hành cốt lõi cho hệ thống Lean Teamwork.

---

## 1. 3 Thiết Luật Bất Biến (The 3 Iron Laws)

### Thiết Luật 1: Nghiệm Thu Thực Tế (Iron Law of Verification)
> **"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"**
- Không bao giờ tuyên bố một tính năng hoạt động, một bug đã sửa xong hoặc bộ test đã pass nếu bạn chưa trực tiếp chạy lệnh kiểm tra và thấy output thành công ngay trong lượt làm việc đó.
- Cấm tuyệt đối các cụm từ ngụy biện phỏng đoán: *"should work"*, *"probably"*, *"looks correct"*, *"tôi tin là code đã ổn"*.

### Thiết Luật 2: Điều Tra Nguyên Nhân Gốc (Iron Law of Root Cause)
> **"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"**
- Cấm tuyệt đối việc thử sai mù quáng (guess-and-check) hoặc sửa triệu chứng hời hợt (symptom fixing).
- Mọi nỗ lực sửa code đều phải dựa trên:
  1. Đọc toàn bộ stacktrace và mã lỗi.
  2. Tái hiện lỗi ổn định (reproduce consistently).
  3. Lập bản đồ luồng dữ liệu qua các ranh giới component.

### Thiết Luật 3: Tự Ra Phán Quyết Kỹ Thuật (Ruling, Not Stalls)
> **"A RUNNING PLAN DOES NOT WAIT ON A HUMAN FOR MINOR CHOICES"**
- Không dừng phiên làm việc để hỏi những câu hỏi nhỏ nhặt, mang tính suy luận kỹ thuật thông thường.
- Tự đưa ra phán quyết theo cú pháp:
  `Ruling: <Điều bạn quyết định> — <Lý do kỹ thuật> — <Hệ quả/chi phí nếu sai>`
- Chỉ dừng lại hỏi người dùng khi gặp **4 tình huống chặn**:
  1. Thao tác không thể đảo ngược hoặc có nguy cơ mất dữ liệu (xóa bảng, force push, drop schema).
  2. Thay đổi cấu trúc bảo mật/xác thực người dùng.
  3. Tác động ra ngoài ranh giới workspace/project.
  4. Yêu cầu mâu thuẫn hoàn toàn đến mức mọi đường đi tiếp đều là phỏng đoán.

---

## 2. Kỹ Thuật Isolated Context Subagent Dispatching

Từ bài học của `subagent-driven-development` và `dispatching-parallel-agents`:
- **Vấn đề**: Khi spawn subagent mà truyền toàn bộ session chat (hàng chục nghìn tokens), subagent dễ bị phân tâm, tăng nguy cơ hallucination và làm cạn kiệt token quota nhanh gấp 5 lần.
- **Giải pháp Lean Teamwork**:
  - Mỗi Worker subagent chỉ nhận đúng thẻ nhiệm vụ nguyên tử (**Atomic Task Card**):
    - Mục tiêu duy nhất cần hoàn thành.
    - Danh sách file độc quyền được chỉnh sửa.
    - Lệnh kiểm thử cụ thể và output mong đợi.
    - Các ranh giới cấm can thiệp.
  - Subagent không cần biết toàn bộ lịch sử trò chuyện trước đó, giúp tốc độ phản hồi nhanh vượt trội và tiết kiệm tối đa quota.

---

## 3. Quy Chuẩn Red-Green-Refactor (TDD Verification)

- Khi viết regression test cho bug:
  1. **RED**: Viết test tái hiện lỗi -> Chạy thử -> Bắt buộc phải **FAIL** đúng lỗi đó. (Nếu test pass ngay từ đầu, test đó vô giá trị!).
  2. **GREEN**: Viết mã sửa tối thiểu -> Chạy lại test -> Test chuyển sang **PASS**.
  3. **REFACTOR**: Tinh gọn mã nguồn mà vẫn giữ trạng thái PASS.
