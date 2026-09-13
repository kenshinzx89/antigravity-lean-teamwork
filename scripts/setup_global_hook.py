import os
import sys
import json
from pathlib import Path

GLOBAL_CONFIG_DIR = Path(os.path.expanduser('~')) / '.gemini' / 'config'
GLOBAL_SCRIPTS_DIR = GLOBAL_CONFIG_DIR / 'scripts'
GLOBAL_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

hook_py = GLOBAL_SCRIPTS_DIR / 'auto_reanchor_hook.py'
hook_content = '''#!/usr/bin/env python3
"""
Antigravity Global PreInvocation Lifecycle Hook
Tự động tiêm thông điệp Re-Anchor tàng hình trước MỖI lượt gọi model ở mọi dự án.
Chống trôi ngữ cảnh (Anti-Context Drift) 100%, không bao giờ để AI quên hỏi và quên popup!
"""

import os
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CONFIG_DIR = Path(__file__).resolve().parent.parent
SKILL_VER_FILE = CONFIG_DIR / 'skills' / 'lean-teamwork' / 'VERSION'

def get_active_version():
    try:
        if SKILL_VER_FILE.exists():
            return SKILL_VER_FILE.read_text(encoding='utf-8').strip()
    except Exception:
        pass
    return '1.3.1'

def main():
    ver = get_active_version()

    # Tự động cấp sẵn đồng hồ macOS Spectrum 480x84 trong suốt vào thư mục brain của session
    cid = os.environ.get('ANTIGRAVITY_CONVERSATION_ID')
    svg_img_tag = '![🧭 ĐỀ XUẤT KỸ THUẬT 💡](technical_proposal_timer.svg)'
    if cid:
        try:
            brain_dir = Path.home() / '.gemini' / 'antigravity' / 'brain' / cid
            brain_dir.mkdir(parents=True, exist_ok=True)
            dst_svg = brain_dir / 'technical_proposal_timer.svg'
            src_svg = CONFIG_DIR / 'skills' / 'lean-teamwork' / 'resources' / 'technical_proposal_timer.svg'
            if src_svg.exists():
                if not dst_svg.exists() or dst_svg.stat().st_size != src_svg.stat().st_size or 'fill="#0D1117"' in dst_svg.read_text(encoding='utf-8', errors='ignore'):
                    import shutil
                    shutil.copyfile(src_svg, dst_svg)
            svg_abs = dst_svg.as_posix()
            svg_img_tag = f'![🧭 ĐỀ XUẤT KỸ THUẬT 💡]({svg_abs})'
        except Exception:
            pass

    # Kiểm tra phản hồi từ Antigravity Desktop Widget
    widget_event_msg = ""
    try:
        bridge_file = Path.home() / '.antigravity_cockpit' / 'teamwork_bridge.json'
        if bridge_file.exists():
            b_data = json.loads(bridge_file.read_text(encoding='utf-8'))
            resp = b_data.get('response')
            if resp and not resp.get('handled'):
                resp['handled'] = True
                b_data['response'] = resp
                bridge_file.write_text(json.dumps(b_data, ensure_ascii=False, indent=2), encoding='utf-8')
                act = resp.get('action')
                if act == 'SELECT_OPTION':
                    opt_id = resp.get('selected_option_id')
                    widget_event_msg = f"\\n\\n🖱️ [SỰ KIỆN TỪ WIDGET DESKTOP]: Người dùng vừa bấm CHỌN PHƯƠNG ÁN [{opt_id}] trực tiếp từ Antigravity Desktop Widget! Hãy thi hành ngay theo phương án này!"
                elif act == 'ACCEPT':
                    widget_event_msg = f"\\n\\n💎 [SỰ KIỆN TỪ WIDGET DESKTOP]: Người dùng vừa bấm [100% HOÀN TẤT - CHẤP THUẬN NGHIỆM THU] trên Desktop Widget! Hãy tổng kết và hoàn thành!"
                elif act == 'DEBUG':
                    widget_event_msg = f"\\n\\n⚡ [SỰ KIỆN TỪ WIDGET DESKTOP]: Người dùng vừa bấm [SUPERPOWERS DEBUG] trên Desktop Widget! Hãy rà soát sâu!"
    except Exception:
        pass

    anchor_msg = (
        f'⚡ [MANDATORY RE-ANCHOR — Lean Teamwork v{ver} (Widget HUD Decoupled)]:\\n'
        '1. 🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡 (Widget HUD): Khi mở đầu hoặc chọn giải pháp kỹ thuật, BẮT BUỘC gọi teamwork_bridge.publish_proposal(title, options, 150) để hiển thị bộ chọn trên Desktop Widget Popover. In tóm tắt ra chat, TUYỆT ĐỐI KHÔNG gọi modal ask_question (giải phóng khung chat 100%).\\n'
        '2. 💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨ (Widget HUD): Khi code xong và test pass (exit 0): BƯỚC 1 in toàn văn Báo cáo & Hướng dẫn đối chứng ra màn hình chat; BƯỚC 2 gọi teamwork_bridge.publish_acceptance(...) để treo bảng nghiệm thu cố định trên Desktop Widget Popover. TUYỆT ĐỐI KHÔNG gọi modal ask_question làm che khung chat, user sẽ bấm trực tiếp từ Desktop Widget.\\n'
        '3. FIRST-TIME RIGHT: Inspect First kỹ lưỡng trước khi sửa, cấm đoán mò vì sợ đọc tài liệu.'
    )
    if widget_event_msg:
        anchor_msg += widget_event_msg

    response = {
        'injectSteps': [
            {
                'ephemeralMessage': anchor_msg
            }
        ]
    }

    sys.stdout.write(json.dumps(response, ensure_ascii=False) + '\\n')
    sys.stdout.flush()
    sys.exit(0)

if __name__ == '__main__':
    main()
'''
hook_py.write_text(hook_content, encoding='utf-8')

hooks_json = GLOBAL_CONFIG_DIR / 'hooks.json'
py_exe = Path(sys.executable).as_posix()
hook_py_str = hook_py.as_posix()
hooks_json_data = {
    "lean-teamwork-global-reanchor": {
        "PreInvocation": [
            {
                "type": "command",
                "command": f'"{py_exe}" "{hook_py_str}"',
                "timeout": 10
            }
        ]
    }
}
hooks_json.write_text(json.dumps(hooks_json_data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'SUCCESS: Created universal global hook pointing to {py_exe} at {GLOBAL_CONFIG_DIR}')
