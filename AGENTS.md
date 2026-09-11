# 🤖 Chỉ Dẫn Vận Hành Nhanh Cho Antigravity (Laptop / Máy Mới)

> **Mục tiêu**: Cài đặt / Cập nhật Lean Teamwork lên máy tính mới trong 1 giây, **TUYỆT ĐỐI KHÔNG đọc quét lại toàn bộ repository để tiết kiệm 100% Quota/Token**.

---

## ⚡ 1. Khi Người Dùng Yêu Cầu "update", "cập nhật" hoặc "áp dụng skill":

Agent **KHÔNG ĐƯỢC** dùng các tool đọc quét mã nguồn (`find_by_name`, `grep_search`, `list_dir` diện rộng).  
Thay vào đó, Agent **chỉ cần chạy DUY NHẤT 1 lệnh terminal**:

```powershell
py sync_skill.py
```

**Cơ chế Thông Minh 2 Chiều (Two-Way Adaptive Sync)**:
- Lệnh tự động so sánh số phiên bản:
  - Nếu **Folder gốc lớn hơn**: Tự động **PULL** bản mới vào máy tính.
  - Nếu **Máy tính này mới hơn** (vừa học được kiến thức mới): Tự động **PUSH** ngược về folder gốc để PC và các máy khác dùng ngay.
  - Tự động hợp nhất 2 chiều toàn bộ kho tri thức `learned_patterns.md`.
  - Tự động chạy kiểm thử verification đạt 100% PASS (Exit Code 0).

---

## 📈 2. Cơ Chế Tăng Phiên Bản (Versioning) Khi Học Hỏi Mới:

Khi Subagent hoàn tất một chu kỳ đúc kết tri thức mới (Self-Evolution), chạy lệnh bump version tự động:

```powershell
py sync_skill.py --bump patch
```

*Lệnh này sẽ tự động tăng số patch (ví dụ: `1.2.1` -> `1.2.2`), cập nhật `VERSION` và đồng bộ 2 chiều ngay lập tức.*

---

## 🛡️ 3. Thiết Luật Bất Biến:
- **Zero-Scan Protocol**: Khi mở thư mục này trên laptop, Agent đọc file `AGENTS.md` hoặc `GEMINI.md` này và thi hành lệnh ngay, không đọc lan man.
- **Two-Way Parity**: Luôn giữ phiên bản và tri thức giữa folder gốc và máy tính đồng nhất.
- **Knowledge Segregation**: Tri thức chỉ lưu ở `learned_patterns.md`, tuyệt đối không nhồi nhét vào `SKILL.md`.
