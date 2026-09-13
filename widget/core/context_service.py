# -*- coding: utf-8 -*-
import os
from pathlib import Path

STATE_FILE = Path(os.environ.get('USERPROFILE', r'C:\Users\tient')) / '.gemini' / 'antigravity' / 'antigravity_state.pbtxt'


def get_context_status():
    """Return only context information Antigravity actually exposes locally."""
    try:
        model = ''
        if STATE_FILE.exists():
            for line in STATE_FILE.read_text(encoding='utf-8', errors='replace').splitlines():
                if 'last_selected_agent_model:' in line:
                    model = line.split(':', 1)[1].strip().strip('"')
                    break
        detail = f'Model: {model}' if model and model != 'MODEL_PLACEHOLDER_M319' else 'Antigravity chưa công bố token context'
        return {'available': False, 'error': detail}
    except OSError:
        return {'available': False, 'error': 'Không đọc được trạng thái Antigravity'}
