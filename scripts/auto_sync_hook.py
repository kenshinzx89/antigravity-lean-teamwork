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

    # Tự động cấp sẵn đồng hồ macOS Spectrum 480x84 trong suốt vào thư mục brain của session
    cid = os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
    svg_img_tag = "![🧭 ĐỀ XUẤT KỸ THUẬT 💡](technical_proposal_timer.svg)"
    if cid:
        try:
            brain_dir = Path.home() / ".gemini" / "antigravity" / "brain" / cid
            brain_dir.mkdir(parents=True, exist_ok=True)
            dst_svg = brain_dir / "technical_proposal_timer.svg"
            src_svg = REPO_ROOT / ".agents" / "skills" / "lean-teamwork" / "resources" / "technical_proposal_timer.svg"
            if src_svg.exists():
                if not dst_svg.exists() or dst_svg.stat().st_size != src_svg.stat().st_size or 'fill="#0D1117"' in dst_svg.read_text(encoding="utf-8", errors="ignore"):
                    import shutil
                    shutil.copyfile(src_svg, dst_svg)
            svg_abs = dst_svg.as_posix()
            svg_img_tag = f"![🧭 ĐỀ XUẤT KỸ THUẬT 💡]({svg_abs})"
        except Exception:
            pass

    anchor_msg = (
        f"⚡ [MANDATORY RE-ANCHOR — Lean Teamwork v{active_version} (Widget HUD Decoupled)]:\n"
        "1. 🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡 (Widget HUD): Khi mở đầu hoặc chọn giải pháp kỹ thuật, BẮT BUỘC gọi teamwork_bridge.publish_proposal(title, options, 150) để hiển thị bộ chọn trên Desktop Widget Popover. In tóm tắt ra chat, TUYỆT ĐỐI KHÔNG gọi modal ask_question (giải phóng khung chat 100%).\n"
        "2. 💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨ (Widget HUD): Khi code xong và test pass (exit 0): BƯỚC 1 in toàn văn Báo cáo & Hướng dẫn đối chứng ra màn hình chat; BƯỚC 2 gọi teamwork_bridge.publish_acceptance(...) để treo bảng nghiệm thu cố định trên Desktop Widget Popover. TUYỆT ĐỐI KHÔNG gọi modal ask_question làm che khung chat, user sẽ bấm trực tiếp từ Desktop Widget.\n"
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
