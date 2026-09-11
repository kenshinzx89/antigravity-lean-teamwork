# Kiến Trúc Multi-Agent Reliability & Evidence Gates

## 1. Quyết Định Kiến Trúc Cốt Lõi

Trong các hệ thống AI Agent phức tạp, **không sử dụng cơ chế "Bầu chọn đa số rồi lặp vô tận" (Majority voting without external ground truth)** để nghiệm thu kết quả. Các mô hình cùng họ có thể chia sẻ điểm mù chung, dẫn đến sự đồng thuận sai lệch nhưng rất tự tin, đồng thời vòng lặp vô hạn làm cạn kiệt token mà không sinh thêm bằng chứng mới.

Thay vào đó, hệ thống áp dụng kiến trúc:
**Execution Brief được phê duyệt đóng băng (Frozen Approved Brief) + Các cổng bằng chứng độc lập (Independent Evidence Gates)**.

```text
User (Lập trình viên)
  └── Intent Architect (Vai trò duy nhất được phép làm rõ yêu cầu với User)
        └── Approved Execution Brief (Đặc tả đã được duyệt và khóa scope)
              └── Orchestrator (Điều phối viên chính)
                    ├── Explorer (Read-only, Model: flash: Khảo sát repo, cấu trúc & rủi ro)
                    ├── Workers (Tối đa 2 Workers, Model: inherit/pro: Viết code trên module độc quyền)
                    └── Gatekeeper / Independent Auditor (Model: flash: Kiểm tra test thực tế & review diff)
  └── Trả kết quả đã xác thực về User kèm bằng chứng khách quan
```

---

## 2. Nguyên Tắc Phân Tách: Stock AGI & Lean Teamwork Skill

1. **Stock Antigravity AGI (Hệ thống nguyên bản trên máy tính)**:
   - Toàn bộ cấu hình toàn cục (`GEMINI.md`) được giữ nguyên bản sạch sẽ: kỷ luật Single Agent mặc định, minimal diff, verification-first.
   - Không hardcode hoặc inject quy tắc Teamwork vào nhân hệ thống nhằm giữ tốc độ cao nhất và tránh hao tổn quota cho các tác vụ 1-3 files.

2. **Lean Teamwork Protocol (Custom Skill độc lập của dự án)**:
   - Đóng gói trọn vẹn trong thư mục `.agents/skills/lean-teamwork/` của dự án.
   - Chỉ được kích hoạt có chủ đích (On-demand) khi đối mặt với bài toán lớn, kiến trúc chưa rõ ràng hoặc refactor đa module.
   - Áp dụng các chốt chặn: Subagent Cap (2-4), Model Tiering (`flash` cho explorer/auditor, `inherit` cho coder), Timeout Best-Path Fallback (150s), và Nghiệm thu độc lập qua Gatekeeper.

---

## 3. Hợp Đồng Chi Tiết Giữa Các Vai Trò (Role Contracts)

### 1. Intent Architect (Giao tiếp với User)
- **Nhiệm vụ**: Phỏng vấn người dùng để tạo và khóa bản `Execution Brief`.
- **Ranh giới**: Không viết code. Chỉ hỏi những câu hỏi có ảnh hưởng cốt lõi (Public contract, CSDL, Auth, Acceptance Criteria).
- **Nguyên tắc**: Sau khi người dùng duyệt brief, nội dung brief trở thành bất biến. Nếu có thay đổi, phải tạo bản sửa đổi `v<N+1>` được người dùng xác nhận.

### 2. Explorer (Khảo sát Read-only)
- **Model Tier**: `flash` hoặc `flash_lite`.
- **Nhiệm vụ**: Khảo sát repository, lập bản đồ các điểm vào (entry points), các file bị ảnh hưởng, các ràng buộc và rủi ro.
- **Ranh giới**: Không được chỉnh sửa code hoặc tự ý mở rộng phạm vi.

### 3. Worker (Chủ sở hữu triển khai mã nguồn)
- **Model Tier**: `inherit` hoặc `pro`.
- **Nhiệm vụ**: Triển khai mã nguồn chính xác theo Execution Brief.
- **Ranh giới**: Chỉ can thiệp vào danh sách file độc quyền được giao (File Ownership). Báo cáo kết quả bằng output thực tế; sự tự tin bằng lời nói không được tính là bằng chứng.

### 4. Gatekeeper / Independent Auditor (Cổng nghiệm thu bằng chứng)
- **Model Tier**: `flash` hoặc `flash_lite`.
- **Nhiệm vụ**: Kiểm tra output lệnh thực tế, chạy test độc lập, bảo đảm test không bị mock giả tạo.
- **Tối ưu Quota**: Gộp khâu Code Review, Test Check và Forensic Audit vào 1 Gatekeeper duy nhất chạy bằng model tier nhẹ.

---

## 3. Cơ Sở Nghiên Cứu Khoa Học

- **Antigravity Teamwork Architecture**: Dựa trên quy chuẩn chính thức của Google Antigravity về cách ly workspace, quyền sở hữu file phân tầng và tạo artifact nghiệm thu: [Antigravity Teamwork](https://antigravity.google/docs/teamwork/).
- **Multi-Agent Debate Limitations**: Nghiên cứu chỉ ra rằng việc tranh luận giữa các agent mà không có bằng chứng từ công cụ bên ngoài dễ dẫn đến ảo giác tập thể (*Shared Priors*). Vì vậy, hệ thống bắt buộc sử dụng bằng chứng khách quan từ test runner và terminal output thay vì biểu quyết (Tham khảo: [Improving Factuality and Reasoning through Multiagent Debate](https://arxiv.org/abs/2305.19118)).
- **Bounded Iterative Reflection**: Tự phản biện chỉ có ý nghĩa khi có phản hồi chứa giá trị thông tin thực (test fails, compiler errors, linter output). Xem thêm: [Reflexion (Shinn et al.)](https://arxiv.org/abs/2303.11366) và [Self-Refine (Madaan et al.)](https://arxiv.org/abs/2303.17651).
