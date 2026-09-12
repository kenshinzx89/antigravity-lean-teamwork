# Cơ Chế Tự Tiến Hóa & Đúc Kết Tri Thức (Self-Evolution Architecture)

Tài liệu thiết kế quy trình khép kín giúp hệ thống Lean Teamwork tự hoàn thiện sau mỗi nhiệm vụ, liên tục giảm lượng token tiêu thụ và tăng tốc độ xử lý dựa trên tinh hoa từ **Hermes Agent**, **Superpowers** và **Recursive-Improve**.

---

## 1. Vòng Đời Tiến Hóa Của Nhiệm Vụ

```text
[Bắt đầu nhiệm vụ]
       │
       ▼
[Thực thi chu kỳ 1..N] ──> [Tự vấn Quota sau mỗi vòng (Cycle Audit)]
       │               ──> [Nén Vết Hành Động (Trajectory Compaction)]
       ▼
[Đạt đủ bằng chứng khách quan (Exit Code 0)]
       │
       ▼
[Treo Bảng Gợi Ý Đánh Giá (Evaluation Panel)] ──(Giữ nguyên checklist & câu hỏi trên IDE)
       │
       ▼
[CỔNG XÁC THỰC NGƯỜI DÙNG] ──(Người dùng test xong gõ "OK / Đã xong")
       │
       ▼
[Kích hoạt Retrospective Loop] ──(Phân tích nội tại giai đoạn: hiệu năng, quota, token)
       │
       ▼
[Trích xuất Tri thức & Golden Path]
       │
       ├──> Thiết lập "Bánh Răng Khóa Chống Hồi Quy" (Ratchet Regression Barrier)
       ├──> Ghi nhận vào docs/learned_patterns.md
       └──> Thăng hạng Skill (Rule of 3) hoặc Tỉa bỏ tri thức thừa (Pruning)
```

---

## 2. 4 Cơ Chế Tự Tiến Hóa Nâng Cao

### 1. Cơ Chế "Bánh Răng Khóa" Chống Hồi Quy (The Ratchet Mechanism)
- Mỗi bug sau khi được sửa và xác nhận "OK" bắt buộc phải có ít nhất một unit test / regression test bảo vệ.
- Test này được bổ sung vào bộ kiểm thử chuẩn của dự án. Không bao giờ cho phép mã nguồn bị sửa lùi dẫn đến tái xuất hiện lỗi cũ.

### 2. Định Dạng "Đường Đi Vàng" (Golden Path Sequence)
- Thay vì ghi chép lý thuyết dài dòng, hệ thống lưu trữ chuỗi hành động công cụ tối thiểu:
  ```text
  Golden Path [Tên Task]: Tool 1 -> Tool 2 -> Tool 3 (Exit Code 0)
  ```
- Lần sau gặp bài toán tương tự, agent tái hiện trực tiếp chuỗi công cụ này, tiết kiệm 70% số lượt chat.

### 3. Nén Vết Hành Động Nguyên Tử (Trajectory Compaction)
- Giữa các chu kỳ làm việc, agent tự động tóm tắt các khối log terminal dài thành 1 dòng **Atomic Milestone**:
  `Milestone #N: <Hành động đã làm> -> <Test kết quả (exit 0)> -> <Rủi ro còn lại>.`
- Giúp giải phóng bộ nhớ context window, ngăn cản cạn kiệt token quota.

### 4. Quy Tắc Thăng Hạng Kỹ Năng (Rule of 3 - Skill Promotion)
- **Thăng hạng (Promotion)**: Khi một pattern trong `learned_patterns.md` được tái sử dụng thành công từ 3 lần trở lên, nó sẽ được tự động đề xuất đóng gói thành một Custom Skill con riêng biệt hoặc một automation script.
- **Tỉa bỏ (Pruning)**: Những bài học đã lỗi thời hoặc đã được thư viện/framework sửa tận gốc sẽ được lược bỏ định kỳ để giữ kho tri thức luôn dưới 50 dòng tinh hoa.

### 5. Cơ Chế Bảng Đánh Giá Side Panel Độc Lập & Subagent Tích Lũy (Persistent Side Panel Gate)
- **Mở bảng độc lập trên Side Panel (`evaluation_panel.html`)**: Khi hoàn thành một giai đoạn, agent tạo artifact giao diện web mở cố định ở Editor / Split View bên phải. Bảng này **tách rời hoàn toàn khỏi khung chat**, không làm gián đoạn hay chặn người dùng chat.
- **Sống liên tục xuyên suốt các lượt trao đổi (Persistent Across Turns)**: Người dùng có thể để nguyên bảng ở tab bên phải và tiếp tục chat ở khung bên trái để yêu cầu sửa code thêm bao nhiêu lượt tùy ý. Agent tiếp tục debug và tự động cập nhật lại checklist trên Side Panel.
- **Chỉ kích hoạt Subagent khi người dùng bấm/chat xác nhận**: Khi người dùng đã test xong thực tế và xác nhận `OK / Đã xong`, Main Agent mới kích hoạt một subagent độc lập nhẹ (`flash`) chạy ngầm đi khảo sát diff, kiểm toán token và trích xuất bài học có Tag vào kho tri thức bên ngoài.

### 6. Nguyên Tắc Cách Ly Tri Thức (Knowledge Segregation & On-Demand Retrieval)
- **Không nhồi nhét vào SKILL.md**: Tuyệt đối không nạp toàn bộ bài học/kinh nghiệm vào file `SKILL.md`. Việc này sẽ khiến AGY mỗi lần kích hoạt skill phải đọc toàn bộ văn bản khổng lồ, làm cạn kiệt context window và token quota.
- **Lưu trữ ngoài & Tra cứu theo Tag (On-Demand Retrieval)**: Toàn bộ kinh nghiệm được lưu tách biệt tại `docs/learned_patterns.md`. Agent trong các phiên làm việc bình thường không đọc file này; chỉ khi gặp đúng mã lỗi hay chủ đề mang `[Tag]` tương ứng thì mới dùng `grep_search` quét đúng 2–3 dòng hướng dẫn.

### 7. Đồng Bộ 2 Chiều Tự Thích Ứng (Two-Way Adaptive Sync Protocol Giữa PC & Laptop)
- **Tự động so sánh phiên bản**: Script `sync_skill.py` tự động so sánh số phiên bản giữa folder gốc (`REPO_ROOT/VERSION`) và máy tính hiện tại (`~/.gemini/config/skills/lean-teamwork/VERSION`).
- **PULL khi folder gốc mới hơn**: Khi làm việc trên Laptop, nếu folder gốc có phiên bản mới hơn do PC vừa cập nhật, hệ thống tự động kéo các templates, references, và rules mới vào máy tính.
- **PUSH khi máy tính mới hơn**: Nếu Laptop vừa kết thúc chu kỳ tự tiến hóa và có version/tri thức mới hơn, hệ thống tự động đẩy ngược các thay đổi và bài học về lại folder gốc để PC có thể dùng ngay mà không bị lệch phiên bản.
- **Cân bằng 2 chiều tri thức (Bidirectional Pattern Merge)**: Hợp nhất các khối bài học có Tag từ cả 2 nguồn, đảm bảo dù bài học được đúc kết trên PC hay Laptop thì cả 2 môi trường đều sở hữu 100% kho tri thức tinh gọn.
- **Zero-Scan Protocol**: Toàn bộ chu trình chỉ gói gọn trong 1 lệnh duy nhất (`py sync_skill.py`), tuyệt đối không đọc quét lan man các file trong repo, tiết kiệm 100% quota và thời gian chờ.

### 8. Phá Bỏ Thiên Lệch Kẻ Sống Sót (Anti-Survivorship Bias & Trajectory Churn Audit)
- **Nghịch lý "Blind Lean" & Điểm mù của Agent nâng cấp**:
  - Khi cấm AI đọc tài liệu vì sợ tốn token ở Turn 1, AI sẽ đoán mò -> Đưa ra giải pháp chắp vá -> Thử-sai qua 8–10 lượt chat.
  - Các lượt chat sau mang theo toàn bộ lịch sử hội thoại (20.000–40.000 tokens), khiến tổng chi phí token tăng gấp 3–5 lần và kéo dài hàng tiếng đồng hồ.
  - **Tại sao Agent tổng hợp trước đây không tự đặt câu hỏi để sửa?**: Do mắc hội chứng *Thiên lệch kẻ sống sót (Survivorship Bias)* — Agent đúc kết chỉ được gọi khi user bấm "ĐÃ XONG" và chỉ nhìn vào Git Diff cuối cùng đã chạy được. Nó hoàn toàn mù trước chuỗi thử-sai thất bại trước đó!
- **Giải pháp Kiểm toán vết hành động (Trajectory Churn Audit)**:
  - Subagent đúc kết bắt buộc phải kiểm toán số lượt chat (`Turn Count`).
  - Nếu số lượt chat > 2: Bắt buộc mổ xẻ nguyên nhân thử-sai (có phải do đoán mò không đọc tài liệu/API gốc ở Turn 1 không?).
  - Trích xuất đồng thời `[Pattern]` (giải pháp chuẩn) và `[Anti-Pattern]` (những suy diễn sai lầm cấm lặp lại) lưu vào `learned_patterns.md`.
- **First-Time Right Protocol**: Thà đọc tài liệu chuẩn 1 lần ở Turn 1 để làm đúng ngay (First-Time Right), còn hơn tiết kiệm mù quáng để rồi thử-sai qua nhiều lượt chat.

---

## 9. Bộ Khung Tự Vấn Phản Tư 6 Chiều & Cơ Chế Khử Phình Tri Thức (6-Point Reflective Inquiry & Knowledge Pruning Protocol)

### 1. Cái Bẫy "Phình To Quy Tắc" (The Rule Bloat & Cognitive Overload Trap)
Nếu sau mỗi lần nghiệm thu chỉ đơn thuần tích lũy (append) bài học mới, tập quy tắc và kho tri thức sẽ ngày càng dày đặc:
- **Tốn Quota Lũy Tiến**: Mỗi lượt gọi model phải cõng thêm hàng nghìn token quy tắc thừa.
- **Nhiễu Loạn Chỉ Dẫn (Cognitive Confusion)**: Khi có quá nhiều luật lệ chồng chéo, AI mất phương hướng, giảm tốc độ suy luận và dễ mắc lỗi hơn.

### 2. Bộ Câu Hỏi Tự Vấn Phản Tư 6 Chiều (6-Point Reflective Inquiry)
Sau khi người dùng bấm nghiệm thu hoàn tất (`💎 [100% HOÀN TẤT] ✨`), Subagent đúc kết BẮT BUỘC phải tự vấn và tự trả lời 6 câu hỏi cốt lõi để nâng cấp chính phương pháp luận Lean Teamwork:

1. ❓ **Q1 [Root Cause & Churn - Nguyên Nhân Gốc Thử-Sai]**: *Tại sao tác vụ này phải làm lại nhiều lần (nếu có)? Đâu là điểm gãy khiến lần đầu chưa đạt?*
2. ❓ **Q2 [First-Time Right - Năng Lực Làm Chuẩn]**: *Có thể dùng Lean Teamwork làm tốt hơn, chính xác hơn ngay từ lượt đầu tiên bằng cách nào?*
3. ❓ **Q3 [Token Economy - Tiết Kiệm Quota]**: *Có thao tác nào của Lean Teamwork làm tốn token vô ích không? Có cách nào cắt giảm context và tối ưu hoá quá trình đó không?*
4. ❓ **Q4 [Velocity & Automation - Tăng Tốc Tiến Trình]**: *Có cách nào để Lean Teamwork thực thi nhanh hơn (tự động hóa qua hook, background script, tối giản câu lệnh)?*
5. ❓ **Q5 [Rule Pruning & Anti-Bloat - Khử Thừa & Tinh Gọn Tri Thức]**: *Có quy tắc hoặc bài học cũ nào đã lỗi thời, dư thừa hoặc trùng lặp trong kho tri thức cần được GỘP (Merge & Generalize) hoặc XÓA BỎ (Prune) để giữ bộ quy tắc luôn nhẹ và không làm AI bị quá tải không?*
6. ❓ **Q6 [Meta-Questioning & Chronic Bottlenecks - Tự Vấn Đệ Quy & Điểm Nghẽn Mãn Tính]**: *Subagent tự vấn chính mình: "Có cần đặt thêm câu hỏi nào khác để hoàn thiện Lean Teamwork không? Có cơ chế/quy trình nào đã qua nhiều lần cải tiến mà vẫn chưa đạt độ mượt mà tối ưu không?" -> Subagent tự trả lời câu hỏi đó và hành động xử lý dứt điểm ngay lập tức.*

### 3. Cơ Chế Tinh Lọc, Nén & Tỉa Bỏ (Pruning & Compaction Mechanism)
- **Quy Tắc Hợp Nhất (Consolidation Rule)**: Khi xuất hiện một bài học mới có cùng bản chất với bài học cũ, Subagent bắt buộc phải hợp nhất thành một nguyên lý tổng quát (General Pattern), cấm ghi thành các dòng rời rạc.
- **Giới Hạn Dung Lượng Kho Tri Thức (Knowledge Upper Bound)**: Kho `docs/learned_patterns.md` và toàn cục chỉ lưu giữ tối đa 10 patterns tinh hoa súc tích. Những bài học đã được chuyển hoá thành code logic trong `sync_skill.py` hoặc hook tự động sẽ được tỉa bỏ (pruned) khỏi file text.
- **Nâng Cấp Ngược Lại Tooling**: Kết quả trả lời của Q3, Q4 và Q6 được ưu tiên hiện thực hoá thành các tiện ích tự động hóa trong script thay vì bắt AI phải nhớ trong đầu dưới dạng text rule.

---

## 10. Giải Phẫu Thực Nghiệm: Loại Bỏ Ràng Buộc Đếm Dòng Cơ Học & Chuẩn Hóa Context-Aware Inspection (Case Study Serene-Bose & Antigravity Widget)

### 1. Hiện Tượng Thực Tế
- **Case Serene-Bose**: AI đọc vụn vặt từng đoạn ngắn 50 dòng chắp vá không đủ ngữ cảnh, dẫn đến grep lòng vòng tốn hơn 30 tool calls.
- **Case Antigravity Widget**: Khi áp đặt quy tắc cứng nhắc đếm dòng ("bắt buộc đọc 100–400 dòng", "cấm đọc dưới 50 dòng"), AI bị rối loạn biên độ đọc trong các session dài, dẫn đến kẹt lặp vô tận đúng 1 đoạn 15 dòng hàng chục lần.

### 2. Bài Học Cốt Tử: Khai Tử Ràng Buộc Đếm Dòng Cơ Học (No Rigid Line-Count Constraints)
- Việc trói buộc AI bằng các con số đếm dòng cơ học (50 dòng hay 100–400 dòng) là một Anti-Pattern tai hại. Mỗi hàm, class hoặc file có cấu trúc và độ dài hoàn toàn khác nhau.
- Ép buộc con số cơ học biến AI thành công cụ máy móc, gây xung đột nhận thức và triệt tiêu khả năng phán đoán ngữ cảnh linh hoạt.

### 3. Thiết Lập Chuẩn: Context-Aware Inspection & First-Time Right
- **Định nghĩa đúng của "Lean"**: Lean là **Trúng Đích & Đủ Ngữ Cảnh (Targeted & Context-Aware)**, hoàn toàn không phải là đếm số dòng cơ học.
- **Chuẩn thực thi First-Time Right**: Khi đã xác định file và khu vực logic cần kiểm tra, BẮT BUỘC đọc bao quát trọn vẹn ngữ cảnh hàm/class/block liên quan trong 1 lần gọi công cụ để hiểu rõ nguyên nhân gốc ngay từ đầu, tuyệt đối cấm đoán mò vì sợ đọc code/tài liệu.


