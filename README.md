<p align="center">
  <img src="assets/demo.gif" alt="Antigravity Lean Teamwork Live Demo" width="100%">
</p>

<p align="center">
  <a href="https://github.com/kenshinzx89/antigravity-lean-teamwork"><img src="https://img.shields.io/badge/target-Google%20Antigravity%20(Gemini%203.7%2F3.8)-4285F4.svg?style=for-the-badge&logo=google" alt="Google Antigravity Only"></a>
  <a href="https://github.com/kenshinzx89/antigravity-lean-teamwork"><img src="https://img.shields.io/badge/role-Phanh%20H%C3%A3m%20%E1%BA%A8u%20ABS-FF6D00.svg?style=for-the-badge" alt="Phanh Hãm Ẩu ABS"></a>
  <a href="https://github.com/kenshinzx89/antigravity-lean-teamwork"><img src="https://img.shields.io/badge/version-1.5.8-00C853.svg?style=for-the-badge" alt="Version"></a>
  <a href="https://github.com/kenshinzx89/antigravity-lean-teamwork"><img src="https://img.shields.io/badge/tests-18%2F18%20passing-brightgreen.svg?style=for-the-badge" alt="Tests"></a>
  <a href="https://github.com/kenshinzx89/antigravity-lean-teamwork"><img src="https://img.shields.io/badge/license-MIT-purple.svg?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <b>⚡ Bộ Đôi Kỹ Năng Tinh Gọn + Desktop Widget HUD Dành Riêng Cho Google Antigravity.</b><br/>
  <i>Giải phóng 100% khung chat, đưa đề xuất & nghiệm thu ra thanh kính mờ HUD ngoài màn hình. Chữa dứt điểm tật làm ẩu và cãi cọ với AI.</i>
</p>

---

> [!IMPORTANT]
> ### 📢 LƯU Ý ĐẶC BIỆT DÀNH CHO BẠN (DỰ ÁN XÂY DỰNG 100% TỰ ĐỘNG BỞI AI)
>
> 🤖 **100% AI-Native Development & Tự Động Git Push**:
> Toàn bộ mã nguồn, tính năng Desktop Widget HUD, hệ thống lifecycle hook và các bản cập nhật trên repo này đều do **AI (Antigravity Agent)** tự động lập trình, tự chạy kiểm thử và tự động `git push` trực tiếp trong quá trình pair-programming thực tế cùng tác giả.
>
> 💻 **Được Phát Triển Trên Môi Trường Thực Tế Của Tác Giả**:
> - Vì được AI tự động build, test live và push liên tục trên máy tính thực tế của tác giả (đôi khi máy hơi lag nhẹ khi chạy nhiều tiến trình ngầm cùng lúc), một số cấu hình thư mục, file khởi động hoặc shortcut ban đầu mang các giá trị mặc định của máy gốc.
> - **Khi bạn đem repo này về máy của mình: Bạn KHÔNG CẦN phải tự sửa tay bằng mắt!**
>
> 🚀 **Cách Tốt Nhất: Hãy Kêu Chính AI Của Bạn Tự Tối Ưu Lại Cho Vừa Khít Máy Bạn**:
> Khi tải repo này về máy tính mới hoặc laptop của bạn, bạn chỉ cần mở thư mục này trong **Antigravity IDE** (hoặc công cụ AI coding agent mà bạn dùng) và ra lệnh:
>
> > 💬 *"Dự án này được build tự động trên máy khác. Hãy kiểm tra lại toàn bộ đường dẫn, môi trường khởi động trên máy tính của tôi, tối ưu và cài đặt hoàn thiện để chạy mượt mà 100% trên máy này!"*
>
> AI trên máy của bạn sẽ tự động đọc [`AGENTS.md`](AGENTS.md) / [`GEMINI.md`](GEMINI.md), nhận diện phiên bản Python, đường dẫn người dùng trên máy bạn và tự động chạy lệnh cài đặt hoàn chỉnh từ A -> Z!
>
> ⚡ **Hoặc bạn có thể tự kích hoạt nhanh trong 5 giây**:
> ```powershell
> powershell -ExecutionPolicy Bypass -File .\install.ps1
> ```

---

## ⚡ Cài Đặt Cho Máy Mới Trong 5 Giây (1-Click Install)

> 💡 **Với Máy Mới**: Bạn chỉ cần tải repo về, mở trong Antigravity IDE và chat duy nhất một câu:  
> **"Hãy cài và sử dụng cho tôi"** (hoặc chạy lệnh PowerShell 1-Click bên dưới):

```powershell
# Chạy duy nhất lệnh này sau khi tải về để cài đặt toàn bộ:
powershell -ExecutionPolicy Bypass -File .\install.ps1
```
*Xem hướng dẫn đầy đủ từ A -> Z tại [INSTALL.md](INSTALL.md).*

---

> [!NOTE]
> ### 🎯 SỰ THẬT ĐẰNG SAU BỘ KỸ NĂNG NÀY (THE NAKED TRUTH)
> 
> - 🏎️ **Tại sao lại cần Lean Teamwork?**  
>   Gemini 3.7 và 3.8 trên Google Antigravity có tốc độ tư duy và phản hồi cực kỳ nhanh, nhưng cái tật cố hữu là **"quá nhanh quá nguy hiểm"**:
>   - **Hay làm ẩu**: Lười đọc tài liệu/mã nguồn gốc ở lượt đầu vì sợ tốn token, dẫn đến đoán mò.
>   - **Gây ức chế**: Đoán mò thì code lỗi, khiến **người dùng phải cãi lộn với AI**, bực bội bắt AI sửa đi sửa lại 5–10 lượt chat.
>   - **Lean Teamwork chính là chiếc "phanh ABS"**: Buộc AI phải **Inspect First** (đọc kỹ trước khi sửa), đưa đề xuất ra **Desktop Widget Popover HUD**, kiểm thử độc lập phải đạt **Exit Code 0**, và chỉ kết thúc khi người dùng bấm **💎 Nghiệm Thu Hoàn Thiện**.
>
> - 💡 **Tại sao không nên dùng cho Cursor, Claude Code hay Codex?**  
>   Không phải vì có bí mật kỹ thuật gì cao siêu, mà thực tế là: **Chỉ có Gemini 3.7 / 3.8 bị cái tật "hấp tấp, làm ẩu" này nên mới cần lắp nhiều cơ chế hãm vâu như vậy!**  
>   Các mô hình như Claude 3.7 Sonnet hay OpenAI Codex vốn dĩ đã có sẵn cơ chế suy nghĩ chậm rãi, điềm đạm trong harness của chúng rồi. Đem bộ phanh này lắp sang bên đó chỉ tổ thừa thãi, cồng kềnh và không cần thiết.

---

## ⚡ Trải Nghiệm Thực Tế (Zero-Scan Đồng Bộ Trong 1.5 Giây)

```shell
$ py sync_skill.py
[SMART-SYNC] Kiểm tra phiên bản:
  • Folder gốc (Source):   v1.5.0
  • Máy tính (Installed):  v1.5.0

⚡ [HƯỚNG: SYNC 2 CHIỀU] Hai bên đồng phiên bản (v1.5.0). Kiểm tra và cân bằng tri thức...
  ✓ [PULL] Đã đồng bộ SKILL.md vào Global Config
  ✓ [PULL] Đã đồng bộ templates/ & references/
  ✓ [PULL] Đã ghi VERSION 1.5.0 vào ~/.gemini/config/skills/lean-teamwork
  ✓ Đã thiết lập Global PreInvocation Hook tại ~/.gemini/config/hooks.json
  ✓ Cân bằng 2 chiều tri thức thành công (19 patterns tại cả 2 nơi).
  ⏳ Đang chạy kiểm thử toàn vẹn hệ thống...
  ✓ Toàn bộ 11/11 kiểm thử hệ thống đạt 100% PASS (Exit Code 0).

============================================================
[SUCCESS] Lean Teamwork v1.5.0 đã đồng bộ 2 chiều hoàn hảo!
============================================================
```

---

## 🏛️ Sơ Đồ Kiến Trúc Hệ Thống (Lấy Cảm Hứng Từ Archify Pipeline)

```mermaid
flowchart TD
    subgraph INVOCATION ["1. TỰ ĐỘNG RE-ANCHOR (PRE-INVOCATION HOOK)"]
        A[Lượt Chat Của Agent Bắt Đầu] --> B[scripts/auto_sync_hook.py]
        B -->|Tiêm Ngầm Chống Quên Luật| C["⚡ MANDATORY RE-ANCHOR<br/>(Chống trôi ngữ cảnh 100%)"]
    end

    subgraph PROPOSAL ["2. CỔNG ĐỀ XUẤT KỸ THUẬT (2.5 PHÚT)"]
        C --> D["🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] ⏱️<br/>Modal 2–4 lựa chọn kèm (Recommended)"]
        D -->|Người Dùng Chọn Hoặc Tự Chạy Sau 2.5m| E["Inspect First: Đọc Kỹ Tài Liệu Gốc<br/>(Triệt tiêu đoán mò ngay Turn 1)"]
    end

    subgraph VERIFICATION ["3. THI HÀNH & CỔNG NGHIỆM THU TREO"]
        E -->|Viết Code & Chạy Kiểm Thử| F["Exit Code 0 Thực Nghiệm<br/>(Cấm dùng từ phỏng đoán)"]
        F --> G["💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨<br/>Modal Treo Vĩnh Viễn (KHÔNG TIMEOUT)"]
    end

    subgraph EVOLUTION ["4. TỰ VẤN 5 CHIỀU & KHỬ PHÌNH TRI THỨC"]
        G -->|Người Dùng Bấm 100% Hoàn Tất| H["Subagent: Knowledge Synthesizer (Flash)"]
        H --> I["❓ Tự Vấn 5 Chiều<br/>(Root Cause, First-Time Right, Token, Velocity, Pruning)"]
        I --> J["✂️ Nén & Tỉa Quy Tắc Cũ Thừa<br/>(Khóa trần tối đa 10 Patterns)"]
        J --> K["Kho Tri Thức Ngoài: docs/learned_patterns.md<br/>(SKILL.md Giữ Sạch <150 Dòng)"]
        K --> L["Đồng Bộ 2 Chiều: py sync_skill.py"]
    end

    style INVOCATION fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#fff
    style PROPOSAL fill:#1e293b,stroke:#f59e0b,stroke-width:2px,color:#fff
    style VERIFICATION fill:#1e293b,stroke:#10b981,stroke-width:2px,color:#fff
    style EVOLUTION fill:#1e293b,stroke:#8b5cf6,stroke-width:2px,color:#fff
```

---

## 💥 So Sánh Hiệu Năng Thực Chiến: Dập Tắt Lãng Phí Token

| Vấn Đề Thường Gặp | Khi Dùng Antigravity Mộc | Khi Dùng Lean Teamwork |
| :--- | :--- | :--- |
| **Tâm lý khởi đầu** | Sợ tốn token nên không đọc tài liệu, bắt tay vào đoán mò ngay | **Inspect First**: Đọc chuẩn tài liệu gốc 1 lần, làm trúng đích ngay lần 1 |
| **Số lượt chat để fix bug** | 5 – 10 lượt (Sửa sai -> Bị chửi -> Sửa tiếp -> Lại sai) | **1 – 2 lượt** (Có test case tái hiện & pass exit code 0 mới báo cáo) |
| **Cảm xúc người dùng** | Ức chế, cãi cọ với AI, tốn thời gian giải thích lại | Thảnh thơi: Chọn phương án đề xuất 🧭 và test thực tế nghiệm thu 💎 |
| **Nguy cơ trôi ngữ cảnh** | Sau 10 lượt chat thì AI quên sạch các luật ban đầu | **0% Drift**: Hook ngầm re-anchor liên tục trước mỗi lượt gọi |
| **Tập quy tắc sau 1 tháng** | Phình to hàng nghìn dòng, AI bị quá tải nhận thức, lú lẫn | **Khóa trần < 10 patterns tinh hoa**: Tự động gộp và tỉa bỏ quy tắc cũ thừa |
| **Cài lên máy mới / laptop** | Mất 15–30 phút copy paste và cấu hình | **1.5 giây**: Chạy đúng 1 lệnh `py sync_skill.py` là xong |

---

## ✨ 4 Trụ Cột Vận Hành Cốt Lõi

### 1. ⚡ Zero-Touch PreInvocation Lifecycle Hooks
Chạy tự động ngầm trước **từng lượt gọi model** thông qua `.agents/hooks.json` và `~/.gemini/config/hooks.json`, tiêm chỉ dẫn định vị để AI không bao giờ quên cổng kiểm soát.

### 2. 🧭 Chuẩn Modal Đối Lập Trực Quan (Dual-Modal Paradigm)
- **🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] ⏱️ [HẠN 2.5 PHÚT] 💡**: Dành cho khởi đầu bài toán hoặc chọn ngã rẽ giải pháp. Có đếm ngược 2.5 phút tự chọn `(Recommended)` nếu người dùng bận, tránh tắc nghẽn tiến độ.
- **💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨**: Dành cho nghiệm thu khi test đã pass 100%. **Treo cố định vĩnh viễn (KHÔNG ĐẾM NGƯỢC)** để người dùng thong thả đối chứng thực tế trên máy thật.

### 3. 🧠 Bộ Tự Vấn Phản Tư 6 Chiều & Cơ Chế Khử Phình Tri Thức
Sau khi nghiệm thu, Subagent không ghi chép bừa bãi mà tự trả lời 6 câu hỏi cốt lõi:
- **Q1 (Root Cause)**: *Tại sao lần trước phải làm lại?*
- **Q2 (First-Time Right)**: *Làm sao để lần sau làm chuẩn xác 100% ngay từ lượt 1?*
- **Q3 (Token Economy)**: *Có bước nào làm lãng phí token không? Cắt giảm ra sao?*
- **Q4 (Velocity & Automation)**: *Có thể tự động hóa quy tắc này thành code/hook để chạy nhanh hơn không?*
- **Q5 (Rule Pruning & Anti-Bloat)**: *Có bài học/quy tắc cũ nào thừa hoặc trùng lặp cần GỘP (Merge) hoặc XÓA (Prune) để giữ bộ não AI luôn nhẹ?*
- **Q6 (Meta-Questioning & Chronic Bottlenecks)**: *Có cần đặt thêm câu hỏi nào khác để hoàn thiện Lean Teamwork không? Có cơ chế/quy trình nào đã cải tiến nhiều lần mà vẫn chưa thực sự ngon không? -> Tự trả lời và hành động sửa dứt điểm ngay!*

### 4. 🔄 Đồng Bộ Tự Thích Ứng 2 Chiều (`sync_skill.py`)
Tự động so sánh phiên bản:
- Nếu Folder gốc mới hơn: Tự động **PULL** vào máy tính.
- Nếu Máy tính vừa học hỏi kiến thức mới: Tự động **PUSH** ngược về folder gốc để PC dùng ngay.
- Cân bằng tri thức 2 chiều trong 1.5 giây, đạt 100% PASS kiểm thử toàn vẹn.

---

## 💡 Cách Dùng Đơn Giản Nhất: "Dạy Một Lần — Tự Học Suốt Đời"

Không cần cấu hình phức tạp, bạn chỉ cần thực hiện 3 bước:

### 1. Tải Về & Mở Workspace
Tải repo này về máy và mở thư mục `antigravity-lean-teamwork` trong Google Antigravity.

### 2. Nói Đúng 1 Câu Với AI
Trong khung chat Antigravity, bạn chỉ cần gõ đúng 1 câu:
> 🗣️ **"Từ nay xài skill Lean Teamwork này nhé"**  
> *(hoặc gõ ngắn gọn: `"update"`, `"cập nhật"`, hay `"áp dụng skill"`)*

AI sẽ tự động chạy lệnh `py sync_skill.py`, tự nạp bộ phanh hãm ẩu, kích hoạt hook toàn cục và chạy bộ test 10/10 PASS trong đúng **1.5 giây**.

### 3. Điều Kỳ Diệu: Kỹ Năng Tự Phát Triển & Tự Học Theo Quá Trình Làm Việc
Điểm đột phá nhất của Lean Teamwork không phải là một tập quy tắc tĩnh:
- **Tự học hỏi sau mỗi task**: Mỗi khi bạn bấm nghiệm thu (`💎 [100% HOÀN TẤT] ✨`), Subagent sẽ tự động chạy chu trình **Tự Vấn Phản Tư 5 Chiều** để tự mổ xẻ: *Tại sao có bước phải làm lại? Có thao tác nào lãng phí token không? Làm sao để lần sau làm chuẩn xác 100% ngay từ lượt 1?*
- **Càng dùng càng khôn mà KHÔNG bị phình to quy tắc**: Nó tự động nén tri thức vào kho ngoài, tự động **GỘP (Merge)** bài học tương đồng và **TỈA BỎ (Prune)** quy tắc cũ thừa, giúp AI không bao giờ bị quá tải nhận thức.
- **Tự động lan tỏa giữa các thiết bị**: Mọi bài học AI tự đúc kết được trên Laptop sẽ tự động PUSH về folder gốc để PC dùng ngay mà không cần cài đặt lại!

---

## ⚡ Hướng Dẫn Kỹ Thuật (Dành Cho Nhà Phát Triển)

### Cài Đặt / Cập Nhật Thủ Công (1 Giây)
```bash
git clone https://github.com/kenshinzx89/antigravity-lean-teamwork.git
cd antigravity-lean-teamwork

# Chạy lệnh duy nhất (Cài core, cấu hình hook, chạy 10/10 test)
py sync_skill.py
```

### Chạy Kiểm Thử Toàn Vẹn Hệ Thống (10/10 Checks)
```bash
py tests/test_skill_integrity.py
```

### Tự Động Tăng Phiên Bản Khi Có Cải Tiến Mới
```bash
# Tăng bản vá (Patch)
py sync_skill.py --bump patch

# Tăng phiên bản phương pháp luận (Minor)
py sync_skill.py --bump minor
```

---

## 📁 Cấu Trúc Dự Án

```text
antigravity-lean-teamwork/
├── .agents/
│   ├── hooks.json                     # Hook vòng đời PreInvocation cấp dự án
│   └── skills/
│       └── lean-teamwork/
│           ├── SKILL.md               # Bộ luật điều phối tinh gọn (<150 dòng)
│           ├── references/            # Tài liệu tham chiếu sâu (Superpowers, Debugging)
│           └── templates/             # Các mẫu brief, cycle audit, evaluation panel
├── .github/
│   ├── ISSUE_TEMPLATE/                # Form tương tác báo lỗi & đề xuất tính năng
│   ├── workflows/
│   │   └── ci.yml                     # Pipeline CI tự động test trên Windows & Ubuntu
│   └── pull_request_template.md       # Checklist kiểm thử bắt buộc trước khi merge
├── assets/
│   └── banner.jpg                     # Ảnh Hero Banner đồ họa chất lượng cao
├── docs/
│   ├── learned_patterns.md            # Kho tri thức ngoài (Khóa trần tối đa 10 patterns)
│   ├── self-evolution.md              # Đặc tả Tự Vấn 5 Chiều & Khử Phình Quy Tắc
│   ├── comparative-study.md           # Nghiên cứu so sánh chi tiết
│   └── architecture.md                # Cấu trúc tách biệt Stock Core & Skill
├── scripts/
│   ├── auto_sync_hook.py              # Script hook tự động tiêm thông điệp Re-Anchor
│   ├── setup_global_hook.py           # Script cài đặt hook toàn cục trên máy tính
│   └── teamwork_bridge.py             # Cầu nối 2 chiều Lean Teamwork <-> Desktop Widget
├── tests/
│   ├── test_skill_integrity.py        # 11 bài test kiểm thử tính toàn vẹn hệ thống
│   └── test_teamwork_bridge.py        # 6 bài test kiểm thử cầu nối & fallback Native IDE
├── widget/                            # Mã nguồn Desktop Widget HUD kính mờ ngoài màn hình
│   ├── core/                          # Windows API GDI+, Popover, Service, Layout
│   ├── assets/                        # Icons, hình ảnh đồ họa chất lượng cao
│   ├── main.py                        # Điểm khởi chạy Widget
│   └── KHOI_DONG_WIDGET.vbs           # Lối tắt khởi động ngầm không hiện console
├── sync_skill.py                      # Bộ điều khiển Zero-Scan & Đồng bộ 2 chiều
├── install.ps1                        # Script cài đặt 1-click tự động toàn diện
├── INSTALL.md                         # Hướng dẫn cài đặt A-Z cho máy mới
├── AGENTS.md                          # Chỉ dẫn thi hành nhanh cho AI
├── CHANGELOG.md                       # Lịch sử nâng cấp phiên bản
├── CONTRIBUTING.md                    # Nguyên tắc đóng góp First-Time Right
├── GEMINI.md                          # Operating Rules cấp toàn cục
├── LICENSE                            # Giấy phép mã nguồn mở MIT
├── SECURITY.md                        # Chính sách bảo mật có trách nhiệm
└── VERSION                            # Số hiệu phiên bản hiện hành (v1.5.0)
```

---

## 📜 Giấy Phép (License)

Phát hành theo giấy phép **MIT License**. Xem chi tiết tại [`LICENSE`](./LICENSE).

---

<p align="center">
  <b>⭐ Gắn Star cho repo nếu nó giúp bạn không còn phải cãi lộn với Gemini 3.7 / 3.8 nữa! ⭐</b>
</p>
