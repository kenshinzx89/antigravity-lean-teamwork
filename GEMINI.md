# 🤖 Lean Teamwork Workspace Controller (Fast-Sync & Zero-Scan)

> **Dành cho Antigravity trên Laptop / Máy phát triển mới**:
> Khi mở thư mục này và nhận lệnh yêu cầu "update", "cập nhật", hoặc "áp dụng skill":

## ⚡ Lệnh Thực Thi Duy Nhất (Two-Way Adaptive Sync):
- **Zero-Scan Protocol**: TUYỆT ĐỐI KHÔNG dùng tool đọc quét toàn bộ repo (`find_by_name`, `grep_search`, `list_dir`, `view_file` diện rộng) để tránh lãng phí Quota/Token.
- Chạy DUY NHẤT 1 lệnh terminal:
  ```powershell
  py sync_skill.py
  ```
- **Cơ chế Thông Minh 2 Chiều**:
  - Nếu **Folder gốc lớn hơn**: Tự động **PULL** bản mới vào máy tính.
  - Nếu **Máy tính này mới hơn**: Tự động **PUSH** ngược về folder gốc để PC/thiết bị khác dùng ngay.
  - Hợp nhất 2 chiều toàn bộ kho tri thức `learned_patterns.md`.
  - Khởi tạo và kiểm tra tính toàn vẹn của Stock Core `GEMINI.md`.
  - Chạy kiểm thử tự động đạt 100% PASS (Exit code 0).
- Sau khi lệnh chạy xong, thông báo ngắn gọn phiên bản cập nhật cho người dùng.

---

## 📈 Tự Động Tăng Phiên Bản (Khi hoàn tất học hỏi mới):
```powershell
py sync_skill.py --bump patch
```
