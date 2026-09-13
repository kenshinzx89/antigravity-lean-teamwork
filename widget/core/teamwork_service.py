# -*- coding: utf-8 -*-
"""
Teamwork Service for Antigravity Widget
Đọc và phản hồi trạng thái Lean Teamwork (Đề xuất kế hoạch & Nghiệm thu hoàn thiện).
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional

BRIDGE_DIR = Path.home() / '.antigravity_cockpit'
BRIDGE_FILE = BRIDGE_DIR / 'teamwork_bridge.json'


class TeamworkService:
    def __init__(self):
        self._last_mtime = 0.0
        self._cached_state: Dict[str, Any] = {
            "status": "IDLE",
            "session_id": "",
            "proposal": None,
            "acceptance": None,
            "response": None
        }

    def get_state(self, force: bool = False) -> Dict[str, Any]:
        """Lấy trạng thái hiện tại từ file bridge."""
        if not BRIDGE_FILE.exists():
            return self._cached_state
        try:
            mtime = BRIDGE_FILE.stat().st_mtime
            if force or mtime != self._last_mtime:
                self._last_mtime = mtime
                data = json.loads(BRIDGE_FILE.read_text(encoding='utf-8'))
                self._cached_state = data
        except Exception:
            pass
        return self._cached_state

    def get_display_info(self) -> Dict[str, Any]:
        """Tính toán thông tin hiển thị trên chip của Widget."""
        state = self.get_state()
        status = state.get("status", "IDLE")
        now = time.time()

        if status == "PROPOSAL":
            prop = state.get("proposal") or {}
            deadline = prop.get("deadline_ts", now)
            rem = max(0, int(deadline - now))
            mins = rem // 60
            secs = rem % 60
            timer_text = f"{mins:02d}:{secs:02d}"
            title = prop.get("title", "Đề xuất Kế hoạch")
            options = prop.get("options", [])
            return {
                "active": True,
                "status": "PROPOSAL",
                "label": f"🧭 Plan [{timer_text}]",
                "short_label": f"🧭 {timer_text}",
                "color_type": "proposal",
                "title": title,
                "remaining_seconds": rem,
                "options": options,
                "start_time": prop.get("start_time", 0.0),
                "deadline_ts": deadline,
                "updated_at": state.get("updated_at", 0.0),
                "details": f"Hạn chót: {timer_text} - Có {len(options)} lựa chọn"
            }
        elif status == "ACCEPTANCE":
            acc = state.get("acceptance") or {}
            title = acc.get("title", "Nghiệm thu Hoàn thiện")
            test_st = acc.get("status", "PASS")
            exit_code = acc.get("exit_code", 0)
            return {
                "active": True,
                "status": "ACCEPTANCE",
                "label": "💎 Nghiệm thu ✨",
                "short_label": "💎 Duyệt",
                "color_type": "acceptance",
                "title": title,
                "summary": acc.get("summary", ""),
                "files_changed": acc.get("files_changed", []),
                "exit_code": exit_code,
                "updated_at": state.get("updated_at", 0.0),
                "details": f"Trạng thái: {test_st} (Exit {exit_code})"
            }
        elif status == "EXECUTING":
            return {
                "active": True,
                "status": "EXECUTING",
                "label": "⚡ Đang chạy...",
                "short_label": "⚡ Chạy",
                "color_type": "executing",
                "title": "Subagent đang xử lý tác vụ",
                "details": "Đang thực thi các bước theo kế hoạch"
            }
        else:
            return {
                "active": False,
                "status": "IDLE",
                "label": "✨ Lean",
                "short_label": "✨",
                "color_type": "idle",
                "title": "Lean Teamwork Sẵn sàng",
                "details": "Không có tác vụ đang chờ phản hồi"
            }

    def submit_response(self, action: str, option_id: Optional[int] = None, note: str = "") -> bool:
        """Gửi phản hồi của người dùng từ Widget."""
        try:
            state = self.get_state(force=True)
            now_ts = time.time()
            state["response"] = {
                "action": action,
                "selected_option_id": option_id,
                "note": note,
                "timestamp": now_ts,
                "handled": False
            }
            if action == "ACCEPT":
                state["last_completed_at"] = now_ts
                hist = state.get("completion_history") or []
                hist.append({
                    "completed_at": now_ts,
                    "session_id": state.get("session_id", ""),
                    "acceptance": state.get("acceptance", {})
                })
                state["completion_history"] = hist[-20:]
            state["updated_at"] = now_ts
            BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
            BRIDGE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
            return True
        except Exception:
            return False


_teamwork_service_instance = None

def get_teamwork_service() -> TeamworkService:
    global _teamwork_service_instance
    if _teamwork_service_instance is None:
        _teamwork_service_instance = TeamworkService()
    return _teamwork_service_instance
