# -*- coding: utf-8 -*-
"""
Config Manager for Cockpit Quota Widget V10 Pro Ultimate
Manages configuration discovery, dynamic sidecar ports, API keys, and widget state.
"""

import os
import json
import base64
from pathlib import Path

from .glass_materials import GLASS_MODES, GLASS_NAMES

# Base Paths
USER_PROFILE = Path(os.environ.get('USERPROFILE', r'C:\Users\tient'))
ROOT_COCKPIT = USER_PROFILE / '.antigravity_cockpit'
STATE_FILE = ROOT_COCKPIT / 'antigravity_widget_state.json'
COCKPIT_DIR = Path(r'C:\Program Files\Cockpit Tools')
COCKPIT_EXE = COCKPIT_DIR / 'cockpit-tools.exe'
COCKPIT_CLIPROXY_EXE = COCKPIT_DIR / 'cockpit-cliproxy.exe'
SIDECAR_DIR = ROOT_COCKPIT / 'codex_local_access_sidecar'
SIDECAR_CONFIG = SIDECAR_DIR / 'config.json'
ACCOUNTS_FILE = ROOT_COCKPIT / 'accounts.json'

# Exact Pixel-Perfect Dimensions
# Compact HUD: the former 680px default left a large amount of decorative
# whitespace once the content was reduced to the essential account/quota tools.
BASE_W = 700
BASE_H = 48
MAX_HORIZONTAL_W = 1600
# The normal horizontal bar may grow taller while unlocked. Keep a modest cap
# so the quota controls stay a compact overlay instead of becoming a panel.
MAX_HORIZONTAL_H = 180
NANO_BASE_W = 340
NANO_BASE_H = 32
VERTICAL_BASE_W = 48
VERTICAL_BASE_H = 320
PILL_H = 36.0
TOP_Y = 6.0


THEMES = ['battery', 'bar', 'ring', 'orbit', 'cards', 'nano']


def get_sidecar_info():
    """Reads dynamic port and api key directly from Cockpit Sidecar configuration."""
    port = 64450
    api_key = None
    if SIDECAR_CONFIG.exists():
        try:
            cfg = json.loads(SIDECAR_CONFIG.read_text(encoding='utf-8'))
            if cfg.get('port'):
                port = int(cfg['port'])
            keys = cfg.get('api-keys') or []
            if keys:
                api_key = keys[0]
        except Exception:
            pass
    return {'port': port, 'api_key': api_key}


def get_active_codex_account_id():
    """Compatibility API for the currently selected Cockpit account record.

    The generic Cockpit account store is the only local account source available
    to this independent Antigravity overlay.  It is shown as Cockpit identity,
    never represented as a verified Antigravity account or billing plan.
    """
    try:
        inst_file = ROOT / 'instances.json'
        if inst_file.exists():
            inst_data = json.loads(inst_file.read_text(encoding='utf-8'))
            bind_id = (inst_data.get('defaultSettings') or {}).get('bindAccountId')
            if bind_id and bind_id != '__api_service__':
                return str(bind_id)
        data = json.loads(ACCOUNTS_FILE.read_text(encoding='utf-8'))
        current_id = data.get('current_account_id')
        return current_id if any(a.get('id') == current_id for a in data.get('accounts', [])) else None
    except (OSError, ValueError, TypeError):
        return None


def load_state():
    """Loads widget state with defaults and validates constraints."""
    default_state = {
        'theme': 'cards',
        'locked': True,
        'rel_x': None,
        'rel_y': None,
        'x': 500,
        'y': 400,
        'width': BASE_W,
        'horizontal_width': BASE_W,
        'height': round(BASE_H * 1.4),
        'scale_percent': 140,
        'glass_mode': 'deep_obsidian',
        'orbit_green': 'blue',
        'orbit_chip_bg': 'glass',
        'chip_text_rgb': None,
        'custom_colors': [],
        'orientation': 'horizontal',
        'anchor_codex_w': 0,
        'anchor_codex_h': 0,
        'anchor_widget_w': 0,
        'anchor_widget_h': 0,
    }

    try:
        if STATE_FILE.exists():
            data = json.loads(STATE_FILE.read_text(encoding='utf-8'))
            theme_val = data.get('theme')
            if theme_val in ['Pin', 'battery']:
                theme_val = 'battery'
            elif theme_val in ['Thanh', 'bar']:
                theme_val = 'bar'
            elif theme_val in ['Vòng', 'ring']:
                theme_val = 'ring'
            elif theme_val in ['Viền chạy', 'orbit']:
                theme_val = 'orbit'
            elif theme_val in ['Card sáng', 'cards']:
                theme_val = 'cards'
            elif theme_val in ['Nano', 'nano']:
                theme_val = 'nano'
            else:
                theme_val = 'cards'

            glass_val = data.get('glass_mode', 'deep_obsidian')
            if glass_val not in GLASS_MODES:
                glass_val = 'deep_obsidian'

            orientation = data.get('orientation', 'horizontal')
            if orientation not in ('horizontal', 'vertical'):
                orientation = 'horizontal'

            # Load scale_percent with fallback to 140% for prominent display
            try:
                scale_pct = int(data.get('scale_percent', 140))
                if not (70 <= scale_pct <= 250):
                    scale_pct = 140
            except Exception:
                scale_pct = 140

            user_scale = float(scale_pct) / 100.0

            horizontal_min_w = NANO_BASE_W if theme_val == 'nano' else round(BASE_W * user_scale)
            horizontal_h = NANO_BASE_H if theme_val == 'nano' else round(BASE_H * user_scale)
            saved_width_raw = int(data.get('horizontal_width', data.get('width', horizontal_min_w)) or horizontal_min_w)
            # Reset runaway width values from previous manual drag errors
            max_limit = round(1600 * user_scale)
            if saved_width_raw > max_limit or saved_width_raw in (680, 560):
                saved_width_raw = horizontal_min_w
            saved_horizontal_width = max(
                horizontal_min_w,
                min(saved_width_raw, max_limit)
            )

            # Vertical is a dedicated column. Horizontal HUD bar computes height with scale_percent
            if orientation == 'vertical':
                w_val, h_val = VERTICAL_BASE_W, VERTICAL_BASE_H
            else:
                w_val = saved_horizontal_width
                h_val = horizontal_h

            # Ensure coordinates are strictly within visible screen space
            cur_x = int(data.get('x', 500))
            cur_y = int(data.get('y', 400))
            try:
                import ctypes
                u32 = ctypes.windll.user32
                v_x = u32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
                v_y = u32.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN
                v_w = u32.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
                v_h = u32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
                if v_w > 0 and v_h > 0:
                    if not (v_x <= cur_x <= v_x + v_w - 100) or not (v_y <= cur_y <= v_y + v_h - 40):
                        cur_x = max(v_x + 50, min(v_x + v_w - w_val - 50, 100))
                        cur_y = max(v_y + 40, min(v_y + v_h - h_val - 50, 40))
            except Exception:
                pass

            default_state.update({
                'theme': theme_val,
                'locked': bool(data.get('locked', True)),
                'rel_x': data.get('rel_x', None),
                'rel_y': data.get('rel_y', None),
                'x': cur_x,
                'y': cur_y,
                'width': w_val,
                'horizontal_width': saved_horizontal_width,
                'height': h_val,
                'scale_percent': scale_pct,
                'glass_mode': glass_val,
                'orbit_green': data.get('orbit_green', 'blue') if data.get('orbit_green') in ('blue', 'green') else 'blue',
                'orbit_chip_bg': data.get('orbit_chip_bg', 'glass') if data.get('orbit_chip_bg') in ('glass', 'transparent') else 'glass',
                'chip_text_rgb': int(data.get('chip_text_rgb')) if isinstance(data.get('chip_text_rgb'), int) and 0 <= data.get('chip_text_rgb') <= 0xFFFFFF else None,
                'custom_colors': [int(v) & 0xFFFFFF for v in data.get('custom_colors', [])[:16] if isinstance(v, int)],
                'orientation': orientation,
                'anchor_codex_w': int(data.get('anchor_codex_w', 0) or 0),
                'anchor_codex_h': int(data.get('anchor_codex_h', 0) or 0),
                'anchor_widget_w': w_val,
                'anchor_widget_h': h_val,
            })
    except Exception:
        pass

    return default_state


def save_state(state_dict):
    """Safely writes widget state to disk."""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(json.dumps(state_dict, ensure_ascii=False, indent=2), encoding='utf-8')
    except OSError:
        pass
