# Nghiên Cứu & Đối Chiếu Hệ Sinh Thái Các Repo AI Agent Tự Tiến Hóa (Comparative Study)

Tài liệu khảo sát, đối chiếu các repository mã nguồn mở hàng đầu về AI Agent tự hoàn thiện (Self-Improving Agents), tối ưu hóa Token Quota và cơ chế điều phối đa tác tử, nhằm rút ra các bài học đắt giá cho **Lean Teamwork**.

---

## 1. Bản Đồ Đối Chiếu Các Repository Tiêu Biểu

| Dự Án | Xuất Xứ / Tổ Chức | Điểm Mạnh Cốt Lõi | Cơ Chế Học Hỏi & Tiến Hóa | Hạn Chế Cần Tránh |
|---|---|---|---|---|
| **Hermes Agent** | Nous Research (Local tại `F:/hermes-agent`) | Vòng lặp học tập khép kín, Trajectory Compression, RPC tool calling | Tự tạo skill sau tác vụ phức tạp, FTS5 Session Search, Honcho user modeling | Hệ thống lớn, nhiều tầng hạ tầng (Docker, Modal, VPS), khá nặng nếu chạy CLI cục bộ |
| **Superpowers** | Community (Local tại `F:/superpowers`) | Kỷ luật thép (Iron Laws), Systematic Debugging, Red-Green Verification | Bắt buộc bằng chứng trước tuyên bố (Gate Function), phân lập context subagent | Quy trình nghiêm ngặt dễ gây nghẽn (stall) nếu không có cơ chế *Ruling, not stalls* |
| **DeepSeek Harness** | DeepSeek AI (Local tại `F:/deepseek-harness`) | Kiến trúc Plugin Cordis cực kỳ module hóa, Guard Loop-Hygiene | Compaction capability, Self-modification plugins | Hướng tới framework phát triển lõi hơn là công cụ người dùng cuối |
| **Self-Learning Skills** | Kulaxyz (Open Source) | Trích xuất "Golden Path" từ các session thành công vào file rule | Tự động hóa tạo file `.mdc` / `SKILL.md` sau khi hoàn thành task | Thiếu cơ chế kiểm thử đối kháng (không có independent checker) |
| **Recursive-Improve** | Kayba-ai (Open Source) | Cơ chế bánh răng khóa (`/ratchet mode`) chống hồi quy | Bắt giữ vết lỗi (trace), áp dụng patch và khóa chặt lỗi không lặp lại | Tốn token nếu chạy vòng lặp lặp vô hạn mà không có Subagent Cap |
| **Reflexio** | ReflexioAI (Open Source) | Trích xuất Playbook hành động từ sai lệch giữa Agent và Chuyên gia | Tạo playbook chẩn đoán dựa trên sự tương phản (Contrastive Learning) | Phụ thuộc nhiều vào feedback mẫu lý tưởng từ con người |

---

## 2. 4 Tinh Hoa Đắt Giá Cần Học Hỏi Cho Lean Teamwork

### 1. Cơ Chế "Bánh Răng Khóa" Chống Hồi Quy (The Ratchet Mechanism - từ Recursive-Improve)
- **Ý tưởng**: Trong cơ học, bánh răng khóa (ratchet) chỉ cho phép quay tiến, cấm quay lùi.
- **Áp dụng vào Lean Teamwork**: Mỗi khi một bug được sửa và người dùng bấm "OK", test case tái hiện lỗi đó lập tức trở thành một **Thành Lũy Chống Hồi Quy (Regression Barrier)**. Mọi phiên làm việc tiếp theo khi chạy test suite đều phải bảo toàn các test case này; không bao giờ cho phép một lỗi cũ xuất hiện trở lại.

### 2. Định Dạng "Đường Đi Vàng" (Golden Path Sequence - từ Self-Learning-Skills & Hermes)
- **Ý tưởng**: Không chỉ ghi chép lỗi dưới dạng văn xuôi, mà ghi nhận **chuỗi thao tác công cụ ngắn nhất** (Minimal Tool Action Path).
- **Ví dụ**:
  ```text
  Golden Path [Lỗi Null Pointer DB]:
  1. grep_search: tìm 'query_user'
  2. view_file: kiểm tra null check
  3. replace_file_content: thêm optional chaining (?.)
  4. run_command: pytest tests/test_db.py (Exit 0)
  ```
- **Lợi ích**: Khi gặp lại lỗi này, agent đi thẳng theo Golden Path trong 3 tool calls thay vì mất 10 tool calls tìm kiếm lại từ đầu.

### 3. Nén Vết Hành Động Nguyên Tử (Trajectory Compaction - từ Hermes Agent)
- **Ý tưởng**: Khi giải quyết một tác vụ dài, không giữ toàn bộ 100 dòng log shell trong context chat.
- **Áp dụng vào Lean Teamwork**: Sau mỗi vòng lặp kiểm thử, agent nén output terminal thành 1 dòng **Atomic Milestone**:
  `Milestone #2: Fixed schema syntax -> Passed 5/5 db tests (exit 0) -> Ready for integration.`
  Nhờ đó, context của session luôn được "giặt sạch", token tiêu thụ giảm đến mức tối thiểu.

### 4. Vòng Đời Tự Nâng Cấp Kỹ Năng (Skill Promotion & Pruning)
- **Ý tưởng**: Tri thức không chỉ nằm yên trong một file note.
- **Quy tắc 3 lần (Rule of 3)**:
  - Nếu một pattern trong `learned_patterns.md` được tái sử dụng thành công **3 lần**, hệ thống đề xuất đóng gói pattern đó thành một **Skill con chuyên biệt** hoặc một script helper tự động.
  - Ngược lại, những pattern đã trở nên hiển nhiên hoặc code library đã fix tận gốc thì tự động **tỉa bỏ (Pruning)** để giữ file tri thức luôn tinh gọn.
