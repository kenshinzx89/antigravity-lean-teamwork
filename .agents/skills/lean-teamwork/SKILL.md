---
name: lean-teamwork
description: Kích hoạt quy trình điều phối đa tác tử tinh gọn (Lean Multi-Agent Protocol), tối ưu hóa quota/token với Independent Evidence Gates và Atomic Task Cards. Sử dụng khi người dùng yêu cầu làm việc theo mô hình Lean Teamwork, tối ưu token, hoặc chia việc đa agent có kiểm soát chặt chẽ.
---

# Lean Teamwork Skill & Superpowers Protocol

Hệ thống điều phối tinh gọn kết hợp kỷ luật thép từ **Superpowers** và cơ chế tối ưu hóa Quota & Token từ **Lean Teamwork Protocol**.

---

## 1. 3 Thiết Luật Bất Biến (The 3 Iron Laws)

Mọi agent và phiên làm việc kích hoạt skill này bắt buộc phải tuân thủ 3 thiết luật:

1. **Thiết Luật Nghiệm Thu (Iron Law of Verification)**:
   > *"NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"*
   - Không được tuyên bố code chạy, bug đã sửa hay test đã pass nếu chưa chạy lệnh kiểm chứng trực tiếp ngay trong lượt làm việc.
   - Cấm tuyệt đối các từ ngữ phỏng đoán: *"should work"*, *"probably"*, *"looks correct"*, *"tôi tin rằng"*.
2. **Thiết Luật Nguyên Nhân Gốc & Làm Đúng Lần Đầu (Iron Law of Root Cause & First-Time Right Protocol)**:
   > *"NO FIXES WITHOUT ROOT CAUSE — FIRST-TIME RIGHT OVER TRIAL-AND-ERROR"*
   - Cấm sửa mò, thử sai hay sửa triệu chứng (symptom fixing). Phải đọc stacktrace, tái hiện lỗi ổn định và khoanh vùng chính xác trước khi chạm vào code.
   - **Khai tử tư duy "Blind Lean" (Tinh gọn mù quáng)**: Lean KHÔNG PHẢI là mù quáng không đọc tài liệu. Khi chạm vào kiến trúc, framework hay tính năng client mới, **BẮT BUỘC phải đọc tài liệu chuẩn (Inspect First đầy đủ)** để hiểu rõ mọi ràng buộc ngầm.
   - **Cấm đoán mò vì sợ tốn token đọc tài liệu**: Tiết kiệm 1.000 token đọc tài liệu ở đầu phiên mà để phát sinh >2 lượt chat thử-sai do đoán mò là **phạm luật Quota nghiêm trọng** (vì các lượt chat sau mang theo toàn bộ lịch sử khổng lồ làm tốn gấp 5 lần token và lãng phí thời gian của người dùng).
3. **Thiết Luật Tự Quyết Định & Hướng Đi Tốt Nhất (Ruling & Best-Path Fallback)**:
   > *"A RUNNING PLAN DOES NOT WAIT ON A HUMAN FOR MINOR CHOICES"*
   - Tự ra phán quyết cho các vấn đề vi mô kèm ghi chú rủi ro (`Ruling: <Quyết định> — <Lý do> — <Hệ quả nếu sai>`).
   - **Tự quyết khi quá thời gian chờ (Timeout Best-Path Fallback)**:
     - **Thời gian chờ mặc định**: **2.5 phút (150 giây)**.
     - **Hiển thị đếm ngược bắt buộc**: Khi đặt câu hỏi, luôn in rõ:
       `⏱️ Hạn phản hồi: 2.5 phút (đến HH:MM). Hết thời gian mà không có phản hồi, agent sẽ tự động thực hiện theo: [Phương án Recommended].`
     - **Kỹ thuật thực thi**: Agent đồng thời gọi công cụ `schedule` (`DurationSeconds: 150`, `TimerCondition: "any"`) để tự động đánh thức sau 2.5 phút nếu không có tin nhắn từ người dùng.
     - Khi hết 2.5 phút: Agent tự động chọn phương án khuyến nghị và tiếp tục thực thi, không để phiên bị treo (never park the session).
   - Chỉ dừng lại chờ người dùng tuyệt đối khi gặp: (1) Thao tác phá hủy/xóa dữ liệu, (2) Thay đổi Auth/Security, (3) Tác động ngoài workspace, hoặc (4) Yêu cầu mâu thuẫn hoàn toàn đến mức mọi đường đi tiếp đều là phỏng đoán mù quáng.

---

## 2. Hai Chế Độ Vận Hành

### Chế Độ 1: Daily Lean Mode (Sửa Bug & Tác Vụ Hàng Ngày 1–3 Files)
1. **Systematic Debugging & Pattern Retrieval**:
   - Khi gặp lỗi quen thuộc hoặc phức tạp: liếc nhanh [`docs/learned_patterns.md`](../../docs/learned_patterns.md) để tái sử dụng ngay giải pháp đã từng thành công.
   - Đọc kỹ stacktrace/mã lỗi và tái hiện lỗi qua test case tối thiểu (Red Phase: test bắt buộc fail).
2. **Minimal Compatible Diff**:
   - Sửa đúng nguyên nhân gốc trong 1 thao tác diff nhỏ nhất.
   - Tự sửa lỗi cú pháp vi mô trong 1 lượt duy nhất (Zero-Spawn Minor Remediation).
3. **Green Verification**:
   - Chạy lại test -> Xác nhận PASS (exit code 0).
4. **Tự vấn Quota & Xin xác thực người dùng**.

### Chế Độ 2: Multi-Agent Lean Mode (Tác Vụ Lớn / Tái Cấu Trúc Đa Module)
1. **Intent Architect**: Phỏng vấn tạo và khóa [Execution Brief](./templates/execution_brief_template.md). Khi đặt câu hỏi làm rõ, luôn nêu rõ: *"Nếu không có phản hồi, sẽ tự động áp dụng phương án khuyến nghị để tiếp tục thực hiện."* Không viết code khi chưa chốt phương án.
2. **Subagent Cap (2–4 Subagents)**:
   - 1 Lead Orchestrator
   - Tối đa 2 Workers song song sở hữu file độc quyền
   - 1 Gatekeeper / Independent Auditor
3. **Isolated Context & Workspace Branching**:
   - Subagent **không kế thừa** toàn bộ lịch sử session chat khổng lồ của parent agent; chỉ nhận [Atomic Task Card](./templates/atomic_task_card_template.md).
   - Với tác vụ rủi ro cao: kích hoạt `Workspace: "branch"` trong `invoke_subagent` để cô lập thử nghiệm, bảo vệ an toàn 100% mã nguồn chính.
4. **Model Tiering**:
   - `Model: "flash"` hoặc `"flash_lite"`: Bắt buộc dùng cho Explorer khảo sát, Gatekeeper chạy test, đọc log.
   - `Model: "inherit"` hoặc `"pro"`: Dành riêng cho Lead Orchestrator và Worker viết thuật toán phức tạp.
5. **Compact Handoff**: Báo cáo giữa các agent bắt buộc dưới 20 dòng theo mẫu [Compact Handoff](./templates/compact_handoff_template.md).

---

## 3. Vòng Lặp Tự Vấn Quota Sau Mỗi Chu Kỳ (Cycle Reflection & Quota Audit)

Sau mỗi vòng sửa code / chạy test, agent tự đặt 4 câu hỏi tự vấn theo [Cycle Reflection Template](./templates/cycle_reflection_template.md):
1. **Về Số Lượt & Thử-Sai (Turn Budget & Churn Audit)**: *Task này đã tốn bao nhiêu lượt chat? (Ngưỡng cảnh báo: >2 lượt). Có bị thử-sai hay đổi hướng giải pháp nhiều lần không? Nếu CÓ: Tại sao? Có phải do ban đầu đoán mò vì thiếu tài liệu API/kiến trúc gốc không?*
2. **Về Quota & Token**: *Vừa rồi có đọc thừa file nào không? Log terminal có quá dài không? Có thể rút ngắn handoff hoặc lược bớt bước nào để tiết kiệm token ở vòng kế tiếp không?*
3. **Về Bằng Chứng (Anti-Rationalization Check)**: *Đã có bằng chứng khách quan (exit code 0, kết quả chạy thật) chưa, hay còn điểm nào phỏng đoán?*
4. **Về Tinh Gọn & Anti-Pattern**: *Có phát hiện mẫu lặp lại (pattern) cần lưu hoặc sai lầm thử-sai (anti-pattern) cần chặn không?*

---

## 4. Cổng Xác Thực Đích Đến Từ Người Dùng (Goal Confirmation Gate)

Khi tất cả các tiêu chí trong Execution Brief hoặc mục tiêu sửa bug đã đạt bằng chứng khách quan:
1. **Dừng lại và xin xác nhận rõ ràng**:
   > *"Tác vụ đã hoàn thành theo yêu cầu. Bạn đã kiểm tra và xác nhận OK chưa?"*
2. **Không tự đóng phiên**: Bắt buộc chờ phản hồi của người dùng trước khi chuyển sang bước đúc kết.

---

## 4.5. Chuyển Hướng Toàn Bộ Đề Xuất & Nghiệm Thu Về Desktop Widget Popover HUD (Widget HUD Decoupled — Rảnh Khung Chat 100%)

Hệ thống chuyển hướng toàn bộ khâu Đề xuất Kỹ thuật (🧭) và Nghiệm thu Hoàn thiện (💎) sang **Desktop Widget Popover HUD** thông qua IPC Bridge (`scripts/teamwork_bridge.py`), **BỎ HOÀN TOÀN modal `ask_question` cũ trong khung chat**:

### 1. 🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡 (2 Lối Song Hành: Chat Stream + Widget HUD Popover)
- **Khi nào kích hoạt**: Khi vừa nhận yêu cầu mới, phân tích hướng đi, hoặc đứng trước các ngã rẽ kỹ thuật quan trọng.
- **Quy chuẩn thực thi 2 Lối Song Hành**:
  1. **Lối 1 (Khung Chat Antigravity)**:
     - Agent in trực tiếp danh sách phương án ra khung chat, đánh số thứ tự rõ ràng kèm phương án `[1] (Recommended) ⭐`.
     - **BẮT BUỘC gọi công cụ `schedule`** (`DurationSeconds: 150`, `TimerCondition: "any"`, `Prompt: "Hết hạn 2.5 phút chờ đề xuất kỹ thuật. Tự động kích hoạt phương án [1] (Khuyên dùng) và tiếp tục thực thi."`).
     - Nếu người dùng có mặt và gõ phím/chọn: Timer `schedule` tự hủy ngay lập tức.
     - Nếu người dùng vắng mặt: Hết 2.5 phút, `schedule` tự động đánh thức AI chọn phương án 1 và tiếp tục code, không để đứt đoạn mạch công việc.
  2. **Lối 2 (Desktop Widget HUD Popover)**:
     - Agent đồng thời gọi `teamwork_bridge.publish_proposal(title, options, duration_seconds=150)` để đẩy đề xuất lên Desktop Widget.
     - Widget tự động bung Popover to rõ trên Desktop với đồng hồ đếm ngược 7 màu Spectrum và danh sách phương án trực quan.
     - Người dùng có thể click chọn trực tiếp trên Desktop Widget (Widget tự động focus và gửi phím số xuống IDE).
     - **Tự động trả về 1 khi hết giờ**: Khi Widget đếm đủ thời gian (hết 150 giây) mà người dùng chưa bấm chọn gì, Widget sẽ **tự động gửi phím '1' về Antigravity IDE cho gọn** và tự đóng Popover!
  3. **TUYỆT ĐỐI KHÔNG GỌI modal `ask_question`**: Khung chat hoàn toàn rảnh rang, không bị modal pop-up chiếm chỗ hay đóng băng tiến trình.

### 2. 💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨ (Widget HUD Decoupled — Treo Cố Định Widget)
- **Khi nào kích hoạt**: Khi code đã viết xong, toàn bộ kiểm thử tích hợp đạt 100% PASS (Exit Code 0).
- **Quy trình Nghiệm Thu Tách Nhịp 2 Bước Rảnh Khung Chat (Two-Beat Decoupled Acceptance)**:
  - **BƯỚC 1 (In Báo Cáo Ra Chat)**: In toàn văn Báo cáo phân tích, kết quả kiểm thử và hướng dẫn đối chứng thực tế ra màn hình chat. Khung chat hiển thị sạch sẽ, minh bạch.
  - **BƯỚC 2 (Treo Nghiệm Thu Trên Desktop Widget)**:
    - Agent gọi `teamwork_bridge.publish_acceptance(title, summary, exit_code=0, files_changed=[...])` để đẩy trạng thái Nghiệm Thu lên Desktop Widget.
    - Popover trên Desktop Widget tự động bung ra và **TREO CỐ ĐỊNH VĨNH VIỄN TRÊN WIDGET** theo **Cấu trúc Popup 2 Trạng Thái** kinh điển:
      1. `💎 [100% HOÀN TẤT] ✨` (Chấp thuận & Khóa tri thức tự động)
      2. `⚡ [SUPERPOWERS DEBUG] 🛠️` (Yêu cầu AI chuyên trách truy vết sâu)
    - **TUYỆT ĐỐI KHÔNG GỌI modal `ask_question`**: Loại bỏ hoàn toàn modal popup cũ trong khung chat. Người dùng kiểm tra đối chứng xong có thể bấm trực tiếp từ Desktop Widget bất kỳ lúc nào mà không lo bị che mất chữ trong khung chat.

### 3. Quy Trình Sửa Lỗi 4 Pha & Điểm Dừng Duy Nhất
- **Khi người dùng chọn nút 2 (`⚡ [SUPERPOWERS DEBUG] 🛠️`) trên Widget**:
  - Main Agent kích hoạt Subagent chuyên trách (`invoke_subagent`, model: `flash`, role: `Superpowers Debugger & Remediation Worker`).
  - Subagent thực thi chuẩn xác quy trình 4 pha từ [Superpowers Systematic Debugging](./references/systematic-debugging.md): (1) Root Cause -> (2) Hypothesis & Red Test -> (3) Minimal Fix -> (4) Green Verification.
- **Điểm dừng duy nhất & Chuẩn Hóa Mật Mã Nghiệm Thu (`OK 💎` / `ok::`)**:
  - Tín hiệu nghiệm thu hoàn tất duy nhất là mật mã **`OK 💎`** (được Desktop Widget tự động gửi khi bấm nút `💎 [100% HOÀN TẤT] ✨` hoặc do người dùng gõ `OK 💎`, hoặc phím tắt siêu tốc **`ok::`**).
  - **Quy tắc Chống Nhầm Lẫn (Anti-False-Acceptance)**: Các trao đổi thông thường chứa chữ "ok" (ví dụ: *"ok làm tiếp đi", "ok bạn", "ok nhé", "ok để mình xem"...*) TUYỆT ĐỐI KHÔNG phải là lệnh nghiệm thu hoàn tất. AI chỉ kích hoạt Self-Evolution khi nhận được mật mã có kèm emoji kim cương `OK 💎` (hoặc `💎 OK`, `[ACCEPT] 💎`, hoặc phím tắt siêu tốc `ok::`).
  - Khi bắt được mật mã `OK 💎` hoặc `ok::`, AI hiểu ngay 100% người dùng đã nghiệm thu chấp thuận và kích hoạt Subagent (`flash`, role: `Knowledge & Quota Synthesizer`) thực thi **Bộ Khung Tự Vấn Phản Tư 6 Chiều** và **Cơ chế Khử Phình Tri Thức** (Merge & Prune), rà soát lỗi trung gian từ mốc hoàn tất gần nhất vào `docs/learned_patterns.md` (hoặc `~/.gemini/config/learned_patterns.md`). Tuyệt đối không nạp vào `SKILL.md`.

---

## 5. Nguyên Tắc Cách Ly Tri Thức & Tự Tiến Hóa (Knowledge Segregation & Continuous Self-Evolution)

> *"TUYỆT ĐỐI KHÔNG NẠP HẾT KINH NGHIỆM VÀO SKILL.MD — TRÁNH BẮT AGY PHẢI ĐỌC TOÀN BỘ MỖI LẦN KHỞI CHẠY"*

1. **SKILL.md là Bộ Quy Tắc Tối Giản (Orchestration Rules Only)**:
   - `SKILL.md` chỉ chứa luật chơi, cấu trúc điều phối và giao thức tương tác (<150 dòng). Tuyệt đối không nhồi nhét log sửa lỗi, bài học tình huống, hay code snippets mẫu vào đây.
2. **Kho Tri Thức Nằm Hoàn Toàn Bên Ngoài (External Segmented Store)**:
   - Mọi bài học đúc kết được lưu tại [`docs/learned_patterns.md`](../../docs/learned_patterns.md) (cấp dự án) và `~/.gemini/config/learned_patterns.md` (toàn cục máy phát triển).
3. **Truy Xuất Đúng Tag Khi Cần (Progressive On-Demand Retrieval)**:
   - Khi bước vào tác vụ mới, agent **không đọc toàn bộ** kho tri thức.
   - Chỉ khi gặp đúng lỗi/chủ đề cụ thể (ví dụ: `[Database]`, `[Build]`, `[Network]`), agent mới dùng `grep_search` quét đúng `[Tag]` tương ứng để đọc đúng 2–3 dòng giải pháp tối thiểu. Nhờ đó, lượng token context ban đầu luôn ở mức thấp nhất.
4. **Cơ Chế Two-Way Adaptive Sync (Đồng bộ 2 chiều tự thích ứng giữa PC & Laptop)**:
   - Trước khi thực thi hoặc sau khi đúc kết tri thức: Liếc nhanh số hiệu phiên bản giữa folder gốc (`VERSION`) và máy tính (`~/.gemini/config/skills/lean-teamwork/VERSION`).
   - Chạy lệnh duy nhất `py sync_skill.py`:
     - **PULL**: Nếu folder gốc mới hơn (`ver_source > ver_installed`) -> Tự động kéo bản cập nhật vào máy tính.
     - **PUSH**: Nếu máy tính vừa học hỏi kiến thức mới (`ver_installed > ver_source`) -> Tự động đẩy ngược về folder gốc để PC/thiết bị khác dùng ngay.
     - **SYNC 2 CHIỀU**: Cân bằng 2 chiều tri thức `learned_patterns.md` (bảo toàn 100% bài học ở cả 2 nơi).
   - Tuyệt đối tuân thủ Zero-Scan Protocol: Không đọc quét lan man các file mã nguồn, tiết kiệm 100% quota token.
5. **Phá Bỏ Thiên Lệch Kẻ Sống Sót & Kiểm Toán Thử-Sai Từ Lần Hoàn Tất Gần Nhất (Anti-Survivorship Bias, Trajectory Churn Audit & From-Last-Completion Retrospective Anchor)**:
   - **Biên độ tổng hợp bắt buộc từ lần bấm Hoàn tất gần nhất (From-Last-Completion Anchor)**: Nếu người dùng chưa bấm Hoàn tất vì còn lỗi và tiếp tục trao đổi qua nhiều lượt chat trung gian, khi người dùng bấm `💎 [100% HOÀN TẤT] ✨`, Subagent đúc kết BẮT BUỘC phải rà soát và tổng hợp TOÀN BỘ chuỗi lỗi, các giả định sai và các lần sửa **TỪ LẦN BẤM HOÀN TẤT GẦN NHẤT ĐẾN NAY**, tuyệt đối không được bỏ sót bất kỳ lỗi trung gian nào.
   - **Cấm chỉ nhìn vào kết quả thành công cuối cùng (Anti-Survivorship Bias)**: Tuyệt đối không chỉ nhìn vào Git diff cuối cùng hay lượt chat chót mà bỏ qua các lần test đỏ, exception hay phản hồi chỉnh sửa của người dùng ở các lượt giữa.
   - **Kiểm toán số lượt hội thoại (Turn Budget Audit)**: Nếu tác vụ tốn >2 lượt chat mới xong, Subagent BẮT BUỘC phải mổ xẻ nguyên nhân gốc: *Tại sao lần đầu làm sai? Có phải do cấm đoán đọc tài liệu chuẩn dẫn đến phỏng đoán mò mẫm không?*
   - **Đúc kết Anti-Pattern song song**: Rút ra cả `[Pattern]` (cách làm đúng) và `[Anti-Pattern]` (những phán đoán/thao tác sai lầm cấm lặp lại) lưu vào `learned_patterns.md`.
6. **Bộ Khung Tự Vấn Phản Tư 6 Chiều & Khử Phình Quy Tắc (6-Point Reflective Inquiry & Anti-Rule-Bloat)**:
   - **Chống phình to quy tắc (Anti-Rule-Bloat)**: Không tích lũy vô hạn. Subagent sau nghiệm thu tự vấn 6 câu (Nguyên nhân thử-sai, Làm chuẩn lần 1, Tiết kiệm quota, Tăng tốc tiến trình, Khử quy tắc thừa, Tự vấn đệ quy & Rà soát điểm nghẽn mãn tính).
   - **Nén, Tỉa & Trị Điểm Nghẽn Mãn Tính (Merge, Prune & Remediate)**: Hợp nhất các mẫu tương tự, tỉa bỏ quy tắc lỗi thời và tự động hành động khắc phục những điểm nghẽn đã cải tiến nhiều lần mà chưa mượt, giữ kho tri thức luôn súc tích và bộ não AI luôn sắc bén.
7. **Kiểm Toán & Tinh Gọn Kỹ Năng Sẵn Có Qua 3–4 Chu Kỳ Nghiệm Thu (Multi-Cycle Skill Usage Audit & On-Demand Context Pruning)**:
   - **Rà soát chuỗi 3–4 mốc nghiệm thu gần nhất**: Khi kết thúc nhiệm vụ, Subagent đúc kết (hoặc Agent nghiệm thu) BẮT BUỘC nhìn lại toàn bộ quá trình qua 3–4 chu kỳ nghiệm thu gần đây để đánh giá danh mục các kỹ năng sẵn có trong Antigravity (`~/.gemini/config/skills/`):
     - *Kỹ năng nòng cốt & đang dùng*: Giữ nguyên các skill thiết yếu (`lean-teamwork`, `git-workflow`, `agentic-engineering`, v.v.) và các skill thuộc tech-stack dự án hiện tại.
     - *Kỹ năng thừa cần tắt bớt*: Tạm tắt các skill hoàn toàn không đụng tới trong suốt 3–4 chu kỳ vừa qua hoặc không thuộc tech-stack của dự án (ví dụ: `laravel-*`, `django-*`, `quarkus-*`, `blender-*`, `csharp-*`, `fsharp-*`, `homelab-*`...) bằng cách chuyển vào `~/.gemini/config/skills_archive/` (hoặc chạy `py scripts/manage_skills.py --prune`). Việc này giải phóng hàng nghìn token trong system prompt ở mọi lượt gọi model tiếp theo.
   - **Báo cáo minh bạch & Gọi lại tức thì khi cần (Transparent Report & Instant Recall On-Demand)**:
     - Báo cáo rõ ràng trong phần đúc kết: Danh sách các skill đã tắt và lý do tắt để tiết kiệm Context Window.
     - Luôn đính kèm hướng dẫn: Các skill này không hề bị mất. Bất cứ khi nào cần lại skill nào trong tương lai, người dùng hoặc AI chỉ cần yêu cầu: *"Bật lại skill [tên skill]"* (hoặc chạy `py scripts/manage_skills.py --restore <tên_skill>`), kỹ năng sẽ lập tức được kích hoạt trở lại 100%!
8. **Chuyển Giao Kỹ Năng Động & Dự Phóng Nhu Cầu Đón Đầu (Predictive Skill Switcher & Sandboxing)**:
   - **Skill Sandboxing (Cô lập skill kiểm thử nặng qua Subagent)**: Cấm bơm các skill nặng (`browser-qa`, `e2e-testing`, `a11y-debugging`, `postgres-patterns`...) trực tiếp vào Main Context. Các tác vụ kiểm thử và rà soát chuyên sâu bắt buộc được ủy quyền cho Subagent độc lập (`Model: "flash"`). Khi Subagent kết thúc, toàn bộ context của skill đó tự động tiêu biến, giữ cho Main Context luôn tinh gọn tuyệt đối.
   - **Speculative Next-Step & Skill Proposal (Dự phóng nhu cầu tại Bước 1 Nghiệm Thu)**: Tại Bước 1 của Chế độ Nghiệm Thu, Agent nắm giữ trọn vẹn bức tranh kỹ thuật vừa hoàn thành và BẮT BUỘC dự phóng 2-3 kịch bản logic tự nhiên tiếp theo kèm danh mục kỹ năng đón đầu (chạy `py scripts/manage_skills.py --predict <domain>`):
     - Xác định rõ: (1) Tính năng đã xong $\rightarrow$ (2) Dự phóng kịch bản tiếp theo $\rightarrow$ (3) Kỹ năng đề xuất cất gọn (`unload`) $\rightarrow$ (4) Kỹ năng đề xuất nạp đón đầu (`preload`).
   - **Dynamic Skill Switch & Clean-Slate Turn (Chuyển giao kỹ năng động)**: Sử dụng lệnh `py scripts/manage_skills.py --switch --unload <a,b> --load <c,d>` để tự động cất kỹ năng cũ và nạp kỹ năng mới, triệt tiêu 100% xung đột quy tắc (Instruction Drift) và ô nhiễm ngữ cảnh (Context Bloat).

---

## 6. Tài Liệu Tham Chiếu Chi Tiết

- [Tích hợp Superpowers](./references/superpowers-integration.md)
- [Cẩm nang Systematic Debugging](./references/systematic-debugging.md)
- [Kiến trúc & Cổng bằng chứng](./references/architecture.md)
- [Quy tắc kiểm soát Quota & Token](./references/lean-protocol.md)
