## Task <ID>: <Một kết quả quan sát được duy nhất>

- **Owner**: <1 Worker cụ thể>
- **Checker**: <1 Gatekeeper / Independent Checker>
- **Files Owned**: <Danh sách file cụ thể; các file khác là Read-only>
- **Preconditions**: <Các sự thật kỹ thuật đã được kiểm chứng>
- **Allowed Changes**: <Thay đổi tối thiểu được phép thực hiện>
- **Boundaries (Must NOT change)**: <Các ranh giới cấm can thiệp>
- **Reproduction / Verification Test**:
  - Test command: `<lệnh test>`
  - Red phase: `<output chứng minh test fail trước khi sửa>`
  - Green phase: `<output chứng minh test pass sau khi sửa>`
- **Ruling Log** (nếu có phán quyết nhỏ):
  - `Ruling: <Quyết định> — <Lý do> — <Hệ quả nếu sai>`
- **Required Evidence**: <Kết quả exit code 0 / log khẳng định>
- **Failure Handling**: <Trả lỗi chi tiết về Owner; tối đa 2 chu kỳ sửa>
