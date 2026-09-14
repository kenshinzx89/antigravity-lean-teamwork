# 🎨 Kho Thẩm Mỹ & Bản Sắc Thiết Kế UI/UX (UI/UX Design DNA & Taste Profile)

> **MỤC TIÊU**: Lưu giữ toàn bộ gu thẩm mỹ, quy chuẩn tương tác và thành phần giao diện đã được người dùng phê duyệt qua các phiên nghiệm thu.
> Khi bước vào bất kỳ tác vụ nào liên quan đến UI/UX, AI tự động nạp khối `<UI_UX_DESIGN_DNA>` tinh gọn (~150 tokens) để thiết kế chuẩn xác ngay từ Turn 1 (First-Time Right UI), triệt tiêu hoàn toàn việc người dùng phải nhắc đi nhắc lại mô tả giao diện.

---

## 💎 Khối Design DNA Tinh Gọn (Dành Cho Auto-Injection)

```xml
<UI_UX_DESIGN_DNA>
  <theme mode="dark" background="#0D1117" surface="#161B22" surface_hover="#21262D" glassmorphism="acrylic-blur(20px)" />
  <palette primary="#58A6FF" accent="macOS-Spectrum-7-Color" success="#2EA043" warning="#D29922" border="rgba(255,255,255,0.08)" />
  <geometry border_radius="12px-16px (squircle)" pill_badge="999px" button_padding="8px 16px" layout_spacing="compact-lean" />
  <typography font_family="Inter, Segoe UI, -apple-system, sans-serif" font_size_base="13px-14px" heading_weight="600-semibold" text_contrast="high" />
  <motion transition="all 150ms-250ms cubic-bezier(0.16, 1, 0.3, 1)" hover_feedback="scale(1.02) or highlight" />
  <anti_patterns>
    - CẤM: Viền đen thô, border dày > 1px, drop-shadow đen kịt kiểu cũ.
    - CẤM: Modal popup đóng băng hoặc che khuất nội dung báo cáo đang đối chứng.
    - CẤM: Phông chữ Serif generic (Times New Roman) hoặc màu neon chói lóa nhức mắt.
    - CẤM: Bố cục dàn trải lãng phí diện tích hiển thị (phải ưu tiên compact, clean, hiện đại).
  </anti_patterns>
</UI_UX_DESIGN_DNA>
```

---

## 🛠️ Chi Tiết Quy Chuẩn Thiết Kế Đã Được Nghiệm Thu

### 1. Hệ Màu Sắc & Vật Liệu (Colors & Materiality)
- **Nền chính (Background)**: Tối sâu tinh tế (`#0D1117`), bề mặt thẻ component (`#161B22`), hover state (`#21262D`).
- **Hiệu ứng kính mờ (Glassmorphism / Acrylic HUD)**:
  - Nền bán trong suốt: `rgba(22, 27, 34, 0.85)` kết hợp `backdrop-filter: blur(20px)`.
  - Đường viền tinh xảo siêu mảnh: `1px solid rgba(255, 255, 255, 0.08)`.
- **Điểm nhấn quang phổ (macOS Spectrum 7-Color)**:
  - Gradient 7 màu mềm mại: `linear-gradient(90deg, #FF5F56, #FFBD2E, #27C93F, #00C7BE, #007AFF, #5856D6, #AF52DE)`.
  - Sử dụng cho thanh tiến trình, đồng hồ đếm ngược, badge trạng thái quan trọng.

### 2. Hình Học & Bố Cục (Geometry & Layout)
- **Bo góc (Border Radius)**:
  - Container / Modal / Card lớn: `12px` đến `16px` (dáng Squircle mượt mà).
  - Chip / Tag / Pill Badge: `999px` (bo tròn hoàn toàn dạng con nhộng).
  - Nút bấm (Button): `8px` đến `10px`.
- **Tương phản & Khoảng cách (Spacing & Padding)**:
  - Ưu tiên layout **Compact & Clean**: Padding vừa vặn (`8px - 16px`), không tạo khoảng trắng mênh mông vô ích.
  - Phân cấp thông tin rõ ràng bằng độ đậm nhạt của chữ (600 cho tiêu đề, 400 cho nội dung, màu `#8B949E` cho phụ chú).

### 3. Tương Tác & Chuyển Động (Interaction & Micro-Motion)
- **Thời gian chuyển động (Duration)**: Siêu phản hồi trong khoảng `150ms – 250ms`.
- **Gia tốc (Easing)**: Đường cong mượt tự nhiên `cubic-bezier(0.16, 1, 0.3, 1)` (chuẩn Apple HIG).
- **Phản hồi xúc giác thị giác**: Khi hover nút có hiệu ứng sáng nhẹ hoặc nâng nhẹ `translateY(-1px) scale(1.01)`.

### 4. Thiết Luật Chống Lỗi Thẩm Mỹ (Anti-Patterns / What NOT to do)
1. **Tuyệt đối không dùng viền đen thô**: Viền luôn phải có độ trong suốt hoặc màu sáng nhẹ trên nền tối.
2. **Không che chữ đối chứng**: Mọi thông báo hay popup tương tác phải nằm ngoài luồng đọc hoặc tách nhịp (Two-Beat Decoupled), cấm che lấp văn bản người dùng đang rà soát.
3. **Không dùng màu rực gây mỏi mắt**: Màu accent phải được cân chỉnh độ bão hòa (saturation) vừa phải, dễ chịu khi làm việc ban đêm.

---

## 🔄 Cơ Chế Tự Tiến Hóa (Continuous Evolution)
- Khi hoàn thành một giao diện mới và người dùng bấm nghiệm thu `💎 [100% HOÀN TẤT] ✨`:
  - Nếu có sự thay đổi hoặc tinh chỉnh về gu (ví dụ: đổi tone màu, đổi kích thước nút), Agent Nghiệm Thu sẽ tự động trích xuất và cập nhật vào file này.
  - Lượt làm việc kế tiếp sẽ kế thừa trọn vẹn sự cải tiến đó!
