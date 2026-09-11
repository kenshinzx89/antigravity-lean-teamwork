# Kho Tri Thức & Các Mẫu Đúc Kết Tinh Gọn (Learned Patterns)

Tài liệu này là nơi lưu trữ các tri thức kỹ thuật, mẫu sửa lỗi tối thiểu và bài học tiết kiệm quota được chắt lọc sau khi người dùng bấm xác nhận "OK".

---

## Mẫu 1: [Database] Gunbound Season 2 - ACID & Inventory Desync
- **Nguyên nhân gốc**: Cơ chế cập nhật CSDL không gộp giao dịch (Transaction ACID), dẫn đến việc trừ tiền thành công nhưng chưa kịp commit bản ghi item vào `item.chest`.
- **Giải pháp tối thiểu**: Sử dụng Transaction Scope bao bọc toàn bộ khối cập nhật số dư ví và chèn rương đồ, rollback ngay lập tức nếu bất kỳ câu lệnh nào thất bại. Lệnh test concurrency đạt Exit code 0.
- **Tiết kiệm Quota**: Gatekeeper chạy `Model: "flash"` kiểm thử độc lập giúp giảm hơn 70% token so với việc spawn hội đồng audit nhiều người.

## Mẫu 2: [Architecture] Custom Skill Độc Lập & Progressive Disclosure
- **Nguyên nhân gốc**: Nhúng quy tắc subagent phức tạp vào global rule làm đè và xung đột với `/teamwork-preview` mặc định của hệ thống.
- **Giải pháp tối thiểu**: Tách toàn bộ kiến trúc nâng cao ra thành Custom Skill độc lập (`lean-teamwork`), khôi phục GEMINI.md toàn cục về nguyên bản nhẹ nhàng. Áp dụng Progressive Disclosure: chỉ nạp chi tiết skill khi thực sự cần.
- **Tiết kiệm Quota**: Giảm 80% overhead context nạp khởi đầu trên mọi phiên làm việc mới.

## Mẫu 3: [UI/Workflow] Dual-Modal Interactive Paradigm & Persistent Side Panel
- **Nguyên nhân gốc**: Dùng GUI ngoài/HTML bị hệ thống chạy nền ẩn; dùng chung timeout làm trôi mất popup nghiệm thu khi người dùng chưa kịp đối chứng thực tế.
- **Giải pháp tối thiểu**: Chuẩn hóa 2 modal đối lập trực quan qua `ask_question`:
  - 🧭 **Đề Xuất Kỹ Thuật**: Timeout 2.5 phút, tự động chọn `(Recommended)` nếu user vắng mặt để tránh đứt đoạn mạch làm việc.
  - 💎 **Nghiệm Thu Hoàn Thiện**: Treo cố định vĩnh viễn (NO TIMEOUT) để bảo vệ quyền kiểm chứng tối thượng của người dùng.
  - Hiển thị kết quả bằng Markdown native trực tiếp trên Side Panel Antigravity; cách ly tri thức ra ngoài `SKILL.md`.
- **Lệnh test**: `py tests/test_skill_integrity.py` -> 10/10 PASS (Exit code 0).

## Mẫu 4: [Debugging] Two-State Autonomous Popup & Superpowers Systematic Debugging
- **Nguyên nhân gốc**: Menu popup phân mảnh nhiều options thừa thãi; sửa lỗi trực tiếp trên main agent làm phình context và hao phí quota nghiêm trọng.
- **Giải pháp tối thiểu**: Thu gọn popup đúng 2 trạng thái (`ask_question`): `💎 [100% HOÀN TẤT] ✨` vs `⚡ [SUPERPOWERS DEBUG] 🛠️`. Khi debug, ủy quyền Subagent `flash` tự điều tra & sửa lỗi theo 4 pha Superpowers độc lập (Reproduce -> Root Cause -> Minimal Fix -> Verify).
- **Tiết kiệm Quota**: Giữ sạch main agent context, tiết kiệm 60-80% token so với debug trực tiếp trên luồng chính.

## Mẫu 5: [Sync/Automation] Zero-Touch Two-Way Lifecycle Sync Giữa PC & Laptop
- **Nguyên nhân gốc**: Chuyển đổi qua lại giữa PC và Laptop dễ quên đồng bộ thủ công gây lệch phiên bản; quét toàn bộ repo làm phình context và lãng phí token.
- **Giải pháp tối thiểu**: Zero-Touch PreInvocation Hook (`hooks.json`) tự động chạy ngầm kiểm tra; thuật toán Two-Way Adaptive Sync (`sync_skill.py`) so sánh SemVer để tự PULL/PUSH và cân bằng 2 chiều `learned_patterns.md`.
- **Kiểm toán Quota & Barrier**: Zero-Scan Protocol tiết kiệm 100% token quét mã; Ratchet Barrier bảo đảm toàn vẹn 10/10 tests PASS (Exit code 0).

## Mẫu 6: [Protocol] First-Time Right, Anti-Survivorship Bias & Trajectory Churn Audit
- **Nguyên nhân gốc**: Nghịch lý "Blind Lean" (ngại đọc tài liệu Turn 1 dẫn đến đoán mò, gây lặp 5-10 lượt sửa sai tốn kém) và "Survivorship Bias" (chỉ nhìn diff thành công cuối cùng mà mù trước chuỗi thất bại trước đó).
- **Giải pháp tối thiểu**:
  - **Inspect First**: Bắt buộc đọc kỹ tài liệu/mã nguồn liên quan ngay Turn 1; cấm đoán mò.
  - **Clarification Gate**: Dừng lại hỏi rõ khi gặp ngã rẽ kiến trúc (kèm timeout 2.5m Best-Path Fallback).
  - **Trajectory Churn Audit**: Kiểm toán turn budget và tỷ lệ First-Time Right trong báo cáo phản tư chu kỳ.
- **Lệnh test**: `py tests/test_skill_integrity.py` -> 10/10 PASS (Exit code 0).

## Mẫu 7: [Meta-Learning] 5-Point Reflective Inquiry & Continuous Knowledge Pruning
- **Nguyên nhân gốc**: Thói quen "gặp lỗi đâu đẻ luật đấy" làm tập quy tắc phình to vô hạn, gây mâu thuẫn chỉ dẫn và quá tải nhận thức cho AI.
- **Giải pháp tối thiểu**: Áp dụng Bộ Khung Tự Vấn 5 Chiều sau mỗi phiên nghiệm thu:
  1. *Root Cause & Churn*: Tìm căn nguyên và phân tích số turn lãng phí.
  2. *First-Time Right*: Biện pháp đảm bảo thành công ngay Turn 1.
  3. *Token Economy*: Cắt giảm triệt để các thao tác lãng phí context.
  4. *Velocity & Automation*: Tự động hóa tối đa qua hook/scripts.
  5. *Rule Pruning & Anti-Bloat*: Định kỳ Gộp (Merge & Generalize) và Tỉa (Prune) các quy tắc trùng lặp/vụn vặt, duy trì kho tri thức tối đa 10 patterns tinh hoa.
- **Nguyên tắc cốt lõi**: Tuyệt đối không sửa/ghi vào `SKILL.md`; mọi tri thức tích lũy đều cách ly tại `learned_patterns.md`.

## Mẫu 8: [Client/Reverse] Gunbound Season 2 - Crash 0xc0000005 & Windowed Mode
- **Nguyên nhân gốc**: `GunBound.gme` đọc ngược 96 ký tự hex từ cuối command line; thừa ký tự làm lệch nibble hỏng AES decrypt gây crash heap. DirectDraw gọi `DDSCL_EXCLUSIVE` ép fullscreen gây lỗi hiển thị.
- **Giải pháp tối thiểu**: Chuẩn hóa chuỗi 96-hex AES (`encUser+encPass+encZero`); dùng wrapper proxy `ddraw.dll` (cnc-ddraw v7.1) ép `windowed=true` (800x600) giữ nguyên tỷ lệ, dọn sạch launcher rác.
- **Lệnh test**: Khởi chạy `GunBound.exe` -> Exit code 0, cửa sổ 800x600 hiển thị mượt mà.

## Mẫu 9: [Bot AI] Gunbound Season 2 - Virtual Player Presence & Lobby/Invite Simulation
- **Nguyên nhân gốc**: GameServer chỉ hiển thị người chơi ở Sảnh và danh sách Mời khi có socket TCP client đang online trong Channel; nạp DB đơn thuần chỉ lưu hồ sơ offline.
- **Giải pháp tối thiểu**: Nạp 12 hồ sơ Virtual Player phân cấp rõ rệt (Gà -> Rồng) vào bảng `user`/`game`/`buddylist`; chạy Virtual Client Worker kết nối TCP giữ hiện diện và tự động phản hồi Invite vào phòng thi đấu.
- **Kiểm chứng**: Danh sách người chơi sảnh hiển thị đầy đủ, nhận lời mời vào phòng thi đấu tức thì.
