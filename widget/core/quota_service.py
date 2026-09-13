# -*- coding: utf-8 -*-
"""
Quota Service for Cockpit Quota Widget V10 Pro Ultimate
Fetches real-time quota data from Cockpit Sidecar Proxy and generates rich status metadata.
"""

import json
import urllib.request
import time
from .config_manager import (
    get_sidecar_info,
    SIDECAR_CONFIG,
    ACCOUNTS_FILE
)


POOL_FILE = SIDECAR_CONFIG.parent / 'quota-pool-state.json'
_last_good = None
FIVE_HOUR_PLANS = {'PLUS', 'PRO', 'TEAM', 'ENTERPRISE'}


def get_pool_account_ids(pool=None):
    """Return the exact Cockpit polling pool, never a Codex target account."""
    try:
        if pool is None:
            pool = (json.loads(POOL_FILE.read_text(encoding='utf-8')).get('accounts') or {})
        cfg = json.loads(SIDECAR_CONFIG.read_text(encoding='utf-8'))
        keys = cfg.get('api-keys') or []
        configured = (cfg.get('api-key-account-ids') or {}).get(keys[0], []) if keys else []
        ids = [str(item).removesuffix('.json') for item in configured]
        return [account_id for account_id in ids if account_id in pool] or list(pool)
    except (OSError, ValueError, TypeError, KeyError):
        return []


def get_pool_rows():
    """Shared detail source for all pool chips and hover cards."""
    try:
        pool = (json.loads(POOL_FILE.read_text(encoding='utf-8')).get('accounts') or {})
        return [(account_id, pool[account_id]) for account_id in get_pool_account_ids(pool) if isinstance(pool.get(account_id), dict)]
    except (OSError, ValueError, TypeError, KeyError):
        return []


def _quota_present(row, period):
    """Use Cockpit's explicit availability flag, never infer from a percent."""
    return bool((row.get(period) or {}).get('present'))


def get_five_hour_rows():
    """Only plans that Cockpit documents as carrying a 5-hour quota."""
    return [
        (account_id, row) for account_id, row in get_pool_rows()
        if str(row.get('planType') or '').upper() in FIVE_HOUR_PLANS
        and _quota_present(row, 'primary')
    ]


def get_weekly_rows():
    """Only accounts whose Cockpit record exposes a weekly quota window."""
    return [
        (account_id, row) for account_id, row in get_pool_rows()
        if _quota_present(row, 'secondary')
    ]


def _active_pool_count():
    """Count Cockpit's configured polling accounts without changing target quota."""
    return len(get_pool_rows())


def _pool_cache_quota():
    """Use Cockpit's own fresh quota cache while its local HTTP proxy is booting."""
    try:
        if not POOL_FILE.exists() or time.time() - POOL_FILE.stat().st_mtime > 300:
            return None
        pool = json.loads(POOL_FILE.read_text(encoding='utf-8')).get('accounts') or {}
        pool_rows = get_pool_rows()
        five_hour_rows = get_five_hour_rows()
        weekly_rows = get_weekly_rows()
        if not pool_rows:
            return None

        primary = [max(0, min(100, int((row.get('primary') or {}).get('remainingPercent', 0)))) for _, row in five_hour_rows]
        secondary = [max(0, min(100, int((row.get('secondary') or {}).get('remainingPercent', 0)))) for _, row in weekly_rows]
        capacity_5h = len(primary) * 100
        capacity_wk = len(secondary) * 100
        raw_5h, raw_wk = sum(primary), sum(secondary)
        return {
            # Account count is intentionally the whole Cockpit pool; quota
            # windows below have their own eligible account sets.
            'accounts': len(pool_rows),
            'five_hour_accounts': len(five_hour_rows),
            'weekly_accounts': len(weekly_rows),
            'available_count': len(pool_rows),
            'cooldown_count': sum(bool(row.get('cooldown')) for _, row in pool_rows),
            'missing_count': 0,
            'five_hour_pct': round(raw_5h * 100 / capacity_5h) if capacity_5h else 0,
            'weekly_pct': round(raw_wk * 100 / capacity_wk) if capacity_wk else 0,
            'raw_5h': raw_5h,
            'capacity_5h': capacity_5h,
            'raw_wk': raw_wk,
            'capacity_wk': capacity_wk,
            'healthy': True,
            'error': '',
            'timestamp': time.time(),
            'source': 'cockpit-cache',
        }
    except (OSError, ValueError, TypeError, KeyError):
        return None


def query_quota_data():
    """Returns pool quota for the main chips; account details stay in the popover."""
    global _last_good
    # The visible 5h/Week chips are the Cockpit pool contract.  Do not replace
    # their aggregate formula with the current Codex account's quota merely
    # because that account is available; that individual value belongs in the
    # account-detail popover.
    pool = _pool_cache_quota()
    if pool:
        _last_good = pool
        return pool

    info = get_sidecar_info()
    quota_port = info['port']
    api_key = info['api_key']

    try:
        req = urllib.request.Request(f'http://127.0.0.1:{quota_port}/v1/cockpit/quota')
        if api_key:
            req.add_header('Authorization', f'Bearer {api_key}')

        with urllib.request.urlopen(req, timeout=1.0) as res:
            if res.status == 200:
                raw_json = json.loads(res.read().decode('utf-8'))
                plans = raw_json.get('plans') or []

                # 5-Hour Pool (PLUS, PRO, ENTERPRISE, TEAM)
                p_5h = [p for p in plans if str(p.get('plan')).upper() in ['PLUS', 'PRO', 'ENTERPRISE', 'TEAM']]
                if not p_5h and plans:
                    p_5h = plans
                c_5h = sum(int(p.get('count') or 0) * 100 for p in p_5h) or (int(raw_json.get('includedAccountCount') or 1) * 100)
                raw_5h = int(raw_json.get('fiveHourRemainingPercent') or raw_json.get('remainingPercent') or 0)
                pct_5h = max(0, min(100, int(round(raw_5h / c_5h * 100)))) if c_5h > 0 else 100

                # Weekly Pool (FREE, GO)
                p_wk = [p for p in plans if str(p.get('plan')).upper() in ['FREE', 'GO']]
                if not p_wk:
                    p_wk = [p for p in plans if (p.get('weeklyRemainingPercent') or 0) > 0 or (p.get('count') or 0) > 0]
                c_wk = sum(int(p.get('count') or 0) * 100 for p in p_wk) or (int(raw_json.get('includedAccountCount') or 1) * 100)
                raw_wk = sum(int(p.get('weeklyRemainingPercent') or 0) for p in p_wk) if p_wk else int(raw_json.get('weeklyRemainingPercent') or 0)
                pct_wk = max(0, min(100, int(round(raw_wk / c_wk * 100)))) if c_wk > 0 else 100

                available_count = int(raw_json.get('availableAccountCount') or raw_json.get('includedAccountCount') or len(plans) or 0)
                cooldown_count = int(raw_json.get('cooldownAccountCount') or 0)
                missing_count = int(raw_json.get('missingAccountCount') or 0)

                result = {
                    'accounts': int(raw_json.get('includedAccountCount') or len(plans) or 0),
                    'available_count': available_count,
                    'cooldown_count': cooldown_count,
                    'missing_count': missing_count,
                    'five_hour_pct': pct_5h,
                    'weekly_pct': pct_wk,
                    'raw_5h': raw_5h,
                    'capacity_5h': c_5h,
                    'raw_wk': raw_wk,
                    'capacity_wk': c_wk,
                    'healthy': True,
                    'error': '',
                    'timestamp': time.time(),
                    'raw': raw_json
                }
                _last_good = result
                return result
    except Exception as exc:
        fallback = _pool_cache_quota() or _last_good
        if fallback:
            return dict(fallback, error=str(exc)[:90])
        return {
            'accounts': 0,
            'available_count': 0,
            'cooldown_count': 0,
            'missing_count': 0,
            'five_hour_pct': 0,
            'weekly_pct': 0,
            'raw_5h': 0,
            'capacity_5h': 100,
            'raw_wk': 0,
            'capacity_wk': 100,
            'healthy': False,
            'error': str(exc)[:90],
            'timestamp': time.time()
        }

    fallback = _pool_cache_quota() or _last_good
    if fallback:
        return fallback
    return {
        'accounts': 0,
        'available_count': 0,
        'cooldown_count': 0,
        'missing_count': 0,
        'five_hour_pct': 0,
        'weekly_pct': 0,
        'raw_5h': 0,
        'capacity_5h': 100,
        'raw_wk': 0,
        'capacity_wk': 100,
        'healthy': False,
        'error': 'API quota không trả dữ liệu hợp lệ',
        'timestamp': time.time()
    }


def get_detailed_accounts_text(quota_data):
    """Builds a formatted multi-line summary of active accounts for tooltips."""
    try:
        active_ids = get_pool_account_ids()

        all_accounts = []
        if ACCOUNTS_FILE.exists():
            data = json.loads(ACCOUNTS_FILE.read_text(encoding='utf-8'))
            all_accounts = data.get('accounts') or []

        matched = [a for a in all_accounts if a.get('id') in active_ids]
        if not matched and all_accounts:
            matched = all_accounts[:3]

        if not matched:
            count = quota_data.get('accounts', 0)
            return f"⚡ COCKPIT POOL\nĐang kết nối: {count} tài khoản" if count > 0 else "Không tìm thấy tài khoản hoạt động"

        lines = ["⚡ POOL TÀI KHOẢN COCKPIT"]
        for a in matched:
            email = a.get('email') or a.get('id') or 'Tài khoản'
            plan = str(a.get('plan_type') or 'PLUS').upper()
            status = "🟢 Sẵn sàng"
            if a.get('cooling_down'):
                status = "🟣 Cooldown"
            elif a.get('error'):
                status = "🔴 Lỗi xác thực"
            lines.append(f"• {email} [{plan}] {status}")

        if quota_data.get('healthy'):
            lines.append(f"──────────────────────")
            lines.append(f"📊 5h Pool: {quota_data.get('raw_5h', 0)}/{quota_data.get('capacity_5h', 0)} điểm ({quota_data.get('five_hour_pct', 0)}%)")
            lines.append(f"📈 Weekly Pool: {quota_data.get('raw_wk', 0)}/{quota_data.get('capacity_wk', 0)} điểm ({quota_data.get('weekly_pct', 0)}%)")

        return "\n".join(lines)
    except Exception:
        return f"⚡ COCKPIT POOL: {quota_data.get('accounts', 0)} tài khoản đang hoạt động"
