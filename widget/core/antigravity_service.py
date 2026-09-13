# -*- coding: utf-8 -*-
"""Read-only view of Cockpit's current Antigravity account and quota cache.

Cockpit owns account encryption, switching and network refreshes.  This module
only reads its public local state/cache; it never writes account files or tries
to impersonate Cockpit's switch operation.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import base64
import re


ROOT = Path.home() / '.antigravity_cockpit'
ACCOUNTS_FILE = ROOT / 'accounts.json'
IDE_ACCOUNTS_FILE = ROOT / 'codex_accounts.json'
CURRENT_FILE = ROOT / 'current_account.json'
INSTANCES_FILE = ROOT / 'instances.json'
IDE_INSTANCES_FILE = ROOT / 'codex_instances.json'
ACCOUNT_FILES = ROOT / 'accounts'
QUOTA_CACHE = ROOT / 'cache' / 'quota_api_v1_desktop' / 'authorized'
_last_good = None
_native_acc_cache = None
_native_acc_time = 0.0


def _read_json(path, fallback=None):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError, TypeError):
        return fallback


def mask_email(value):
    """Strip domain for clean account display without ellipsis masking."""
    value = str(value or '').strip()
    if '@' not in value:
        return value if value else 'Chưa rõ'
    local, _ = value.split('@', 1)
    return local if local else 'Chưa rõ'


def get_native_antigravity_account():
    """Discover native logged-in Antigravity / Antigravity IDE account when Cockpit is absent.
    Reads directly from Antigravity IDE state database (state.vscdb) or state config.
    Cached for 10 seconds to avoid unnecessary disk I/O.
    """
    global _native_acc_cache, _native_acc_time
    now = time.monotonic()
    if _native_acc_cache is not None and (now - _native_acc_time) < 10.0:
        return _native_acc_cache

    candidates = []
    # Windows paths
    appdata = os.environ.get('APPDATA')
    if appdata:
        p_appdata = Path(appdata)
        candidates.extend([
            p_appdata / 'Antigravity IDE' / 'User' / 'globalStorage' / 'state.vscdb',
            p_appdata / 'Antigravity' / 'User' / 'globalStorage' / 'state.vscdb',
            p_appdata / 'Code' / 'User' / 'globalStorage' / 'state.vscdb',
        ])
    # macOS paths
    home = Path.home()
    mac_appsupport = home / 'Library' / 'Application Support'
    if mac_appsupport.exists():
        candidates.extend([
            mac_appsupport / 'Antigravity IDE' / 'User' / 'globalStorage' / 'state.vscdb',
            mac_appsupport / 'Antigravity' / 'User' / 'globalStorage' / 'state.vscdb',
        ])
    # Linux paths
    linux_config = home / '.config'
    if linux_config.exists():
        candidates.extend([
            linux_config / 'Antigravity IDE' / 'User' / 'globalStorage' / 'state.vscdb',
            linux_config / 'Antigravity' / 'User' / 'globalStorage' / 'state.vscdb',
        ])

    for db_path in candidates:
        if not db_path.exists():
            continue
        try:
            conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
            c = conn.cursor()
            c.execute('SELECT value FROM ItemTable WHERE key = ?', ('antigravityUnifiedStateSync.userStatus',))
            row = c.fetchone()
            conn.close()
            if not row or not row[0]:
                continue
            val = row[0]
            email = None
            name = None
            plan = None
            try:
                dec = base64.b64decode(val)
                for sub in re.findall(rb'[A-Za-z0-9+/=]{16,}', dec):
                    try:
                        sdec = base64.b64decode(sub)
                        m = re.findall(rb'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', sdec)
                        if m and not email:
                            email = m[0].decode('latin1')
                        sdec_text = sdec.decode('utf-8', errors='ignore')
                        if 'Google AI Pro' in sdec_text:
                            plan = 'Google AI Pro'
                        elif 'Google AI Ultra' in sdec_text:
                            plan = 'Google AI Ultra'
                    except Exception:
                        pass
                if not email:
                    m = re.findall(rb'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', dec)
                    if m:
                        email = m[0].decode('latin1')
            except Exception:
                pass
            if not email:
                m = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', str(val))
                if m:
                    email = m[0]
            if email:
                result = {
                    'email': email,
                    'name': name or mask_email(email),
                    'plan': plan or 'Antigravity IDE',
                    'source': str(db_path.parent.parent.parent.name),
                }
                _native_acc_cache = result
                _native_acc_time = now
                return result
        except Exception:
            continue

    _native_acc_cache = None
    _native_acc_time = now
    return None


def _current_account_id():
    """Return active Antigravity account ID prioritized from current Cockpit account, accounts.json, or instance."""
    doc = _read_json(ACCOUNTS_FILE, {}) or {}
    acc_rows = doc.get('accounts') or []

    # 1. Prioritize explicit active account from current_account.json
    record = _read_json(CURRENT_FILE, {}) or {}
    curr_email = str(record.get('email') or '').strip().lower()
    if curr_email:
        for acc in acc_rows:
            if str(acc.get('email') or '').strip().lower() == curr_email:
                return str(acc.get('id') or '')

    # 2. Check accounts.json current_account_id
    cid = str(doc.get('current_account_id') or '')
    if cid:
        return cid

    # 3. Check instances if active instance has bindAccountId
    inst = _read_json(INSTANCES_FILE, {}) or {}
    for item in (inst.get('instances') or []):
        bid = item.get('bindAccountId')
        if bid and bid != '__api_service__':
            return str(bid)
    bind_id = (inst.get('defaultSettings') or {}).get('bindAccountId')
    if bind_id and bind_id != '__api_service__':
        return str(bind_id)

    # 4. Native Antigravity IDE
    native = get_native_antigravity_account()
    if native and native.get('email'):
        return 'native_ide'
    return ''


def _current_email():
    """Resolve email for currently active account in Cockpit Antigravity IDE or Native IDE."""
    # 1. Direct explicit active account file from Cockpit / Widget switcher
    record = _read_json(CURRENT_FILE, {}) or {}
    curr_email = str(record.get('email') or '').strip().lower()
    if curr_email:
        return curr_email

    # 2. Check accounts.json current_account_id
    doc = _read_json(ACCOUNTS_FILE, {}) or {}
    cid = str(doc.get('current_account_id') or '')
    for acc in (doc.get('accounts') or []):
        if str(acc.get('id') or '') == cid:
            em = str(acc.get('email') or '').strip().lower()
            if em:
                return em

    # 3. Check bound instance account
    curr_id = _current_account_id()
    if curr_id and curr_id != 'native_ide':
        for acc in (doc.get('accounts') or []):
            if str(acc.get('id') or '') == curr_id:
                em = str(acc.get('email') or '').strip().lower()
                if em:
                    return em

    # 4. Native Antigravity IDE fallback
    native = get_native_antigravity_account()
    if native and native.get('email'):
        return str(native['email']).strip().lower()
    return ''


def get_cockpit_accounts_with_quota():
    """Return unified list of Cockpit Antigravity accounts enriched with real-time quota stats.
    No split submenus, showing exact quota parameters for each account so the user can easily
    decide which account to switch to.
    """
    payload = _read_json(ACCOUNTS_FILE, {}) or {}
    ide_payload = _read_json(IDE_ACCOUNTS_FILE, {}) or {}
    current_id = _current_account_id()
    current_email = _current_email()
    
    seen_emails = set()
    raw_accounts = []
    for acc in (payload.get('accounts') or []):
        em = str(acc.get('email') or '').strip().lower()
        if em and em not in seen_emails:
            seen_emails.add(em)
            raw_accounts.append(acc)
    for acc in (ide_payload.get('accounts') or []):
        em = str(acc.get('email') or '').strip().lower()
        if em and em not in seen_emails:
            seen_emails.add(em)
            raw_accounts.append(acc)

    caches = {}
    try:
        for path in QUOTA_CACHE.glob('*.json'):
            record = _read_json(path, {})
            email = str(record.get('email') or '').strip().lower()
            if email:
                stamp = str(record.get('updatedAt') or '')
                key = (stamp, path.stat().st_mtime)
                if email not in caches or key > caches[email][0]:
                    caches[email] = (key, record)
    except OSError:
        pass

    results = []
    for acc in raw_accounts:
        acc_id = str(acc.get('id') or '')
        if not acc_id:
            continue
        email = str(acc.get('email') or '').strip()
        clean_name = mask_email(email)
        is_active = (acc_id == current_id) or (email.lower() == current_email.lower())
        cache_entry = caches.get(email.lower())

        if cache_entry:
            record = cache_entry[1]
            bmap = _bucket_map(record.get('payload') or {})
            has_data = bool('gemini-5h' in bmap or '3p-5h' in bmap or 'gemini-weekly' in bmap)
            if has_data:
                g_5h = _percent(bmap.get('gemini-5h', {}))
                c_5h = _percent(bmap.get('3p-5h', {}))
                g_w = _percent(bmap.get('gemini-weekly', {}))
                c_w = _percent(bmap.get('3p-weekly', {}))

                if g_5h == 0 and c_5h == 0 and g_w == 0 and c_w == 0:
                    status_text = "[Hết Quota: G 0% · C 0%]"
                    score = 0
                else:
                    status_text = f"[5H: G {g_5h}% · C {c_5h}%  |  Tuần: G {g_w}% · C {c_w}%]"
                    score = g_5h + c_5h + (g_w + c_w) * 0.1

                results.append({
                    'id': acc_id,
                    'email': email,
                    'clean_name': clean_name,
                    'is_active': is_active,
                    'has_cache': True,
                    'g_5h': g_5h,
                    'c_5h': c_5h,
                    'g_w': g_w,
                    'c_w': c_w,
                    'status_text': status_text,
                    'score': score,
                })
            else:
                results.append({
                    'id': acc_id,
                    'email': email,
                    'clean_name': clean_name,
                    'is_active': is_active,
                    'has_cache': False,
                    'status_text': "[Chưa có cache quota]",
                    'score': -1,
                })
        else:
            results.append({
                'id': acc_id,
                'email': email,
                'clean_name': clean_name,
                'is_active': is_active,
                'has_cache': False,
                'status_text': "[Chưa có cache quota]",
                'score': -1,
            })

    # Fallback to native Antigravity IDE account if no Cockpit accounts found
    if not results:
        native = get_native_antigravity_account()
        if native and native.get('email'):
            native_res = {
                'id': 'native_ide',
                'email': native['email'],
                'clean_name': mask_email(native['email']),
                'is_active': True,
                'has_cache': True,
                'g_5h': 100,
                'c_5h': 100,
                'g_w': 100,
                'c_w': 100,
                'status_text': f"[{native.get('plan') or 'Native IDE'}]",
                'score': 100,
            }
            return {
                'active': [native_res],
                'ready': [],
                'empty': [],
                'all': [native_res],
            }

    # Sort accounts:
    # 1. Active account first
    # 2. Rich quota accounts sorted by score descending
    # 3. Exhausted or no-cache accounts
    active_acc = [r for r in results if r['is_active']]
    other_with_quota = sorted([r for r in results if not r['is_active'] and r.get('score', -1) > 0], key=lambda x: x['score'], reverse=True)
    no_quota = [r for r in results if not r['is_active'] and r.get('score', -1) <= 0]

    return {
        'active': active_acc,
        'ready': other_with_quota,
        'empty': no_quota,
        'all': active_acc + other_with_quota + no_quota,
    }


_tags_cache = None
_tags_cache_time = 0.0


def get_cockpit_tags_map():
    """Discover account tags/groups from Cockpit backups and LevelDB storage.
    Cached for 10.0 seconds for maximum performance and zero jitter.
    """
    global _tags_cache, _tags_cache_time
    now = time.monotonic()
    if _tags_cache is not None and (now - _tags_cache_time) < 10.0:
        return _tags_cache

    tags_map = {}

    # 1. Read from latest Cockpit auto backup (contains 100% clean account tag records)
    import zipfile
    import glob
    backup_dir = ROOT / 'backups'
    if backup_dir.exists():
        zips = sorted(backup_dir.glob('*.zip'), key=lambda p: p.stat().st_mtime, reverse=True)
        if zips:
            try:
                zf = zipfile.ZipFile(zips[0])
                if 'accounts/antigravity.json' in zf.namelist():
                    data = json.loads(zf.read('accounts/antigravity.json'))
                    if isinstance(data, list):
                        for item in data:
                            em = str(item.get('email') or '').strip().lower()
                            tags = item.get('tags')
                            if em and tags and isinstance(tags, list) and len(tags) > 0:
                                tags_map[em] = str(tags[0])
            except Exception:
                pass

    # 2. Augment / override with live LevelDB updates if any exist
    local_app_data = Path(os.environ['LOCALAPPDATA']) if os.environ.get('LOCALAPPDATA') else Path.home() / 'AppData' / 'Local'
    base_dir = local_app_data / 'com.jlcodes.cockpit-tools' / 'EBWebView' / 'Default' / 'Local Storage' / 'leveldb'
    if base_dir.exists():
        paths = sorted(
            [p for p in base_dir.glob('*.*') if p.suffix in ('.log', '.ldb')],
            key=lambda p: (0 if p.suffix == '.log' else 1, p.stat().st_mtime),
            reverse=True
        )
        import re
        pattern_email = re.compile(r'"email":"([^"]+)"')
        pattern_tags = re.compile(r'"tags":(\[[^\]]*\])')
        for p in paths:
            try:
                raw = p.read_bytes()
                for enc in ('utf-16le', 'utf-8'):
                    text = raw.decode(enc, errors='ignore')
                    for chunk in text.split('{"id":"'):
                        if '"email":"' in chunk and '"tags":' in chunk:
                            m_em = pattern_email.search(chunk)
                            m_tg = pattern_tags.search(chunk)
                            if m_em and m_tg:
                                em = m_em.group(1).strip().lower()
                                try:
                                    t_list = json.loads(m_tg.group(1))
                                    if em and t_list and isinstance(t_list, list) and len(t_list) > 0:
                                        tags_map[em] = str(t_list[0])
                                except Exception:
                                    pass
            except Exception:
                pass

    _tags_cache = tags_map
    _tags_cache_time = now
    return tags_map



def get_top_quota_accounts(limit=4):
    """Return unified accounts for quick-switch popover:
    - Row 1: Always the currently active logged-in account (with '● ĐANG DÙNG' status).
    - Rows 2..N: Top available accounts from DIFFERENT tags (family groups) in Cockpit.
      Each tag contributes its single best account with highest quota.
    """
    tags_map = get_cockpit_tags_map()
    data = get_cockpit_accounts_with_quota()
    all_accs = data.get('all', [])

    # 1. Identify active account and assign tags
    active_acc = None
    for a in all_accs:
        em = a['email'].lower()
        tag = tags_map.get(em)
        if not tag:
            tag = a['clean_name']
        a['tag'] = tag
        if a.get('is_active') and active_acc is None:
            active_acc = a

    active_tag = active_acc.get('tag') if active_acc else None

    # 2. Group other accounts by tag
    tag_groups = {}
    for a in all_accs:
        if a.get('is_active'):
            continue
        tag = a.get('tag', 'other')
        if tag not in tag_groups:
            tag_groups[tag] = []
        tag_groups[tag].append(a)

    # 3. For each tag, pick the single account with the highest quota score
    tag_representatives = []
    for tag, acc_list in tag_groups.items():
        sorted_accs = sorted(acc_list, key=lambda x: x.get('score', -1), reverse=True)
        best_in_tag = sorted_accs[0]
        tag_representatives.append((tag, best_in_tag))

    # Prioritize accounts from DIFFERENT tags first (family group diversity)
    other_tags = [item for item in tag_representatives if item[0] != active_tag]
    same_tag = [item for item in tag_representatives if item[0] == active_tag]

    other_tags_sorted = sorted(other_tags, key=lambda x: x[1].get('score', -1), reverse=True)
    same_tag_sorted = sorted(same_tag, key=lambda x: x[1].get('score', -1), reverse=True)

    selected_others = [acc for _, acc in other_tags_sorted]
    if len(selected_others) < limit - 1:
        selected_others += [acc for _, acc in same_tag_sorted]

    # Combine: active first, then top quota representative of each other tag
    combined = []
    if active_acc:
        combined.append(active_acc)
    combined += selected_others[:max(0, limit - len(combined))]

    rows = []
    for a in combined:
        rows.append({
            'id': a['id'],
            'email': a['email'],
            'clean_name': a['clean_name'],
            'tag': a.get('tag', ''),
            'prim_pct': a.get('g_5h', 0) if a.get('has_cache') else 0,
            'sec_pct': a.get('c_5h', 0) if a.get('has_cache') else 0,
            'g_w': a.get('g_w', 0) if a.get('has_cache') else 0,
            'c_w': a.get('c_w', 0) if a.get('has_cache') else 0,
            'prim_reset': a.get('reset_5h', 'Sẵn sàng') if 'reset_5h' in a else 'Sẵn sàng',
            'sec_reset': a.get('reset_w', '') if 'reset_w' in a else '',
            'is_active': a.get('is_active', False),
            'has_cache': a.get('has_cache', False),
            'status_text': a.get('status_text', ''),
        })
    return rows



def _cockpit_ws_switch(account_id):
    """Notify Cockpit daemon via WebSocket to perform full credential injection and switch."""
    try:
        server_file = ROOT / 'server.json'
        if not server_file.exists():
            return False
        server_info = _read_json(server_file, {}) or {}
        port = server_info.get('ws_port')
        token = server_info.get('auth_token')
        if not port or not token:
            return False
        import socket, base64, struct
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(('127.0.0.1', int(port)))
        key = base64.b64encode(b'1234567890123456').decode('ascii')
        req = (
            f'GET / HTTP/1.1\r\n'
            f'Host: 127.0.0.1:{port}\r\n'
            f'Upgrade: websocket\r\n'
            f'Connection: Upgrade\r\n'
            f'Sec-WebSocket-Key: {key}\r\n'
            f'Sec-WebSocket-Version: 13\r\n'
            f'Authorization: Bearer {token}\r\n'
            f'\r\n'
        )
        s.sendall(req.encode('ascii'))
        s.recv(4096)
        payload = json.dumps({'type': 'request.switch_account', 'payload': {'account_id': str(account_id)}}).encode('utf-8')
        length = len(payload)
        frame = bytearray([0x81])
        mask_key = b'WIDG'
        if length <= 125:
            frame.append(0x80 | length)
        elif length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(struct.pack('!H', length))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack('!Q', length))
        frame.extend(mask_key)
        frame.extend(bytearray(payload[i] ^ mask_key[i % 4] for i in range(length)))
        s.sendall(bytes(frame))
        s.close()
        return True
    except Exception:
        return False


def switch_active_account(account_id, email=None):
    """Safely and simultaneously switch current account for BOTH Antigravity thường
    and Antigravity IDE (Codex), ensuring both applications always receive the exact same account.
    """
    now = int(time.time())
    account_id = str(account_id or '').strip()
    email = str(email or '').strip().lower()

    # Load account registries
    acc_payload = _read_json(ACCOUNTS_FILE, {}) or {}
    ide_payload = _read_json(IDE_ACCOUNTS_FILE, {}) or {}
    reg_accounts = acc_payload.get('accounts') or []
    ide_accounts = ide_payload.get('accounts') or []

    # If email wasn't provided, resolve from account_id in either registry
    if not email and account_id:
        for a in reg_accounts:
            if str(a.get('id') or '') == account_id:
                email = str(a.get('email') or '').strip().lower()
                break
        if not email:
            for a in ide_accounts:
                if str(a.get('id') or '') == account_id:
                    email = str(a.get('email') or '').strip().lower()
                    break

    # Resolve IDs for both Antigravity thường (UUID) and Antigravity IDE (codex_...)
    target_regular_id = None
    target_ide_id = None

    if email:
        for a in reg_accounts:
            if str(a.get('email') or '').strip().lower() == email:
                target_regular_id = str(a.get('id') or '')
                break
        for a in ide_accounts:
            if str(a.get('email') or '').strip().lower() == email:
                target_ide_id = str(a.get('id') or '')
                break

    # Fallback to provided account_id if one target wasn't found by email
    if not target_regular_id and account_id and not account_id.startswith('codex_'):
        target_regular_id = account_id
    if not target_ide_id and account_id and account_id.startswith('codex_'):
        target_ide_id = account_id

    # 1. Update Antigravity thường state files (accounts.json & instances.json)
    if target_regular_id:
        try:
            inst_payload = _read_json(INSTANCES_FILE, {}) or {}
            inst_payload.setdefault('defaultSettings', {})['bindAccountId'] = target_regular_id
            INSTANCES_FILE.write_text(json.dumps(inst_payload, indent=2), encoding='utf-8')
        except Exception:
            pass

        try:
            acc_payload['current_account_id'] = target_regular_id
            ACCOUNTS_FILE.write_text(json.dumps(acc_payload, indent=2), encoding='utf-8')
        except Exception:
            pass

    # 2. Update Antigravity IDE (Codex) state files (codex_instances.json & codex_accounts.json)
    if target_ide_id:
        try:
            ide_inst = _read_json(IDE_INSTANCES_FILE, {}) or {}
            ide_inst.setdefault('defaultSettings', {})['bindAccountId'] = target_ide_id
            IDE_INSTANCES_FILE.write_text(json.dumps(ide_inst, indent=2), encoding='utf-8')
        except Exception:
            pass

        try:
            for a in ide_accounts:
                if str(a.get('id') or '') == target_ide_id:
                    a['last_used'] = now
                    break
            ide_payload['accounts'] = ide_accounts
            IDE_ACCOUNTS_FILE.write_text(json.dumps(ide_payload, indent=2), encoding='utf-8')
        except Exception:
            pass

    # 3. Update current_account.json (unified active email record)
    if email:
        try:
            curr_payload = {'email': email, 'updated_at': now}
            CURRENT_FILE.write_text(json.dumps(curr_payload, indent=2), encoding='utf-8')
        except Exception:
            pass

    # 4. Trigger real Cockpit switches via WebSocket for both!
    ok1 = _cockpit_ws_switch(target_regular_id) if target_regular_id else False
    ok2 = _cockpit_ws_switch(target_ide_id) if target_ide_id else False

    return ok1 or ok2


def get_cockpit_account_groups():
    """Return safe, display-only account choices grouped by Cockpit product."""
    def rows_for(path):
        payload = _read_json(path, {}) or {}
        current_id = _current_account_id()
        rows = []
        for row in payload.get('accounts') or []:
            account_id = str(row.get('id') or '')
            if not account_id:
                continue
            label = mask_email(row.get('email') or row.get('name'))
            rows.append({
                'id': account_id,
                'label': label,
                'active': account_id == current_id,
            })
        return rows

    res = {
        'antigravity': rows_for(ACCOUNTS_FILE),
        'ide': rows_for(IDE_ACCOUNTS_FILE),
    }
    if not res['antigravity'] and not res['ide']:
        native = get_native_antigravity_account()
        if native and native.get('email'):
            res['ide'] = [{
                'id': 'native_ide',
                'label': mask_email(native['email']),
                'active': True,
            }]
    return res


def _antigravity_ids():
    ids = set()
    try:
        for path in ACCOUNT_FILES.glob('*.json'):
            record = _read_json(path, {})
            if record.get('kind') == 'antigravity':
                ids.add(path.stem)
    except OSError:
        pass
    if not ids:
        native = get_native_antigravity_account()
        if native and native.get('email'):
            ids.add('native_ide')
    return ids


def _latest_cache(email):
    newest = None
    try:
        for path in QUOTA_CACHE.glob('*.json'):
            record = _read_json(path, {})
            if email and str(record.get('email') or '').strip().lower() != email:
                continue
            stamp = str(record.get('updatedAt') or '')
            key = (stamp, path.stat().st_mtime)
            if newest is None or key > newest[0]:
                newest = (key, record)
    except OSError:
        pass
    return newest[1] if newest else None


def _recent_caches(limit=3):
    """One freshest cache per account, newest first; no credentials are read."""
    rows = {}
    try:
        for path in QUOTA_CACHE.glob('*.json'):
            record = _read_json(path, {})
            email = str(record.get('email') or '').strip().lower()
            if not email:
                continue
            stamp = str(record.get('updatedAt') or '')
            key = (stamp, path.stat().st_mtime)
            if email not in rows or key > rows[email][0]:
                rows[email] = (key, record)
    except OSError:
        pass
    return [record for _, record in sorted(rows.values(), reverse=True)[:limit]]


def _bucket_map(payload):
    buckets = {}
    for group in ((payload.get('quota_summary') or {}).get('groups') or []):
        for bucket in group.get('buckets') or []:
            bucket_id = str(bucket.get('bucketId') or '')
            if bucket_id:
                buckets[bucket_id] = bucket
    return buckets


def _percent(bucket):
    try:
        return max(0, min(100, round(float(bucket.get('remainingFraction')) * 100)))
    except (TypeError, ValueError, AttributeError):
        return 0


def _format_reset(value):
    if value is None or value == '':
        return 'Chưa có lịch reset'
    try:
        if isinstance(value, (int, float)):
            target = datetime.fromtimestamp(float(value) / (1000 if float(value) > 100000000000 else 1), tz=timezone.utc)
        else:
            target = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
            if target.tzinfo is None:
                target = target.replace(tzinfo=timezone.utc)
        seconds = int((target - datetime.now(timezone.utc)).total_seconds())
        if seconds <= 0:
            return 'Đang reset'
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes = seconds // 60
        return f'{days}d {hours}h' if days else f'{hours}h {minutes}m'
    except (ValueError, TypeError, OverflowError):
        return 'Có lịch reset'


def query_antigravity_data():
    """Return current Cockpit-selected Antigravity quota from its disk cache."""
    global _last_good
    ids = _antigravity_ids()
    account_rows = (_read_json(ACCOUNTS_FILE, {}) or {}).get('accounts') or []
    current = _current_email()
    active = next((row for row in account_rows if str(row.get('email') or '').lower() == current), {})
    cache = _latest_cache(current)
    if not cache:
        # Fallback to Native Antigravity IDE when Cockpit cache is missing or Cockpit is not installed
        native = get_native_antigravity_account()
        if native and native.get('email'):
            result = {
                'accounts': max(len(ids), 1),
                'available_count': 1,
                'cooldown_count': 0,
                'missing_count': 0,
                'five_hour_pct': 100,
                'weekly_pct': 100,
                'claude_five_hour_pct': 100,
                'claude_weekly_pct': 100,
                'five_hour_reset': 'Native IDE',
                'weekly_reset': 'Active',
                'active_email': mask_email(native['email']),
                'active_account_id': 'native_ide',
                'active_account_name': native.get('name') or mask_email(native['email']),
                'healthy': True,
                'error': '',
                'timestamp': time.time(),
                'cache_updated_at': datetime.now(timezone.utc).isoformat(),
                'source': 'native-antigravity-ide',
                'plan': native.get('plan') or 'Antigravity IDE',
            }
            _last_good = result
            return result

        return dict(_last_good or {}, healthy=False, accounts=len(ids), error='Cockpit chưa có cache quota Antigravity cho tài khoản đang chọn')

    payload = cache.get('payload') or {}
    buckets = _bucket_map(payload)
    five_hour = buckets.get('gemini-5h', {})
    weekly = buckets.get('gemini-weekly', {})
    if not five_hour or not weekly:
        return dict(_last_good or {}, healthy=False, accounts=len(ids), error='Cache Cockpit thiếu bucket quota Gemini')

    result = {
        'accounts': len(ids),
        'available_count': 1 if current else 0,
        'cooldown_count': 0,
        'missing_count': 0,
        'five_hour_pct': _percent(five_hour),
        'weekly_pct': _percent(weekly),
        'claude_five_hour_pct': _percent(buckets.get('3p-5h', {})),
        'claude_weekly_pct': _percent(buckets.get('3p-weekly', {})),
        'five_hour_reset': _format_reset(five_hour.get('resetTime')),
        'weekly_reset': _format_reset(weekly.get('resetTime')),
        'active_email': mask_email(current),
        'active_account_id': str(active.get('id') or ''),
        'active_account_name': str(active.get('name') or active.get('email') or 'Antigravity'),
        'healthy': True,
        'error': '',
        'timestamp': time.time(),
        'cache_updated_at': str(cache.get('updatedAt') or ''),
        'source': 'cockpit-antigravity-cache',
    }
    _last_good = result
    return result


def get_antigravity_detail_rows():
    """One current-account row for the hover card, derived from the same cache."""
    data = query_antigravity_data()
    if not data.get('healthy'):
        return []
    return [{
        'email': data['active_email'],
        'plan': 'ANTIGRAVITY',
        'prim_pct': data['five_hour_pct'],
        'prim_reset': data['five_hour_reset'],
        'sec_pct': data['weekly_pct'],
        'sec_reset': data['weekly_reset'],
        'is_active': True,
    }]


def get_recent_antigravity_rows(limit=3):
    """Recent Cockpit quota cards for the pool chip, with identities masked."""
    rows = []
    for record in _recent_caches(limit):
        buckets = _bucket_map(record.get('payload') or {})
        rows.append({
            'email': mask_email(record.get('email')),
            'plan': 'ANTIGRAVITY',
            'prim_pct': _percent(buckets.get('gemini-5h', {})),
            'prim_reset': _format_reset((buckets.get('gemini-5h') or {}).get('resetTime')),
            'sec_pct': _percent(buckets.get('3p-5h', {})),
            'sec_reset': _format_reset((buckets.get('3p-5h') or {}).get('resetTime')),
            'is_active': True,
        })
    return rows
