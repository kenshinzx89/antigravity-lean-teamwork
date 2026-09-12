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
    anchor_msg = (
        f'⚡ [MANDATORY RE-ANCHOR — Lean Teamwork v{ver}]:\\n'
        '1. 🧭 [CHẾ ĐỘ ĐỀ XUẤT KỸ THUẬT] 💡: Khi mở đầu hoặc chọn giải pháp, dùng modal ask_question có tiền tố tiêu đề \\'🧭 [ĐỀ XUẤT KỸ THUẬT]\\' gồm 2–4 lựa chọn kèm (Recommended). Hạn 2.5 phút: nếu user chưa chọn, tự động chọn hướng tối ưu để làm tiếp, tránh đứt đoạn.\\n'
        '2. 💎 [CHẾ ĐỘ NGHIỆM THU HOÀN THIỆN] ✨ (TÁCH NHỊP 2 BƯỚC v1.4.2): Khi code xong và test pass (exit 0): '
        'BƯỚC 1: BẮT BUỘC in toàn văn Báo cáo & Hướng dẫn đối chứng ra màn hình, TUYỆT ĐỐI KHÔNG gọi ask_question cùng lúc làm che mất chữ. '
        'BƯỚC 2: Chờ user đọc xong và phản hồi, sau đó MỚI gọi modal ask_question \\'💎 [NGHIỆM THU HOÀN THIỆN]\\' (💎 [100% HOÀN TẤT] ✨ vs ⚡ [SUPERPOWERS DEBUG] 🛠️) để user xác nhận an toàn.\\n'
        '3. FIRST-TIME RIGHT & COHESIVE INSPECTION: Inspect First đọc trọn vẹn khối chức năng liên quan (100–400 dòng trong 1 lần view_file). CẤM đọc vụn 50 dòng (Micro-Peeking), cấm đoán mò vì sợ tốn token.'
    )

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
hooks_json_content = '''{
  "lean-teamwork-global-reanchor": {
    "PreInvocation": [
      {
        "type": "command",
        "command": "py scripts/auto_reanchor_hook.py",
        "timeout": 10
      }
    ]
  }
}
'''
hooks_json.write_text(hooks_json_content, encoding='utf-8')
print('SUCCESS: Created global hook and script at', GLOBAL_CONFIG_DIR)
