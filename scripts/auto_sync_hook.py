#!/usr/bin/env python3
"""
Antigravity PreInvocation Lifecycle Hook
Tự động kiểm tra và cân bằng phiên bản 2 chiều giữa folder gốc và máy tính ngầm.
Hoàn toàn tự động, người dùng không cần gõ bất kỳ câu lệnh nào!
"""

import sys
import json
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

def main():
    sync_occurred = False
    active_version = "1.0.0"

    try:
        import sync_skill
        src_v = sync_skill.get_source_version()
        inst_v = sync_skill.get_installed_version()
        active_version = src_v

        src_tuple = sync_skill.parse_semver(src_v)
        inst_tuple = sync_skill.parse_semver(inst_v)

        # Kiểm tra xem có lệch version không
        if src_tuple != inst_tuple:
            sync_skill.auto_smart_sync()
            sync_occurred = True
        else:
            # Kiểm tra nhanh xem patterns có lệch nhau không
            src_p = REPO_ROOT / "docs" / "learned_patterns.md"
            dst_p = sync_skill.GLOBAL_CONFIG_DIR / "learned_patterns.md"
            if src_p.exists() and dst_p.exists():
                if src_p.stat().st_size != dst_p.stat().st_size:
                    sync_skill.bidirectional_merge_patterns()
                    sync_occurred = True
    except Exception as e:
        pass

    anchor_msg = (
        f"⚡ [MANDATORY RE-ANCHOR — Lean Teamwork v{active_version}]:\n"
        "1. 🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡: Khi mở đầu hoặc chọn giải pháp, dùng modal ask_question có tiền tố tiêu đề '🧭 [ĐỀ XUẤT KỸ THUẬT]' gồm 2–4 lựa chọn kèm (Recommended). Hạn 2.5 phút: nếu user chưa chọn, tự động chọn hướng tối ưu để làm tiếp, tránh đứt đoạn.\n"
        "2. 💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨: Khi code xong và test pass (exit 0), BẮT BUỘC gọi modal ask_question có tiền tố tiêu đề '💎 [NGHIỆM THU HOÀN THIỆN]' (💎 [100% HOÀN TẤT] ✨ vs ⚡ [SUPERPOWERS DEBUG] 🛠️), TREO CỐ ĐỊNH VĨNH VIỄN (KHÔNG TIMEOUT) để chờ user đối chứng thực tế và rà soát học tập.\n"
        "3. FIRST-TIME RIGHT: Inspect First kỹ lưỡng trước khi sửa, cấm đoán mò vì sợ đọc tài liệu."
    )
    if sync_occurred:
        anchor_msg = f"🔄 [AUTO-SYNC]: Đã đồng bộ 2 chiều ngầm v{active_version}.\n" + anchor_msg

    response = {
        "injectSteps": [
            {
                "ephemeralMessage": anchor_msg
            }
        ]
    }

    sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
    sys.stdout.flush()
    sys.exit(0)

if __name__ == "__main__":
    main()
