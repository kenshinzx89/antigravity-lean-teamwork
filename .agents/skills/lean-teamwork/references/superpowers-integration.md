# Tích Hợp Tri Thức & Kinh Nghiệm Từ Superpowers Vào Lean Teamwork

## 1. 3 Thiết Luật Bất Biến (The 3 Iron Laws)

1. **Iron Law of Verification**: Không bao giờ tuyên bố hoàn thành nếu không có fresh verification output. Cấm dùng từ phỏng đoán.
2. **Iron Law of Root Cause**: Không sửa code khi chưa điều tra nguyên nhân gốc và tái hiện lỗi ổn định.
3. **Ruling, Not Stalls**: Tự ra phán quyết cho các vấn đề vi mô kèm ghi chú rủi ro (`Ruling: <Quyết định> — <Lý do> — <Hệ quả nếu sai>`).

## 2. Isolated Context Dispatching

Subagent chỉ nhận đúng Task Card với phạm vi file độc quyền, không kế thừa lịch sử chat session lớn của parent.

## 3. Red-Green Verification (TDD)

Viết test tái hiện lỗi -> Xác nhận FAIL -> Sửa code tối thiểu -> Xác nhận PASS.
