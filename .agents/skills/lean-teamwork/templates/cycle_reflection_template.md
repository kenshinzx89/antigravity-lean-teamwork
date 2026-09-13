### Cycle Reflection & Quota Audit (Sau mỗi vòng thực thi)

```markdown
#### [CYCLE AUDIT #<N>]
1. **Turn Budget & Churn Analysis (Kiểm toán thử - sai & số lượt)**:
   - Tổng số lượt chat (Turns) đã tiêu tốn cho task này: <N> (Mục tiêu: ≤ 2 lượt).
   - Có bị thử - sai / đổi hướng giải pháp không? [CÓ / KHÔNG]
   - Nếu CÓ: Tại sao? Có phải do ĐOÁN MÒ vì thiếu tài liệu API/kiến trúc gốc không?
   - Đánh giá First-Time Right: [ĐẠT (1-2 lượt) / HỎNG (Thử sai nhiều lần)]

2. **Quota / Token Analysis**:
   - Files read: <Số lượng file đã đọc> (Có đọc đúng tài liệu có thẩm quyền cao nhất không?)
   - Terminal/Diff output: <Ngắn gọn / Dài dòng?>
   - Tiết kiệm token cho vòng kế tiếp: <Cách rút ngắn context / lệnh test>

3. **Evidence & Anti-Rationalization Check (Superpowers Rule)**:
   - Đã có exit code 0 / kết quả trực tiếp chưa? [CÓ / CHƯA]
   - Bằng chứng: `<command> -> <output summary>`
   - Cảnh báo đỏ: Có dùng từ phỏng đoán ("should work", "probably", "looks correct") không? [KHÔNG]

4. **Ruling & Anti-Pattern Log**:
   - Có phát hiện Anti-Pattern (đoán mò, thiếu tài liệu, options rỗng) không?
   - Bài học rút ra để không lặp lại: `<...>`

5. **Multi-Cycle Skill Usage Audit (Rà soát kỹ năng qua 3–4 chu kỳ & Tắt bớt để tiết kiệm Context)**:
   - Các skill đã dùng thực tế qua 3–4 chu kỳ gần nhất: `<danh sách>`
   - Các skill thừa / lệch tech-stack đã cất vào `skills_archive`: `<danh sách>`
   - Lệnh khôi phục khi cần: `py scripts/manage_skills.py --restore <tên_skill>`
```

