# 🚀 HƯỚNG DẪN CÀI ĐẶT TOÀN DIỆN CHO MÁY MỚI (INSTALLATION GUIDE)

> **Antigravity Lean Teamwork v1.5.0 + Desktop Widget HUD Monorepo**  
> Bộ công cụ tối thượng: Kỷ luật kỹ thuật tinh gọn cho Google Antigravity IDE kết hợp thanh trạng thái kính mờ HUD nổi ngoài màn hình.

---

## 📋 1. Yêu Cầu Hệ Thống (Prerequisites)

- **Hệ điều hành**: Windows 10 / Windows 11 (64-bit).
- **Python**: Phiên bản 3.10 trở lên (khuyên dùng Python 3.11 hoặc 3.12).
  - Kiểm tra trong terminal:
    ```powershell
    py --version
    # hoặc
    python --version
    ```
- **IDE**: Google Antigravity (Gemini 3.7 / 3.8).

---

## ⚡ 2. Cài Đặt Nhanh 1-Click (Recommended — Chỉ Mất 5 Giây)

Sau khi tải hoặc clone repository về máy tính mới:

```powershell
git clone https://github.com/kenshinzx89/antigravity-lean-teamwork.git
cd antigravity-lean-teamwork
```

Chạy **DUY NHẤT 1 LỆNH**:

```powershell
.\install.ps1
```

*(Hoặc mở Command Prompt / PowerShell và chạy: `py sync_skill.py`)*

### 🛠️ Script Cài Đặt Sẽ Tự Động Thực Hiện:
1. Nạp **Lean Teamwork Protocol v1.5.0** vào cấu hình Antigravity IDE (`~/.gemini/config/skills/lean-teamwork`).
2. Kích hoạt **PreInvocation Lifecycle Hook** (`~/.gemini/config/hooks.json`) để IDE luôn tự động tuân thủ kỷ luật kỹ thuật.
3. Hợp nhất kho tri thức kinh nghiệm **19 Patterns** (`learned_patterns.md`).
4. Khởi động ngay thanh **Antigravity Desktop Widget** nổi trên màn hình.
5. Tạo phím tắt khởi động ngoài màn hình Desktop.

---

## 🖱️ 3. Cài Đặt Thủ Công Từng Bước (Manual Setup)

Nếu bạn muốn tự tay kiểm soát từng bước mà không chạy script tự động:

### Bước 1: Đồng bộ Skill & Hook vào Antigravity IDE
```powershell
py sync_skill.py
```
*Kết quả thành công sẽ báo: `ALL 11/11 SYSTEM CHECKS PASSED (Exit Code 0)`.*

### Bước 2: Khởi động Desktop Widget HUD
- Chạy qua Python:
  ```powershell
  pythonw widget\main.py
  ```
- Hoặc double-click trực tiếp vào file:
  `widget\KHOI_DONG_WIDGET.vbs` (chạy ngầm êm ái, không hiện cửa sổ đen cmd).

---

## 🔄 4. Tự Động Khởi Động Widget Cùng Windows (Auto-Start on Boot)

Để Desktop Widget luôn sẵn sàng mỗi khi bạn mở máy:

1. Nhấn tổ hợp phím `Win + R`.
2. Gõ `shell:startup` và nhấn **Enter** (thư mục Startup của Windows sẽ mở ra).
3. Nhấp chuột phải vào file `widget\KHOI_DONG_WIDGET.vbs` trong thư mục dự án -> Chọn **Create shortcut** (Tạo lối tắt).
4. Kéo lối tắt vừa tạo vào thư mục `Startup`.
5. Từ nay, thanh Widget sẽ tự động xuất hiện mỗi khi bạn khởi động máy tính!

---

## 🎯 5. Trải Nghiệm & Vận Hành Thực Tế

### 🧭 A. Đề Xuất Kỹ Thuật (Proposal Mode):
- Khi bạn giao nhiệm vụ mới hoặc AI đứng trước ngã rẽ giải pháp:
- **Khung chat rảnh rang**: AI in tóm tắt ngắn gọn, **TUYỆT ĐỐI KHÔNG BẬT MODAL CHE MÀN HÌNH**.
- **Desktop Widget HUD**: Tự động bung bảng lựa chọn kính mờ với đồng hồ Spectrum đếm ngược 2.5 phút.
- **Tương tác**: Bạn bấm trực tiếp nút phương án trên Desktop Widget -> Lựa chọn được gửi thẳng xuống khung chat IDE!

### 💎 B. Nghiệm Thu Hoàn Thiện (Acceptance Mode):
- Khi AI hoàn thành code và kiểm thử đạt **100% PASS (Exit Code 0)**:
- **Khung chat**: In toàn văn báo cáo kiểm chứng chi tiết, minh bạch.
- **Desktop Widget HUD**: Bung bảng nghiệm thu kính mờ to rõ (+20% font, tự co giãn theo nội dung) với 2 nút kinh điển:
  - `💎 [100% HOÀN TẤT] ✨`: Chấp thuận và tự động khóa tri thức.
  - `⚡ [SUPERPOWERS DEBUG] 🛠️`: Kích hoạt AI chuyên trách truy vết sâu 4 pha.
- Bạn bấm nghiệm thu trực tiếp từ màn hình Desktop Widget mà không bị che mất dòng code nào trong khung chat!

---

## 🛡️ 6. Kiểm Thử Toàn Vẹn Hệ Thống (Verification)

Bất kỳ lúc nào bạn muốn kiểm tra xem toàn bộ hệ thống có hoạt động chuẩn xác hay không:

```powershell
py tests\test_skill_integrity.py
py tests\test_teamwork_bridge.py
```

*Tiêu chuẩn: Toàn bộ 100% tests phải PASS (Exit Code 0).*
