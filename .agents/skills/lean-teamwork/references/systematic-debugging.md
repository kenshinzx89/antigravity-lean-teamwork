# Cẩm Nang Systematic Debugging

1. **Pha 1: Root Cause Investigation**: Đọc kỹ stacktrace/mã lỗi, tái hiện lỗi ổn định, kiểm tra git diff gần nhất.
2. **Pha 2: Pattern Analysis**: So sánh với đoạn code đang chạy đúng, rà soát điều kiện biên.
3. **Pha 3: Hypothesis & Minimal Test**: Đưa ra giả thuyết và viết test kiểm chứng giả thuyết (Red phase).
4. **Pha 4: Minimal Fix & Verification**: Sửa trúng nguyên nhân trong minimal diff, chạy lại test (Green phase) và suite hồi quy.
