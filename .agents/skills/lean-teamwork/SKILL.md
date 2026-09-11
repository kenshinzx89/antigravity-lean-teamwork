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

## 4.5. Phân Biệt Hai Chế Độ Modal: Đề Xuất Kỹ Thuật (🧭) vs Nghiệm Thu Hoàn Thiện (💎)

Hệ thống sử dụng công cụ `ask_question` để kích hoạt Popup tương tác với 2 chế độ nhận diện riêng biệt:

### 1. 🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡 (Khởi đầu / Lựa chọn giải pháp kiến trúc)
- **Khi nào kích hoạt**: Khi vừa nhận yêu cầu mới, phân tích hướng đi, hoặc đứng trước các ngã rẽ kỹ thuật quan trọng.
- **Quy chuẩn hiển thị**: Tiền tố câu hỏi modal `ask_question` bắt buộc có nhãn `🧭 [ĐỀ XUẤT KỸ THUẬT] ⏱️ [HẠN 2.5 PHÚT] 💡`.
- **Cấu trúc tùy chọn**: Cung cấp từ 2 đến 4 giải pháp cụ thể, luôn đánh dấu dòng tối ưu nhất bằng `(Recommended)`.
- **Đồng hồ đếm ngược & Hạn thời gian (Timeout 2.5 phút)**:
  - Do modal UI của Antigravity hiển thị văn bản tĩnh (không có widget animation SVG kim đồng hồ chạy trực tiếp), giới hạn đếm ngược được thể hiện rõ nét qua nhãn `⏱️ [HẠN 2.5 PHÚT — TỰ ĐỘNG CHỌN RECOMMENDED NẾU QUÁ GIỜ]`.
  - Nếu sau 2.5 phút người dùng chưa bấm chọn, hệ thống tự động tiếp tục với hướng `(Recommended)` để giữ mạch công việc không bị đình trệ.

### 2. 💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨ (Popup 2 Trạng Thái Chuẩn Superpowers)
- **Khi nào kích hoạt**: Khi code đã viết xong, toàn bộ kiểm thử tích hợp đạt 100% PASS (Exit Code 0).
- **Quy chuẩn hiển thị**: Tiền tố câu hỏi modal `ask_question` bắt buộc có nhãn `💎 [NGHIỆM THU HOÀN THIỆN] ✨`.
- **Cấu trúc Popup 2 Trạng Thái kinh điển**:
  1. `(Recommended) 💎 [100% HOÀN TẤT] ✨ Xác nhận nghiệm thu toàn diện & Khóa tri thức tự động`
  2. `⚡ [SUPERPOWERS DEBUG] 🛠️ Mở AI chuyên trách tự truy vết mã lỗi & sửa trúng đích (4 pha chuẩn Superpowers, tiết kiệm quota)`
  *(Kèm ô nhập liệu bên dưới để người dùng có thể gõ chỉ định lỗi cụ thể nếu muốn).*
- **Cơ chế thời gian (Treo cố định vĩnh viễn - KHÔNG TIMEOUT / KHÔNG ĐẾM NGƯỢC)**:
  - BẮT BUỘC treo chờ người dùng trực tiếp kiểm tra và đối chứng thực tế trên môi trường thật.
  - Tuyệt đối KHÔNG đếm ngược, KHÔNG tự động chọn, KHÔNG tự ý đóng phiên.

### 3. Quy Trình Sửa Lỗi 4 Pha & Điểm Dừng Duy Nhất
- **Khi người dùng chọn dòng 2 (`⚡ [SUPERPOWERS DEBUG] 🛠️`)**:
  - Main Agent kích hoạt Subagent chuyên trách (`invoke_subagent`, model: `flash`, role: `Superpowers Debugger & Remediation Worker`).
  - Subagent thực thi chuẩn xác quy trình 4 pha từ [Superpowers Systematic Debugging](./references/systematic-debugging.md): (1) Root Cause -> (2) Hypothesis & Red Test -> (3) Minimal Fix -> (4) Green Verification.
  - Sửa xong: Báo cáo ngắn gọn và **BẮT BUỘC BẬT LẠI POPUP NGHIỆM THU NGAY LẬP TỨC**.
- **Điểm dừng duy nhất**: Vòng lặp chỉ kết thúc khi người dùng bấm `💎 [100% HOÀN TẤT] ✨`. Khi đó kích hoạt Subagent (`flash`, role: `Knowledge & Quota Synthesizer`). Subagent thực thi **Bộ Khung Tự Vấn Phản Tư 6 Chiều** (Root Cause, First-Time Right, Token Economy, Velocity, Rule Pruning, Meta-Questioning & Chronic Bottlenecks) và **Cơ chế Khử Phình Tri Thức** (Merge & Prune) nhằm nén và tinh lọc bài học vào `docs/learned_patterns.md` (hoặc `~/.gemini/config/learned_patterns.md`). Tuyệt đối không nạp vào `SKILL.md`.

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
5. **Phá Bỏ Thiên Lệch Kẻ Sống Sót & Kiểm Toán Thử-Sai (Anti-Survivorship Bias & Trajectory Churn Audit)**:
   - **Cấm chỉ nhìn vào kết quả thành công cuối cùng (Anti-Survivorship Bias)**: Subagent đúc kết khi được kích hoạt KHÔNG ĐƯỢC chỉ nhìn vào Git diff cuối cùng mà bỏ qua chuỗi thử-sai trước đó.
   - **Kiểm toán số lượt hội thoại (Turn Budget Audit)**: Nếu tác vụ tốn >2 lượt chat mới xong, Subagent BẮT BUỘC phải mổ xẻ nguyên nhân gốc: *Tại sao lần đầu làm sai? Có phải do cấm đoán đọc tài liệu chuẩn dẫn đến phỏng đoán mò mẫm không?*
   - **Đúc kết Anti-Pattern song song**: Rút ra cả `[Pattern]` (cách làm đúng) và `[Anti-Pattern]` (những phán đoán/thao tác sai lầm cấm lặp lại) lưu vào `learned_patterns.md`.
6. **Bộ Khung Tự Vấn Phản Tư 6 Chiều & Khử Phình Quy Tắc (6-Point Reflective Inquiry & Anti-Rule-Bloat)**:
   - **Chống phình to quy tắc (Anti-Rule-Bloat)**: Không tích lũy vô hạn. Subagent sau nghiệm thu tự vấn 6 câu (Nguyên nhân thử-sai, Làm chuẩn lần 1, Tiết kiệm quota, Tăng tốc tiến trình, Khử quy tắc thừa, Tự vấn đệ quy & Rà soát điểm nghẽn mãn tính).
   - **Nén, Tỉa & Trị Điểm Nghẽn Mãn Tính (Merge, Prune & Remediate)**: Hợp nhất các mẫu tương tự, tỉa bỏ quy tắc lỗi thời và tự động hành động khắc phục những điểm nghẽn đã cải tiến nhiều lần mà chưa mượt, giữ kho tri thức luôn súc tích và bộ não AI luôn sắc bén.

---

## 6. Tài Liệu Tham Chiếu Chi Tiết

- [Tích hợp Superpowers](./references/superpowers-integration.md)
- [Cẩm nang Systematic Debugging](./references/systematic-debugging.md)
- [Kiến trúc & Cổng bằng chứng](./references/architecture.md)
- [Quy tắc kiểm soát Quota & Token](./references/lean-protocol.md)
