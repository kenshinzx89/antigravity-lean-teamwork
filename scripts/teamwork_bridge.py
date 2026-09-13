# -*- coding: utf-8 -*-
"""
Lean Teamwork Desktop Bridge SDK
Điều phối dữ liệu 2 chiều thời gian thực giữa Antigravity IDE và Antigravity Desktop Widget.
Vị trí lưu trữ chia sẻ: ~/.antigravity_cockpit/teamwork_bridge.json
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Optional, List, Dict, Any

BRIDGE_DIR = Path(os.environ.get('USERPROFILE', r'C:\Users\tient')) / '.antigravity_cockpit'
BRIDGE_FILE = BRIDGE_DIR / 'teamwork_bridge.json'


def _ensure_dir():
    try:
        BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


def get_bridge_state() -> Dict[str, Any]:
    """Đọc trạng thái hiện tại từ file bridge."""
    if not BRIDGE_FILE.exists():
        return {
            "version": "1.0",
            "updated_at": 0.0,
            "status": "IDLE",
            "session_id": "",
            "proposal": None,
            "acceptance": None,
            "response": None
        }
    try:
        data = json.loads(BRIDGE_FILE.read_text(encoding='utf-8'))
        return data
    except Exception:
        return {
            "version": "1.0",
            "updated_at": 0.0,
            "status": "IDLE",
            "session_id": "",
            "proposal": None,
            "acceptance": None,
            "response": None
        }


def write_bridge_state(state: Dict[str, Any]) -> bool:
    """Ghi trạng thái an toàn nguyên tử (atomic write) vào file bridge."""
    _ensure_dir()
    state["updated_at"] = time.time()
    temp_file = BRIDGE_DIR / f'teamwork_bridge.tmp.{os.getpid()}'
    try:
        content = json.dumps(state, ensure_ascii=False, indent=2)
        temp_file.write_text(content, encoding='utf-8')
        temp_file.replace(BRIDGE_FILE)
        return True
    except Exception:
        try:
            BRIDGE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
            return True
        except Exception:
            return False
    finally:
        if temp_file.exists():
            try:
                temp_file.unlink()
            except Exception:
                pass


def publish_proposal(
    title: str,
    options: List[Dict[str, Any]],
    duration_seconds: int = 150,
    session_id: Optional[str] = None
) -> bool:
    """
    Phát tín hiệu Đề Xuất Kế Hoạch lên Desktop Widget.
    """
    now = time.time()
    cid = session_id or os.environ.get('ANTIGRAVITY_CONVERSATION_ID', '')
    state = {
        "version": "1.0",
        "updated_at": now,
        "status": "PROPOSAL",
        "session_id": cid,
        "proposal": {
            "title": title,
            "duration_seconds": duration_seconds,
            "start_time": now,
            "deadline_ts": now + duration_seconds,
            "options": options
        },
        "acceptance": None,
        "response": None
    }
    return write_bridge_state(state)


def publish_acceptance(
    title: str,
    summary: str,
    files_changed: List[str],
    exit_code: int = 0,
    session_id: Optional[str] = None
) -> bool:
    """
    Phát tín hiệu Báo Cáo Nghiệm Thu Hoàn Thiện lên Desktop Widget.
    """
    now = time.time()
    cid = session_id or os.environ.get('ANTIGRAVITY_CONVERSATION_ID', '')
    state = {
        "version": "1.0",
        "updated_at": now,
        "status": "ACCEPTANCE",
        "session_id": cid,
        "proposal": None,
        "acceptance": {
            "title": title,
            "summary": summary,
            "status": "PASS" if exit_code == 0 else "FAIL",
            "exit_code": exit_code,
            "files_changed": files_changed,
            "completed_at": now
        },
        "response": None
    }
    return write_bridge_state(state)


def submit_user_response(
    action: str,
    selected_option_id: Optional[int] = None,
    note: str = ""
) -> bool:
    """
    Ghi nhận phản hồi từ Widget về IDE.
    action: "SELECT_OPTION" | "ACCEPT" | "DEBUG" | "PAUSE"
    """
    state = get_bridge_state()
    state["response"] = {
        "action": action,
        "selected_option_id": selected_option_id,
        "note": note,
        "timestamp": time.time(),
        "handled": False
    }
    return write_bridge_state(state)


def check_user_response(mark_handled: bool = True) -> Optional[Dict[str, Any]]:
    """
    Kiểm tra xem người dùng đã tương tác bấm nút trên Widget hay chưa.
    Tự động ghi nhận mốc thời gian hoàn tất (last_completed_at) khi người dùng bấm ACCEPT.
    """
    state = get_bridge_state()
    resp = state.get("response")
    if resp and not resp.get("handled", False):
        if mark_handled:
            resp["handled"] = True
            state["response"] = resp
            if resp.get("action") == "ACCEPT":
                now_ts = resp.get("timestamp") or time.time()
                state["last_completed_at"] = now_ts
                hist = state.get("completion_history") or []
                hist.append({
                    "completed_at": now_ts,
                    "session_id": state.get("session_id", ""),
                    "acceptance": state.get("acceptance", {})
                })
                state["completion_history"] = hist[-20:]
            write_bridge_state(state)
        return resp
    return None


def get_last_completed_timestamp() -> float:
    """Trả về timestamp của lần bấm hoàn tất gần nhất (nếu có), hoặc 0.0 nếu chưa có trong phiên."""
    state = get_bridge_state()
    return float(state.get("last_completed_at") or 0.0)


def record_intermediate_issue(issue_description: str, error_type: str = "BUG") -> bool:
    """Ghi nhận một lỗi trung gian phát sinh giữa 2 mốc hoàn tất."""
    state = get_bridge_state()
    issues = state.get("intermediate_issues") or []
    issues.append({
        "timestamp": time.time(),
        "error_type": error_type,
        "description": issue_description
    })
    state["intermediate_issues"] = issues
    return write_bridge_state(state)


def get_intermediate_issues(clear: bool = False) -> List[Dict[str, Any]]:
    """Lấy danh sách các lỗi trung gian phát sinh kể từ lần hoàn tất gần nhất."""
    state = get_bridge_state()
    issues = state.get("intermediate_issues") or []
    if clear:
        state["intermediate_issues"] = []
        write_bridge_state(state)
    return issues


def clear_bridge(status: str = "IDLE") -> bool:
    """Đưa trạng thái về IDLE khi hoàn thành toàn bộ công việc, bảo toàn mốc hoàn tất gần nhất."""
    old_state = get_bridge_state()
    state = {
        "version": "1.0",
        "updated_at": time.time(),
        "status": status,
        "session_id": os.environ.get('ANTIGRAVITY_CONVERSATION_ID', ''),
        "proposal": None,
        "acceptance": None,
        "response": None,
        "last_completed_at": old_state.get("last_completed_at", 0.0),
        "completion_history": old_state.get("completion_history", []),
        "intermediate_issues": []
    }
    return write_bridge_state(state)
