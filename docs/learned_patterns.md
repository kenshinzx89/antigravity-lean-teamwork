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

## Mẫu 3: [UI/Workflow] Dual-Modal Interactive Paradigm & Two-Beat Acceptance Gate (v1.4.2)
- **Nguyên nhân gốc**: Dùng GUI ngoài/HTML bị hệ thống chạy nền ẩn; dùng chung timeout làm trôi mất popup nghiệm thu; gọi modal che mất chữ báo cáo đối chứng thực tế.
- **Giải pháp tối thiểu**: Chuẩn hóa 2 modal đối lập trực quan qua `ask_question`:
  - 🧭 **Đề Xuất Kỹ Thuật**: Timeout 2.5 phút, tự động chọn `(Recommended)` nếu user vắng mặt để tránh đứt đoạn mạch làm việc.
  - 💎 **Nghiệm Thu Hoàn Thiện (Tách Nhịp 2 Bước)**: Bước 1 in toàn văn báo cáo phân tích ra màn hình, cấm mở modal che chữ. Bước 2 mới mở modal `💎 [NGHIỆM THU HOÀN THIỆN]` treo cố định (NO TIMEOUT) để chờ user đối chứng thực tế.
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

## Mẫu 7: [Meta-Learning] 6-Point Reflective Inquiry & Continuous Knowledge Pruning
- **Nguyên nhân gốc**: Thói quen "gặp lỗi đâu đẻ luật đấy" làm tập quy tắc phình to vô hạn, gây mâu thuẫn chỉ dẫn và quá tải nhận thức cho AI.
- **Giải pháp tối thiểu**: Áp dụng Bộ Khung Tự Vấn 6 Chiều sau mỗi phiên nghiệm thu:
  1. *Root Cause & Churn*: Tìm căn nguyên và phân tích số turn lãng phí.
  2. *First-Time Right*: Biện pháp đảm bảo thành công ngay Turn 1.
  3. *Token Economy*: Cắt giảm triệt để các thao tác lãng phí context.
  4. *Velocity & Automation*: Tự động hóa tối đa qua hook/scripts.
  5. *Rule Pruning & Anti-Bloat*: Gộp (Merge) và Tỉa (Prune) các quy tắc trùng lặp, giữ kho tri thức tối đa 10 patterns tinh hoa.
  6. *Meta-Questioning & Chronic Bottlenecks*: Tự vấn đệ quy về điểm nghẽn mãn tính và hành động xử lý dứt điểm.
- **Nguyên tắc cốt lõi**: Tuyệt đối không sửa/ghi vào `SKILL.md`; mọi tri thức tích lũy đều cách ly tại `learned_patterns.md`.

## Mẫu 8: [Client/Reverse] Gunbound Season 2 - Crash 0xc0000005 & Windowed Mode
- **Nguyên nhân gốc**: `GunBound.gme` đọc ngược 96 ký tự hex từ cuối command line; thừa ký tự làm lệch nibble hỏng AES decrypt gây crash heap. DirectDraw gọi `DDSCL_EXCLUSIVE` ép fullscreen gây lỗi hiển thị.
- **Giải pháp tối thiểu**: Chuẩn hóa chuỗi 96-hex AES (`encUser+encPass+encZero`); dùng wrapper proxy `ddraw.dll` (cnc-ddraw v7.1) ép `windowed=true` (800x600) giữ nguyên tỷ lệ, dọn sạch launcher rác.
- **Lệnh test**: Khởi chạy `GunBound.exe` -> Exit code 0, cửa sổ 800x600 hiển thị mượt mà.

## Mẫu 9: [Bot AI] Gunbound Season 2 - Virtual Player Presence & Lobby/Invite Simulation
- **Nguyên nhân gốc**: GameServer chỉ hiển thị người chơi ở Sảnh và danh sách Mời khi có socket TCP client đang online trong Channel; nạp DB đơn thuần chỉ lưu hồ sơ offline.
- **Giải pháp tối thiểu**: Nạp 12 hồ sơ Virtual Player phân cấp rõ rệt (Gà -> Rồng) vào bảng `user`/`game`/`buddylist`; chạy Virtual Client Worker kết nối TCP giữ hiện diện và tự động phản hồi Invite vào phòng thi đấu.
- **Kiểm chứng**: Danh sách người chơi sảnh hiển thị đầy đủ, nhận lời mời vào phòng thi đấu tức thì.

## Mẫu 10: [Inspection/Quota] Context-Aware Inspection vs Rigid Line-Count Anti-Pattern (Case Study Serene-Bose & Antigravity Widget)
- **Nguyên nhân gốc**: Ép buộc các con số đếm dòng cứng nhắc ("cấm đọc dưới 50 dòng", "bắt đọc 100–400 dòng") làm AI bị rối loạn biên độ đọc trong các session dài, gây kẹt lặp vô tận (như kẹt đọc 1 đoạn 15 dòng ở Widget). Ngược lại, việc chỉ đọc vài dòng chắp vá không nắm ngữ cảnh cũng làm đứt gãy mạch logic.
- **Giải pháp tối thiểu**: Loại bỏ hoàn toàn mọi ràng buộc đếm dòng cơ học. Áp dụng **Context-Aware Inspection**: Đọc linh hoạt theo trọn vẹn ngữ cảnh hàm/class/module cần thiết để hiểu rõ nguyên nhân gốc ngay từ lượt đầu (First-Time Right), tuyệt đối không đoán mò.
- **Lệnh test**: `py tests/test_skill_integrity.py` -> 10/10 PASS (Exit code 0).

## Mẫu 3: [UI/Workflow] Dual-Modal Interactive Paradigm & Persistent Side Panel
- **Nguyên nhân gốc**: Dùng GUI ngoài/HTML bị hệ thống chạy nền ẩn; dùng chung timeout làm trôi mất popup nghiệm thu khi người dùng chưa kịp đối chứng thực tế.
- **Giải pháp tối thiểu**: Chuẩn hóa 2 modal đối lập trực quan qua `ask_question`:
  - 🧭 **Đề Xuất Kỹ Thuật**: Timeout 2.5 phút, tự động chọn `(Recommended)` nếu user vắng mặt để tránh đứt đoạn mạch làm việc.
  - 💎 **Nghiệm Thu Hoàn Thiện**: Treo cố định vĩnh viễn (NO TIMEOUT) để bảo vệ quyền kiểm chứng tối thượng của người dùng.
  - Hiển thị kết quả bằng Markdown native trực tiếp trên Side Panel Antigravity; cách ly tri thức ra ngoài `SKILL.md`.
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

## Mẫu 1: Case Study Gunbound Season 2 - ACID & Inventory Desync
- **Nguyên nhân gốc**: Cơ chế cập nhật CSDL không gộp giao dịch (Transaction ACID), dẫn đến việc trừ tiền nhưng chưa kịp commit bản ghi item vào `item.chest`.
- **Mẫu sửa tối ưu**: Sử dụng Transaction Scope bao bọc toàn bộ khối cập nhật số dư ví và chèn rương đồ, rollback ngay lập tức nếu bất kỳ câu lệnh nào thất bại.
- **Bài học Token**: Sử dụng Gatekeeper chạy `Model: "flash"` kiểm thử độc lập giúp giảm hơn 70% token so với việc spawn hội đồng audit nhiều người.

## Mẫu 2: [UI/Workflow] Persistent Side Panel Gate & Knowledge Segregation
- **[UI/Workflow] [Persistent Side Panel & Knowledge Segregation]**:
  - *Nguyên nhân*: Dùng GUI ngoài / file HTML bị hệ thống chạy nền ẩn không hiển thị; nhồi nhét tri thức vào `SKILL.md` làm phình context token mỗi khi nạp agent.
  - *Giải pháp tối thiểu*: Dùng Artifact Markdown native hiển thị trực tiếp ở Side Panel Antigravity (khung chat bên trái tự do 100%); cách ly toàn bộ tri thức nghiệm thu ra file ngoài `learned_patterns.md` bằng Subagent `flash` sau khi người dùng xác nhận "OK".
  - *Lệnh test*: `py tests/test_skill_integrity.py` -> 6/6 PASS (Exit code 0).

## Mẫu 3: [Popup/Debugging] Two-State Autonomous Popup & Superpowers Systematic Debugging
- **[Popup/Debugging] [Two-State Popup & Superpowers Systematic Debugging]**:
  - *Nguyên nhân*: Menu popup phân mảnh options thừa thãi; sửa lỗi trực tiếp trên main agent làm phình context và hao phí quota token.
  - *Giải pháp tối thiểu*: Thu gọn popup đúng 2 trạng thái (`ask_question`); ủy quyền Subagent `flash` tự điều tra & sửa lỗi theo 4 pha Superpowers độc lập; cách ly tri thức ra `learned_patterns.md`.
  - *Lệnh test*: `py tests/test_skill_integrity.py` -> 6/6 PASS (Exit code 0).

## Mẫu 4: [Sync/Automation] Zero-Touch Two-Way Lifecycle Sync Giữa PC & Laptop
- **[Sync/Automation] [Zero-Touch Two-Way Lifecycle Sync Giữa PC & Laptop]**:
  - *Nguyên nhân*: Chuyển đổi qua lại giữa PC và Laptop dễ quên đồng bộ thủ công gây lệch phiên bản; quét toàn bộ repo làm phình context và lãng phí token.
  - *Giải pháp tối thiểu*: Zero-Touch PreInvocation Hook (`hooks.json`) tự động chạy ngầm; thuật toán Two-Way Adaptive Sync so sánh SemVer để tự PULL/PUSH và hợp nhất 2 chiều `learned_patterns.md`.
  - *Kiểm toán Quota & Barrier*: Zero-Scan tiết kiệm 100% token quét mã; Ratchet Barrier bảo đảm toàn vẹn 8/8 tests PASS (Exit code 0).

## Danh Mục Tri Thức Đã Đúc Kết

- **[Database] [Gunbound Season 2 - ACID / Inventory]**:
  - *Nguyên nhân*: Thiếu Transaction Scope khi vừa trừ tiền vừa ghi rương đồ.
  - *Giải pháp tối thiểu*: Gói trong 1 transaction duy nhất, rollback ngay nếu có lỗi. Lệnh test concurrency exit 0.
  - *Tiết kiệm Quota*: Gatekeeper `flash` độc lập giảm hơn 70% token so với hội đồng audit.

- **[Architecture] [Antigravity Custom Skill & Clean Global Rules]**:
  - *Nguyên nhân*: Nhúng quy tắc subagent phức tạp vào global rule làm đè và xung đột với `/teamwork-preview` gốc.
  - *Giải pháp tối thiểu*: Tách kiến trúc nâng cao ra thành Custom Skill độc lập (`lean-teamwork`), khôi phục `/teamwork-preview` về nguyên bản. Ở cấp toàn cục chỉ giữ `Daily Lean Workflow` siêu nhẹ.
  - *Tiết kiệm Quota*: Progressive disclosure — chỉ nạp chi tiết skill khi thực sự cần.

- **[Workflow] [Self-Evolution & Pattern Retrieval Loop]**:
  - *Nguyên nhân*: Kiến thức sau khi sửa lỗi không được tái sử dụng, dẫn đến điều tra lại từ đầu ở các phiên sau.
  - *Giải pháp tối thiểu*: Khép kín vòng lặp: Inspect First liếc nhanh `learned_patterns.md` -> Sửa minimal diff -> Xin xác nhận OK -> Tự động append 2-3 dòng.
  - *Tiết kiệm Quota*: Tiết kiệm 50-70% token cho các lỗi lặp lại.

- **[Client/Reverse] [Gunbound Season 2 - Crash 0xc0000005 & Windowed Mode]**:
  - *Nguyên nhân*: `GunBound.gme` đọc ngược 96 ký tự hex từ cuối command line; thừa ký tự làm lệch nibble hỏng AES decrypt gây crash heap. DirectDraw gọi `DDSCL_EXCLUSIVE` ép fullscreen.
  - *Giải pháp tối thiểu*: Chuẩn hóa chuỗi 96-hex AES (`encUser+encPass+encZero`); dùng wrapper proxy `ddraw.dll` (cnc-ddraw v7.1) ép `windowed=true` (800x600) giữ nguyên tỷ lệ, dọn sạch launcher rác.
  - *Lệnh test*: Khởi chạy `GunBound.exe` -> Exit code 0, cửa sổ 800x600 hiển thị mượt mà.

- **[Bot AI] [Gunbound Season 2 - Virtual Player Presence & Lobby/Invite]**:
  - *Nguyên nhân*: GameServer chỉ hiển thị người chơi ở Sảnh và danh sách Mời khi có socket TCP client đang online trong Channel; nạp DB đơn thuần chỉ lưu hồ sơ offline.
  - *Giải pháp tối thiểu*: Nạp 12 hồ sơ Virtual Player phân cấp rõ rệt (Gà -> Rồng) vào bảng `user`/`game`/`buddylist`; chạy Virtual Client Worker kết nối TCP giữ hiện diện và tự động phản hồi Invite vào phòng thi đấu.

- **[Teamwork/Workflow] [Ambiguity & Decision Checkpoints - Ask First, Suggest Options]**:
  - *Nguyên nhân*: Khi gặp ngã rẽ kiến trúc (Server vs Client, cấu hình vs code mới) hoặc yêu cầu còn mơ hồ, agent tự phỏng đoán làm lan man gây sai lệch ý đồ người dùng và lãng phí token.
  - *Giải pháp tối thiểu*: Bắt buộc dừng lại, dùng `ask_question` gợi ý các phương án cụ thể (ưu/nhược điểm, phương án đề xuất `Recommended`) để người dùng chọn trước khi bắt tay thực hiện.
  - *Tiết kiệm Quota*: Tránh 100% việc viết code mò mẫm, sửa nhầm hướng và phải hoàn tác tốn kém.

- **[UI/Workflow] [Persistent Side Panel & Knowledge Segregation]**:
  - *Nguyên nhân*: Cố tạo GUI ngoài / file HTML bị hệ thống chạy nền ẩn không hiển thị; nhồi nhét tri thức vào `SKILL.md` làm phình context token mỗi phiên.
  - *Giải pháp tối thiểu*: Dùng Artifact Markdown native hiển thị trực tiếp ở Side Panel Antigravity (khung chat tự do); cách ly toàn bộ tri thức nghiệm thu ra file ngoài `learned_patterns.md` qua Subagent `flash`.
  - *Lệnh test*: `py tests/test_skill_integrity.py` -> 6/6 PASS (Exit code 0).

- **[Popup/Debugging] [Two-State Popup & Superpowers Systematic Debugging]**:
  - *Nguyên nhân*: Menu popup phân mảnh options thừa thãi; sửa lỗi trực tiếp trên main agent làm phình context và hao phí quota token.
  - *Giải pháp tối thiểu*: Thu gọn popup đúng 2 trạng thái (`ask_question`); ủy quyền Subagent `flash` tự điều tra & sửa lỗi theo 4 pha Superpowers độc lập; cách ly tri thức ra `learned_patterns.md`.
  - *Lệnh test*: `py tests/test_skill_integrity.py` -> 6/6 PASS (Exit code 0).

- **[Anti-Pattern] [Blind Lean & Trajectory Churn]**: Ngại đọc tài liệu Turn 1 dẫn đến đoán mò, gây ra chuỗi 5-10 lượt chat sửa sai lặp lại -> Bắt buộc First-Time Right Protocol (Inspect First đọc sâu tài liệu/code ngay Turn 1) -> `py tests/test_skill_integrity.py` (Exit code 0)
- **[Anti-Pattern] [Survivorship Bias in Evaluation]**: Đúc kết chỉ nhìn vào Git Diff thành công cuối cùng mà mù trước chuỗi thất bại -> Trajectory Churn Audit kiểm toán toàn bộ lịch sử turn và tỷ lệ First-Time Right -> `py tests/test_skill_integrity.py` (Exit code 0)
- **[Protocol] [First-Time Right & Anti-Churn]**: Thiếu cơ chế kiểm soát chất lượng từ đầu gây lãng phí quota -> Phân tích nguyên nhân gốc + kiểm toán vết thực thi (trajectory audit) trước khi chốt nghiệm thu -> `py tests/test_skill_integrity.py` (Exit code 0)
- **[Gate/Quota] [Global Clarification Gate & Zero-Guesswork]**: Không phỏng vấn làm rõ khi gặp ngã rẽ kỹ thuật dẫn đến phỏng đoán mò mẫm hao phí quota -> Kích hoạt Clarification Gate qua `ask_question` (kèm timeout 2.5m Best-Path Fallback) trong GEMINI.md toàn cục -> `py tests/test_skill_integrity.py` (Exit code 0)
- **[UI/UX] [Premium 2-State Popup Identity]**: Menu nghiệm thu đơn điệu, thiếu phân định trực quan giữa chốt phiên và debug -> Chuẩn hóa bộ nhận diện icon cao cấp tương phản (`💎 ✨` Hoàn tất vs `⚡ 🛠️` Superpowers Debug) trên modal `ask_question` -> `py tests/test_skill_integrity.py` (Exit code 0)

## Mẫu 10: [Inspection/Quota] Cohesive Block Inspection vs Micro-Peeking Anti-Pattern (Case Study Serene-Bose)
- **Nguyên nhân gốc**: Hiểu sai tính "Lean" dẫn tới tật đọc vụn vặt 50 dòng (`Micro-Peeking`). Cắt đứt ngữ cảnh của hàm/class làm AI phải grep đi grep lại hơn 30 tool calls chắp vá, gây tốn token gấp 5 lần và người dùng rất ức chế.
- **Giải pháp tối thiểu**: Thiết lập nguyên tắc **Cohesive Block Inspection** — Đọc trọn vẹn 100–400 dòng của hàm/class liên quan trong **1 lần gọi `view_file` duy nhất**. CẤM chuỗi thao tác lặp: grep -> đọc 50 dòng -> grep lại trong cùng file. Đọc trọn vẹn ngữ cảnh ngay Turn 1 giúp làm đúng ngay lần đầu (First-Time Right) trong 1 diff duy nhất.
- **Lệnh test**: `py tests/test_skill_integrity.py` -> 10/10 PASS (Exit code 0).

## Mẫu 11: [UI/UX & Architecture] Desktop Widget HUD Decoupled & Chat Freedom (Lean Teamwork v1.5.0)
- **[UI/UX & Architecture] [Desktop Widget HUD Decoupled & Chat Freedom]**:
  - *Nguyên nhân gốc*: Modal popup cũ (ask_question) là lệnh chặn cứng (hard-blocking) chiếm trọn khung chat, che mất nội dung phân tích/code và đóng băng tiến trình AI, làm người dùng rất vướng víu và ức chế.
  - *Giải pháp tối thiểu*: Chuyển hướng 100% Đề xuất Kỹ thuật (🧭) và Bảng Nghiệm Thu (💎) ra ngoài Desktop Widget Popover HUD qua IPC Bridge (teamwork_bridge.py). Khung chat rảnh rang tuyệt đối, chỉ hiển thị báo cáo sạch sẽ. Tương tác 1 chạm trực tiếp từ Desktop Widget tự động focus và gửi lệnh phím xuống IDE.
  - *Khắc phục hiển thị*: Popover tự động co giãn (compute_dynamic_layout), word-wrap toàn diện cho tiêu đề, tự thích ứng vùng làm việc SPI_GETWORKAREA (trừ taskbar) chống cắt cụt nút bấm và mất chữ.
  - *Lệnh test*: py tests/test_skill_integrity.py -> 11/11 PASS (Exit code 0).

## Mẫu 12: [Architecture & Onboarding] Dual Account Detection, Zero-Pip Portability & From-Last-Completion Retrospective Anchor (v1.5.1)
- **[Architecture & Onboarding] [Dual Account Detection, Zero-Pip Portability & From-Last-Completion Retrospective Anchor]**:
  - *Nguyên nhân gốc*:
    1. Khi tải repo sang máy tính mới chưa cài Cockpit Tool, Widget bị lỗi hiển thị `Offline` / `No Acc` do thiếu cơ chế kết nối trực tiếp tài khoản Google trong Antigravity IDE.
    2. Khi người dùng gặp lỗi tiếp tục chat mà chưa ấn Hoàn tất, nếu agent chỉ nhìn vào lượt cuối cùng sẽ mắc bẫy *Survivorship Bias*, bỏ sót toàn bộ chuỗi lỗi trung gian chưa được rút kinh nghiệm.
    3. Việc chứa đường dẫn tuyệt đối cứng (`C:\Users\tient...`) hoặc yêu cầu cài thêm thư viện qua pip khiến máy mới không thể chạy ngay lập tức.
  - *Giải pháp tối thiểu*:
    1. **Dual Account Detection**: Trích xuất trực tiếp tài khoản Google đang đăng nhập từ SQLite native của Antigravity IDE (`%APPDATA%\Antigravity IDE\User\globalStorage\state.vscdb`) làm fallback khi máy mới chưa có Cockpit Tool, hiển thị đầy đủ tên, email và trạng thái hoạt động 100%.
    2. **From-Last-Completion Retrospective Anchor**: Lưu mốc thời gian `last_completed_at` trong `teamwork_bridge.py` và `teamwork_service.py`. Khi thực hiện đúc kết bài học (Self-Evolution), bắt buộc rà soát và tổng hợp toàn bộ các lỗi trung gian phát sinh từ lần bấm Hoàn tất gần nhất đến nay.
    3. **Zero-Pip Portability & 1-Click Zero-Scan**: Toàn bộ hệ sinh thái chạy 100% trên Python Standard Library (`ctypes` GDI+, `sqlite3`, `json`), khử hoàn toàn đường dẫn cứng. Tích hợp chỉ dẫn `AGENTS.md` / `GEMINI.md` để AI trên máy mới chỉ cần chạy DUY NHẤT 1 lệnh `install.ps1` là đạt Full Parity ngay lập tức không tốn token quét mã.
  - *Lệnh test*: `py -m unittest discover -s tests` -> 18/18 PASS (Exit code 0).

## Mẫu 13: [Protocol & UI] Acceptance Passcode ("OK 💎") & Anti-False-Acceptance Guard (v1.5.2)
- **[Protocol & UI] [Acceptance Passcode ("OK 💎") & Anti-False-Acceptance Guard]**:
  - *Nguyên nhân gốc*: Sử dụng chuỗi nghiệm thu "OK" trơn quá đơn giản và thông dụng trong văn phong trò chuyện hàng ngày. Khi người dùng trao đổi ("ok bạn", "ok làm tiếp đi", "ok để mình xem"...), AI rất dễ phán đoán sai là người dùng đã nghiệm thu chấp thuận và vội vàng đóng phiên đúc kết tri thức.
  - *Giải pháp tối thiểu*:
    1. **Chuẩn Hóa Mật Mã Nghiệm Thu (`OK 💎`)**: Desktop Widget HUD Popover khi người dùng bấm `[💎 100% HOÀN TẤT]` tự động gõ gửi chuỗi mật mã `OK 💎` xuống Antigravity IDE thông qua Win32 `KEYEVENTF_UNICODE` (hỗ trợ đầy đủ UTF-16 surrogate pairs cho emoji).
    2. **Anti-False-Acceptance Guard (`is_acceptance_signal`)**: Main Agent loại trừ 100% các từ "ok" giao tiếp tự nhiên nếu không đi kèm emoji kim cương 💎 hoặc không khớp đúng mật mã `OK 💎`. Chỉ khi nhận diện đúng mật mã `OK 💎` (hoặc `💎 OK`, `[ACCEPT] 💎`), AI mới kích hoạt chu trình Self-Evolution và hoàn tất task.
  - *Lệnh test*: `py -m unittest discover -s tests` -> 19/19 PASS (Exit code 0).
