# Tham Chiếu: 4 Trụ Cột Lean Multi-Agent Protocol

1. **Subagent Cap**: Tối đa 2–4 subagents thiết yếu (1 Lead, 2 Workers, 1 Gatekeeper).
2. **Model Tiering**:
   - `flash` / `flash_lite`: Khảo sát, đọc log, chạy test, audit.
   - `inherit` / `pro`: Lead Orchestrator, Worker viết thuật toán phức tạp.
3. **Compact Handoff**: Mọi báo cáo giữa các agent bắt buộc dưới 20 dòng. Không dump thô log/schema vào context.
4. **Zero-Spawn Minor Remediation**: Tự sửa lỗi cú pháp vi mô trong minimal diff; không spawn subagent sửa lỗi lặt vặt.
