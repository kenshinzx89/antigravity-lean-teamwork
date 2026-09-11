# Tham Chiếu Kiến Trúc: Lean Teamwork

## 1. Bản Đồ Điều Phối

```text
User
  └── Intent Architect (Khóa Execution Brief)
        └── Orchestrator (Điều phối)
              ├── Explorer (Model: flash, Read-only)
              ├── Workers (Tối đa 2 Workers, Model: inherit/pro)
              └── Gatekeeper (Model: flash, Test runner & Audit)
```

## 2. Nguyên Tắc Cốt Lõi

1. **Frozen Brief**: Sau khi duyệt, scope bị khóa. Mọi thay đổi phải tạo Brief phiên bản mới.
2. **Independent Gates**: Không cho phép worker tự xác nhận hoàn thành. Bắt buộc có Gatekeeper độc lập chạy lệnh kiểm tra thực tế.
3. **No Majority Voting**: Bỏ cơ chế biểu quyết thuần lý thuyết; chỉ chấp nhận bằng chứng vật lý từ terminal/test suite.
