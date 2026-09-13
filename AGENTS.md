# 🤖 Chỉ Dẫn Vận Hành Tự Động Cho AI (Máy Mới / Máy Phát Triển Khác)

> **MỤC TIÊU CỐT TỬ**: Khi người dùng chuyển sang một máy tính mới hoàn toàn, tải repo này về và chỉ cần bảo AI:
> **"cài và sử dụng"** (hoặc "cài đặt", "setup", "áp dụng skill", "cập nhật", "update")...
> AI phải thiết lập **HOÀN THIỆN 100% NGAY LẬP TỨC Y NHƯ TRÊN MÁY GỐC**, không phát sinh bất kỳ lỗi nào, không thiếu bất kỳ thành phần nào.

---

## ⚡ 1. Khi Người Dùng Yêu Cầu "cài và sử dụng", "cài đặt", "setup" hoặc "áp dụng skill":

Agent **TUYỆT ĐỐI KHÔNG DÙNG TOOL ĐỌC QUÉT MÃ NGUỒN** (`find_by_name`, `grep_search`, `list_dir`, `view_file` diện rộng) để tiết kiệm 100% Quota/Token.  
Thay vào đó, Agent **chỉ cần chạy DUY NHẤT 1 lệnh terminal**:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
*(hoặc nếu đang ở môi trường Python trực tiếp: `py sync_skill.py`)*

---

## 🛠️ 2. Những Gì Hệ Thống Tự Động Thiết Lập Trọn Gói (Full Parity Guarantee):

Khi lệnh trên chạy xong, toàn bộ môi trường máy mới sẽ trở nên y hệt máy gốc:
1. **Nạp Skill Toàn Cục & Builtin**:
   - Nạp Lean Teamwork Protocol vào `~/.gemini/config/skills/lean-teamwork`.
   - Nạp vào Builtin Skills của IDE Antigravity (`~/.gemini/antigravity/builtin/skills/lean-teamwork`).
2. **Kích Hoạt PreInvocation Lifecycle Hook**:
   - Tự động cấu hình `~/.gemini/config/hooks.json` với đường dẫn Python động (`sys.executable`), hoạt động trên mọi phiên bản Python bất kể Windows đã add Python to PATH hay chưa.
3. **Neo Luật Toàn Cục Tối Cao (GEMINI.md)**:
   - Tự động duy trì mỏ neo Lean Teamwork trên mọi workspace của Antigravity IDE.
4. **Hợp Nhất 2 Chiều Toàn Bộ Kho Tri Thức (19 Patterns)**:
   - Tự động cân bằng và nạp 19 bài học kinh nghiệm từ `learned_patterns.md` vào máy tính mới.
5. **Cơ Chế Dual Account Detection (Tự Động Kết Nối Native IDE)**:
   - Nếu máy mới **chưa cài Cockpit Tool**: Widget tự động trích xuất trực tiếp tài khoản Google đang đăng nhập trong Google Antigravity IDE (`state.vscdb`), hiển thị tên và email thật, **tuyệt đối không bị lỗi đỏ `Offline` hay `No Acc`**.
6. **Không Cần Cài Thêm Thư Viện (Zero External Pip Dependencies)**:
   - Toàn bộ Desktop Widget chạy 100% trên Python Standard Library (`ctypes` Win32 GDI+), không cần `pip install` bất cứ thứ gì.
7. **Khởi Động Widget HUD & Tạo Shortcut Desktop**:
   - Tự động tạo Shortcut `Antigravity Widget` ngoài Desktop.
   - Tự động kích hoạt Widget chạy ngầm êm ái bằng `wscript.exe` (không hiện cửa sổ cmd đen).
8. **Kiểm Thử Toàn Vẹn Hệ Thống (18/18 Tests PASS)**:
   - Tự động chạy bộ test kiểm tra, đảm bảo exit code 0 trước khi bàn giao cho người dùng.

---

## 📈 3. Cơ Chế Tăng Phiên Bản (Versioning) Khi Học Hỏi Mới:

Khi Subagent hoàn tất một chu kỳ đúc kết tri thức mới (Self-Evolution), chạy lệnh bump version tự động:

```powershell
py sync_skill.py --bump patch
```

*Lệnh này sẽ tự động tăng số patch (ví dụ: `1.5.1` -> `1.5.2`), cập nhật `VERSION` và đồng bộ 2 chiều ngay lập tức.*

---

## 🛡️ 4. Thiết Luật Bất Biến:
- **Zero-Scan Protocol**: Khi mở thư mục này trên máy mới, Agent đọc file `AGENTS.md` hoặc `GEMINI.md` này và thi hành lệnh ngay, không đọc lan man.
- **Two-Way Parity**: Luôn giữ phiên bản và tri thức giữa folder gốc và máy tính đồng nhất.
- **From-Last-Completion Anchor**: Khi người dùng chưa bấm Hoàn tất vì còn lỗi và tiếp tục chat, đến khi bấm Hoàn tất phải tổng hợp toàn bộ các lỗi trung gian từ lần bấm Hoàn tất gần nhất đến nay.
