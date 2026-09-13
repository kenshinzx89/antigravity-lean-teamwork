# 📜 Changelog — Lean Teamwork Protocol

Tất cả các thay đổi, bài học và tính năng nâng cấp qua từng phiên bản.

---

## [1.5.7] — 2026-09-13
### Added
- **Tinh Gọn Đề Xuất Kỹ Thuật (Zero-Token IDE Proposals) & Độc Quyền Đếm Ngược Trên Widget HUD**:
  - Loại bỏ hoàn toàn ảnh SVG đồng hồ đếm ngược trong khung chat IDE để tiết kiệm 100% Token và Quota.
  - Chuyển giao toàn bộ giao diện đồng hồ đếm ngược 150s thời gian thực sang Desktop Widget HUD Popover.
- **Chuẩn Hóa Biên Giới Hiển Thị Full vs Thu Gọn**:
  - Khi Antigravity IDE đang mở trên màn hình: Widget **LUÔN HIỂN THỊ FULL 100% (587px - 636px)**, không bao giờ bị co lại bất thường khi có đề xuất hoặc khi tương tác.
  - Thu nhỏ về viên pill compact (~67px) **CHỈ ÁP DỤNG** khi Antigravity IDE bị Minimize xuống taskbar hoặc hoàn toàn không chạy, giúp giải phóng màn hình Desktop tối đa.
- **Tối Ưu Hóa Video Demo Nhúng README.md (97.2% Compression)**:
  - Video quay màn hình 2.5K Retina 52s (131.7 MB) được nén chuẩn H.264 1080p xuống còn **3.65 MB**, nhúng trực tiếp thay thế banner/logo trên đầu `README.md`, hiển thị sắc nét và mượt mà trên GitHub.

## [1.5.6] — 2026-09-13
### Added
- **Nhận Biết Cửa Sổ Hoạt Động (Foreground Awareness) & Tự Động Thu Gọn Khi Chuyển App**:
  - Khắc phục triệt để trường hợp người dùng click chuyển sang ứng dụng khác (Telegram, Chrome, Notepad...) hoặc mở Desktop nhưng Widget vẫn hiển thị thanh dài 636px.
  - Tích hợp kiểm tra `GetForegroundWindow()` đối chiếu với PID của Antigravity IDE, đồng thời lắng nghe chuột `mouse_over` trên Widget.
  - Khi người dùng ở app khác hoặc minimize IDE: Widget tự động co lại thành duy nhất viên pill Nghiệm thu siêu nhỏ (**115px**), không còn chiếm diện tích màn hình.
  - Khi người dùng click lại vào Antigravity IDE hoặc hover chuột vào viên pill: Widget tự động bung to đầy đủ tất cả các chip Quota, Context, Account và dock bám dính chính xác.
- **Đồng Bộ Hai Chiều Tự Động Với Thư Mục Desktop (`Desktop\Du An\CockpitQuotaWidget`)**:
  - `sync_skill.py` tự động phát hiện và đồng bộ song song mã nguồn Widget sang thư mục Desktop của người dùng, đảm bảo dù người dùng khởi động từ shortcut nào cũng luôn nhận phiên bản mới nhất 100%.

## [1.5.5] — 2026-09-13
### Added
- **Tự Động Thu Gọn Về Duy Nhất Chip Nghiệm Thu Khi Không Có Antigravity (Compact Teamwork Chip Mode)**:
  - Khi không có Antigravity IDE (hoặc khi IDE bị minimize), thanh Widget HUD tự động co lại kích thước (~160px), **CHỈ HIỆN DUY NHẤT CHIP TEAMWORK (Nghiệm thu / Đề xuất)**.
  - Toàn bộ các chip khác (Account, 5H, Weekly, Switch, Refresh, Lock) được tự động ẩn đi, giải phóng không gian màn hình Desktop tối đa, tránh gây vướng tầm nhìn và chống click nhầm.
  - Khi người dùng mở lại Antigravity IDE, Widget tự động bung to trở lại đầy đủ tất cả các chip và gắn vào cửa sổ IDE như bình thường.

## [1.5.4] — 2026-09-13
### Added
- **Tự Động Thu Gọn Widget Khi Minimize Antigravity IDE (Auto-Collapse & Standalone Alerts)**:
  - **Auto-Collapse**: Khi Antigravity IDE bị minimize xuống taskbar, thanh Widget HUD chính tự động ẩn đi (`SW_HIDE`), giải phóng hoàn toàn không gian màn hình Desktop, chống click nhầm và chống xung đột cửa sổ. Khi người dùng mở lại IDE, Widget tự động hiển thị lại (`SW_SHOWNA`) và gắn vào góc IDE như bình thường.
  - **Chỉ Mở Cửa Sổ Nghiệm Thu / Đề Xuất Khi Có Thông Báo**: Nếu trong lúc IDE đang minimize mà có đề xuất (`PROPOSAL`) hoặc nghiệm thu (`ACCEPTANCE`) mới tới, Popover thông báo vẫn tự động bung lên độc lập ở góc trên bên phải màn hình desktop để người dùng theo dõi và duyệt kịp thời. Sau khi tương tác hoặc hết giờ, Popover tự ẩn.

## [1.5.3] — 2026-09-13
### Added
- **Đề Xuất Kỹ Thuật 2 Lối Song Hành (Dual-Track Proposals) & Tự Động Trả Về [1] Khi Hết Giờ**:
  - **Lối 1 (Khung Chat Antigravity)**: In trực tiếp danh sách phương án ra chat kèm `[1] (Recommended) ⭐`, đồng thời gọi công cụ `schedule` (150s, `TimerCondition: "any"`) làm fallback tự động đánh thức AI chọn phương án 1 nếu người dùng rời máy.
  - **Lối 2 (Desktop Widget HUD Popover)**: Khắc phục triệt để hiện tượng Widget không bung Popover ở các turn đề xuất liên tiếp bằng cơ chế nhận diện timestamp (`updated_at > last_tw_updated_at`), giữ Popover mở suốt thời gian đếm ngược (`deadline_ts + 5.0s`).
  - **Tự động trả về phím '1' khi hết 150s**: Khi đồng hồ đếm ngược trên Widget về `00:00` mà người dùng chưa bấm chọn gì, Widget sẽ tự động focus và gửi phím `1` về Antigravity IDE cho gọn, tự động đóng Popover sau khi hoàn tất.

## [1.5.2] — 2026-09-13
### Added
- **Chuẩn Hóa Mật Mã Nghiệm Thu (`OK 💎`) & Anti-False-Acceptance Guard**:
  - Tách bạch hoàn toàn giữa trao đổi thông thường và tín hiệu nghiệm thu chính thức, chống nhầm lẫn các từ "ok" trong giao tiếp hàng ngày.

## [1.5.1] — 2026-09-13
### Added
- **Quy Tắc Biên Độ Tổng Hợp Từ Lần Hoàn Tất Gần Nhất (From-Last-Completion Retrospective Anchor)**:
  - Khi trong một phiên làm việc người dùng chưa bấm Hoàn tất vì còn lỗi và tiếp tục trao đổi qua nhiều lượt chat trung gian:
  - Đến khi người dùng bấm `💎 [100% HOÀN TẤT] ✨`, việc đúc kết tri thức (Self-Evolution / Retrospective) **BẮT BUỘC rà soát toàn bộ chuỗi lỗi, các giả định sai và các lần sửa TỪ LẦN BẤM HOÀN TẤT GẦN NHẤT ĐẾN NAY**.
  - **Zero Error Dropping**: Tuyệt đối không được bỏ sót bất kỳ lỗi trung gian nào phát sinh giữa 2 mốc hoàn tất; cấm chỉ nhìn vào git diff cuối cùng hay lượt chat chót.
  - **Cơ chế lưu mốc trong Bridge SDK**: Bổ sung `last_completed_at`, `completion_history`, `record_intermediate_issue()` và `get_intermediate_issues()` vào `teamwork_bridge.py` và `teamwork_service.py` để ghi nhớ mốc thời gian chính xác cho việc rà soát `transcript.jsonl`.
- **Dual Account Detection (Native IDE Fallback)**:
  - Widget tự động kết nối trực tiếp với tài khoản Google Antigravity IDE cục bộ (`state.vscdb`) khi máy mới không cài Cockpit Tool, loại bỏ hoàn toàn lỗi `Offline` / `No Acc`.

## [1.5.0] — 2026-09-13
### Added
- **Gộp Dự Án Monorepo (Lean Teamwork + Desktop Widget HUD)**:
  - Hợp nhất toàn diện mã nguồn Desktop Widget vào monorepo tại `widget/`.
  - Bổ sung `install.ps1` và `INSTALL.md` cho máy mới trong 5 giây.
  - Tách nhịp nghiệm thu độc lập ra Widget Popover HUD, giải phóng 100% khung chat.

## [1.4.7] — 2026-09-13
### Changed
- **Chuyển Đề Xuất Kỹ Thuật (🧭) Sang Chat Stream + Timer Ngầm `schedule` (Non-Blocking Autonomous Fallback)**:
  - Khắc phục triệt để điểm nghẽn nghiêm trọng: Pop-up modal `ask_question` là lệnh chặn cứng (hard-blocking), khiến IDE đóng băng tiến trình AI, làm timer không thể đánh thức và gây đứt đoạn công việc khi người dùng rời máy.
  - Chuyển `🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡` sang in trực tiếp ra khung chat kèm danh sách lựa chọn số `[1] (Recommended)`, `[2]`, ... và kích hoạt `schedule(150s, TimerCondition: "any")`.
  - Nếu người dùng có mặt: Gõ số chọn trực tiếp (timer tự hủy ngay lập tức).
  - Nếu vắng mặt quá 2.5 phút: AI tự động thức dậy, kích hoạt phương án `(Recommended)` và tiếp tục thực thi không để đứt đoạn mạch công việc.
- **Bảo Toàn Pop-up Modal `ask_question` Cho Nghiệm Thu Hoàn Thiện (💎)**:
  - Giữ nguyên Pop-up Modal `ask_question` 2 trạng thái (`100% HOÀN TẤT` vs `SUPERPOWERS DEBUG`) ở chế độ treo cố định (không timeout) theo quy trình Tách Nhịp 2 Bước v1.4.2 để bảo đảm đối chứng thực tế khách quan trước khi khóa tri thức.
- **Loại Bỏ Ràng Buộc Nhúng SVG Đếm Ngược Lỗi Thời**:
  - Gỡ bỏ thẻ ảnh SVG trong tiêu đề modal vốn bị Chromium CSP chặn render và gây vỡ đường dẫn khi đổi conversation ID/máy tính.

## [1.4.6] — 2026-09-12
### Changed
- **Gỡ Bỏ Ràng Buộc Đếm Dòng Cơ Học (Eliminate Rigid Line-Count Constraints)**: Loại bỏ triệt để các con số đếm dòng cứng nhắc ("cấm đọc dưới 50 dòng", "bắt buộc đọc 100–400 dòng") vốn gây rối loạn biên độ đọc trong các session dài (như hiện tượng kẹt lặp đọc 15 dòng ở Antigravity Widget).
- **Chuẩn Hóa Nguyên Tắc Context-Aware Inspection & First-Time Right**: Thay thế đếm dòng cơ học bằng việc đọc linh hoạt trọn vẹn ngữ cảnh hàm/class/module cần thiết để nắm bắt nguyên nhân gốc ngay từ đầu và làm chuẩn ngay lần đầu, không đoán mò vì sợ đọc code hay tài liệu.
- **Duy Trì Toàn Vẹn 100% Các Tính Năng Đột Phá**: Bảo tồn nguyên vẹn Đồng hồ đếm ngược đồ họa 7 màu macOS Spectrum (`technical_proposal_timer.svg`) và Cổng nghiệm thu tách nhịp 2 bước (`Two-Beat Acceptance Gate`).

## [1.4.5] — 2026-09-12
### Added
- **Gắn Chặt Lean Teamwork Mặc Định Vào IDE Antigravity (Builtin Core Integration)**: Đăng ký Lean Teamwork trực tiếp vào `~/.gemini/antigravity/builtin/skills/` thành Builtin Skill chính thức của IDE.
- **Nâng Cấp Thiết Luật Toàn Cục Tối Cao**: Đồng bộ cả 3 file `GEMINI.md` của Antigravity, đưa Lean Teamwork Gate (`🧭 [ĐỀ XUẤT KỸ THUẬT]` & `💎 [NGHIỆM THU HOÀN THIỆN]`) thành Thiết luật bắt buộc mặc định trên mọi workspace.
- **Tính Năng Cài Đặt Vào Dự Án Nhanh (`--install-to <path>`)**: Hỗ trợ trang bị trọn gói Lean Teamwork vào bất kỳ dự án nào trên máy chỉ với 1 lệnh terminal.
- **Trang Bị Trực Tiếp Cho Dự Án `AntigravityWidget`**: Cài đặt hoàn chỉnh skill, tài nguyên SVG và controllers vào thư mục `AntigravityWidget`.

## [1.4.4] — 2026-09-12
### Added
- **Cơ Chế Tương Thích Tuyệt Đối Mọi Máy Tính (Universal Multi-Machine Parity)**: Khắc phục lỗi hook ngầm chỉ chạy được trong repo mà chết ở các project khác (như antigravity-widget).
- **Khử Phụ Thuộc PATH Bằng Dynamic `sys.executable`**: Tự động phát hiện đường dẫn thực thi tuyệt đối của Python trên từng máy (`"{sys.executable}" "{hook_script}"`), giúp hook chạy mượt mà ngay cả khi Windows chưa tích chọn "Add Python to PATH".
- **Khóa Kiểm Thử Đa Thư Mục (Multi-CWD Barrier)**: Thêm assertion vào `tests/test_skill_integrity.py` kiểm tra hook từ thư mục ngoài repo đạt 100% exit code 0.
- **Neo Chặt Vào Global `GEMINI.md`**: Đảm bảo Lean Teamwork luôn được Antigravity nhận diện trên mọi workspace mà không lo bị kẹt trong giới hạn 303 skills.

## [1.4.3] — 2026-09-12
### Added
- **Đồng Hồ Đồ Họa Đếm Ngược Động Trực Tiếp Trên Popup (Live Countdown SVG)**: Tích hợp đồ họa `technical_proposal_timer.svg` trực tiếp vào modal `ask_question` với phong cách 7 màu chuyển sắc nhẹ nhàng macOS Spectrum, số SF Mono lùi từng giây thực tế (`02:30 -> 00:00`) và thanh progress capsule mượt mà.
- **Tiêu Đề Chuẩn Nhận Diện Lean Teamwork**: Chốt tiêu đề `🧭 ĐỀ XUẤT KỸ THUẬT 💡` và mô tả hành động `Tự động chọn [Recommended] sau:`.
- **Cơ Chế Pause Ô 3 Thông Minh**: Tự động coi đồng hồ như đã tạm dừng khi người dùng bấm/nhập ô số 3 (ý kiến riêng), đảm bảo AI không bao giờ tự ý chọn phương án Recommended.

## [1.4.2] — 2026-09-12
### Added
- **Khai Tử Bệnh "Đọc Vụn Nhòm Khe 50 Dòng" (Micro-Peeking Anti-Pattern)**: Rút kinh nghiệm sâu sắc từ thực nghiệm tại dự án `serene-bose`, cấm tuyệt đối việc đọc vụn vặt 50 dòng làm đứt gãy ngữ cảnh của hàm/class gây ra 20–30 tool calls lòng vòng.
- **Thiết Lập Chuẩn Cohesive Block Inspection**: Đọc trọn vẹn 100–400 dòng liên quan trong đúng 1 lần gọi `view_file` duy nhất để làm đúng ngay lần đầu (First-Time Right).
- **Cổng Nghiệm Thu Tách Nhịp 2 Bước (Two-Beat Acceptance Gate)**: Bước 1 in toàn văn báo cáo phân tích và hướng dẫn đối chứng ra màn hình, cấm mở modal đè mất chữ. Bước 2 mới mở modal `💎 [NGHIỆM THU HOÀN THIỆN]` sau khi người dùng đã đọc xong.

## [1.4.0] — 2026-09-11
### Added
- **Bộ Khung Tự Vấn Phản Tư 6 Chiều (6-Point Reflective Inquiry)**: Subagent đúc kết tự đặt và trả lời 6 câu hỏi cốt lõi để nâng cấp phương pháp luận Lean Teamwork và trị điểm nghẽn mãn tính.
- **Cơ Chế Khử Phình Tri Thức (Knowledge Pruning & Consolidation)**: Gộp (Merge) và Tỉa (Prune) các quy tắc thừa, duy trì kho tri thức tối đa 10 patterns tinh hoa.

## [1.3.2] — 2026-09-11
### Added
- **Thiết Luật Tăng Version Bắt Buộc (Mandatory Semantic Version Bump)**: Mọi thay đổi dù nhỏ nhất (cấu hình, rule, template, hook) bắt buộc tăng version (`--bump patch`) để cơ chế Fast-Sync trên Laptop luôn nhận diện phiên bản mới và PULL tự động 100%.
- **Phân Định Rạch Ròi Timeout 2.5p vs Treo Popup Cố Định**:
  - *Cổng Đề Xuất Kỹ Thuật (Clarification Gate)*: Áp dụng timeout ngầm 2.5 phút — nếu người dùng bận, AI tự động chọn phương án `(Recommended)` tốt nhất để tiếp tục code, tránh đứt đoạn mạch làm việc.
  - *Cổng Nghiệm Thu Hoàn Thiện (Autonomous Remediation Gate)*: Bắt buộc **treo cố định vĩnh viễn (không timeout)** để chờ người dùng đối chứng thực tế trên máy và bấm xác nhận, đảm bảo Agent rà soát đúc kết học tập chính xác.
- **Kích Hoạt Tầng 2: Mũi Tiêm Tàng Hình Toàn Cục (PreInvocation Re-Anchor)**: Hook ngầm chạy trước MỖI lượt gọi AI ở mọi dự án, tiêm thông điệp Re-Anchor chống trôi ngữ cảnh (Anti-Context Drift) 100%.

## [1.3.1] — 2026-09-11
### Added
- **Chuẩn Hóa Bộ Nhận Diện Icon Cao Cấp (Premium 2-State Popup Identity)**: Nâng cấp bộ biểu tượng cao cấp tương phản `💎 ✨` cho trạng thái Hoàn Tất và `⚡ 🛠️` cho trạng thái Superpowers Debug trên modal `ask_question`, giúp giao diện sắc nét, trực quan và chuyên nghiệp.
- **Kích Hoạt Clarification Gate Toàn Cục**: Đưa quy tắc bắt buộc dùng `ask_question` phỏng vấn người dùng trước khi code vào thẳng `~/.gemini/config/GEMINI.md` toàn cục, ép Antigravity ở mọi workspace luôn chủ động hỏi ý đồ thay vì tự đoán mò.
- **Thư Viện Icon Chuẩn Lucide CDN**: Thay thế toàn bộ SVG tự vẽ tay trong `evaluation_panel_template.html` và bảng Side Panel bằng thư viện Lucide Icons CDN chính thức.

## [1.3.0] — 2026-09-10
### Added
- **Phá Bỏ Thiên Lệch Kẻ Sống Sót (Anti-Survivorship Bias)**: Khắc phục điểm mù cố hữu của Agent nâng cấp/đúc kết. Cấm chỉ nhìn vào Git Diff cuối cùng; bắt buộc kiểm toán toàn bộ vết hành động và số lượt chat (`Turn Count`).
- **Kiểm Toán Vết Hành Động & Thử-Sai (Trajectory Churn Audit)**: Nếu task tốn >2 lượt chat, Agent đúc kết bắt buộc mổ xẻ nguyên nhân thử-sai và trích xuất cả `[Anti-Pattern]` (những suy diễn sai lầm cấm lặp lại) lưu vào `learned_patterns.md`.
- **First-Time Right Protocol**: Khai tử tư duy "Blind Lean" (tinh gọn mù quáng) — cấm đoán mò vì sợ tốn token đọc tài liệu ban đầu. Thà đọc tài liệu chuẩn 1 lần ở Turn 1 để làm đúng ngay lần đầu, tránh phát sinh 5–10 lượt chat thử-sai kéo theo chi phí token khổng lồ.
- **Khóa Kiểm Thử Toàn Vẹn Hệ Thống (9/9 Checks PASS)**: Nâng cấp `tests/test_skill_integrity.py` với kiểm thử `test_anti_survivorship_and_first_time_right` đạt exit code 0.

## [1.2.1] — 2026-09-10
### Added
- **Two-Way Adaptive Sync (Đồng bộ 2 chiều tự thích ứng giữa PC & Laptop)**: Nâng cấp `sync_skill.py` tự động so sánh phiên bản: PULL nếu folder gốc mới hơn, PUSH nếu máy tính mới hơn, và hợp nhất 2 chiều toàn bộ kho bài học `learned_patterns.md`.
- **Zero-Scan Protocol**: Bổ sung `GEMINI.md` controller tại workspace root, đảm bảo laptop chỉ chạy đúng 1 lệnh terminal `py sync_skill.py` là hoàn tất, không đọc quét lặp lại toàn bộ repository.
- **Ratchet Regression Barrier**: Bổ sung kiểm thử `test_versioning_and_fast_sync` khóa chặt cả `AGENTS.md` lẫn `GEMINI.md`, xác nhận 7/7 test cases pass 100%.

## [1.2.0] — 2026-09-10
### Added
- **Popup 2 Trạng Thái Tinh Giản**: Loại bỏ options thừa, tích hợp nút chốt hoàn thành 100% và nút kích hoạt Subagent tự sửa lỗi.
- **Tích Hợp Superpowers Systematic Debugging**: Subagent tự sửa lỗi chạy bằng model `flash`, tuân thủ 4 pha kỷ luật thép (Root cause -> Minimal test -> Minimal diff fix -> Verification).
- **Knowledge Segregation**: Cách ly hoàn toàn tri thức ra file ngoài `learned_patterns.md`, giữ `SKILL.md` siêu nhẹ (<135 dòng).
- **Cơ Chế Fast-Sync & Versioning**: Tạo `sync_skill.py`, `VERSION` và `AGENTS.md` để laptop/máy mới chỉ cần 1 lệnh là tự update skill lên máy, không cần quét lại toàn bộ dự án.

## [1.1.0] — 2026-09-10
### Added
- Timeout Best-Path Fallback 2.5 phút (150 giây).
- Tích hợp 3 Thiết Luật Bất Biến (Iron Laws) từ Superpowers.
- Tách biệt hoàn toàn Stock AGI `/teamwork-preview` và Custom Lean Teamwork.

## [1.0.0] — 2026-09-10
### Added
- Khởi tạo kiến trúc Lean Teamwork Protocol: Subagent Cap (2-4), Model Tiering, Frozen Execution Brief, Independent Evidence Gates.
