import json
from pathlib import Path

COCKPIT = Path.home() / ".antigravity_cockpit"
ANTI_STATE = Path.home() / ".gemini" / "antigravity" / "antigravity_state.pbtxt"

def _load(path, fallback):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError): return fallback

def _mask(value):
    value = (value or "").strip()
    if "@" not in value: return value[:2] + "•••" if value else "Không xác định"
    local, domain = value.split("@", 1)
    return f"{local[:2]}•••@{domain}"

def snapshot():
    doc = _load(COCKPIT / "accounts.json", {})
    accounts = doc.get("accounts", [])
    inst = _load(COCKPIT / "instances.json", {})
    active_id = (inst.get("defaultSettings") or {}).get("bindAccountId") or doc.get("current_account_id")
    active = next((a for a in accounts if a.get("id") == active_id), {})
    anti = _load(COCKPIT / "antigravity_legacy_instances.json", {}).get("instances", [])
    try:
        lines = ANTI_STATE.read_text(encoding="utf-8").splitlines()
        model_line = next((line for line in lines if "last_selected_agent_model" in line), "")
        model = model_line.split(":", 1)[-1].strip().strip('"') or "MODEL_UNKNOWN"
    if not accounts:
        try:
            from core.antigravity_service import get_native_antigravity_account
            native = get_native_antigravity_account()
            if native and native.get("email"):
                return {"active": _mask(native.get("email")), "pool": 1, "anti": 1, "model": model.replace("MODEL_PLACEHOLDER_", "")}
        except Exception:
            pass
    return {"active": _mask(active.get("email") or active.get("name")), "pool": len(accounts), "anti": len(anti) if isinstance(anti, list) else 0, "model": model.replace("MODEL_PLACEHOLDER_", "")}
