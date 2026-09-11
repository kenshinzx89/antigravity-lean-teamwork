# Quản Lý Tác Vụ Bằng Atomic Task Cards

Dành cho các tác vụ thay đổi từ **1–3 files liên quan**.

Thay vì để 1 agent nhận một yêu cầu rộng rồi tự sửa tự chạy không kiểm soát, hệ thống sử dụng quy trình tinh gọn với **Intake Dispatcher** và các **Thẻ Nhiệm Vụ Nguyên Tử (Atomic Task Cards)**.

---

## 1. Luồng Vận Hành

```text
User -> Intake Dispatcher -> Atomic Task Card(s)
                                  │
                    Explorer / Worker -> Independent Checker
                                  │              │
                                  └─── PASS ─────┘
                                         │
                                   Thẻ tiếp theo
                                         │
                                     Hoàn thành
```

---

## 2. Nguyên Tắc Cốt Lõi

1. **Một chủ sở hữu (Single Owner)**: Mỗi file chỉ được gán cho đúng 1 Worker tại một thời điểm để tránh xung đột mã nguồn.
2. **Một người kiểm tra độc lập (Independent Checker)**: Người viết code không được tự xác nhận code của mình đã hoàn hảo; Checker phải chạy lệnh kiểm tra thực tế.
3. **Ranh giới bất biến (Boundaries)**: Xác định rõ phần mã nào CẤM chỉnh sửa trước khi bắt đầu.
4. **Bằng chứng độc lập (Objective Evidence)**: Tác vụ chỉ kết thúc khi lệnh kiểm tra trả về exit code 0 hoặc kết quả quan sát trực tiếp được ghi nhận.

---

## 3. Cấu Trúc Atomic Task Card

```markdown
## Task <ID>: <Một kết quả quan sát được duy nhất>
- Owner: <1 Worker cụ thể>
- Checker: <1 Checker độc lập>
- Files Owned: <Đường dẫn file cụ thể, các file khác là Read-only>
- Preconditions: <Các sự thật kỹ thuật đã được kiểm chứng>
- Allowed Changes: <Thay đổi tối thiểu được phép thực hiện>
- Boundaries (Must NOT change): <Các ranh giới cấm can thiệp>
- Acceptance Check: <Lệnh test cụ thể, API call hoặc tương tác UI>
- Required Evidence: <Kết quả exit code / log khẳng định / screenshot>
- Failure Handling: <Trả lỗi chi tiết về Owner; không tự ý mở rộng phạm vi>
```
