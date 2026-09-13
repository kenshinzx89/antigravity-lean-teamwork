# -*- coding: utf-8 -*-
"""Pure layout rules for the Cockpit quota bar.

Rendering and mouse hit-testing both consume these rectangles.  Keeping the
math here prevents the previous situation where an icon was resized after the
text cards had already consumed the available width.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class HorizontalLayout:
    scale: float
    boxes: dict[str, Rect]


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))


def estimate_account_text_width(text: str) -> float:
    """Accurately estimate text width for Segoe UI Bold 14pt (scale 1.0)."""
    if not text:
        return 40.0
    w = 0.0
    for ch in text:
        if ch in 'ijlI1!|:;.,\'"`':
            w += 4.5
        elif ch in 'mwMW@%#':
            w += 11.5
        elif ch.isupper():
            w += 9.5
        elif ch in 'rtf- ':
            w += 6.0
        elif ch.isdigit():
            w += 8.2
        else:
            w += 8.0
    return w


def calculate_account_chip_width(account_name: str, scale: float = 1.0) -> float:
    """Calculate compact, pixel-perfect width for account chip based on text length."""
    acc_clean = account_name.split('@')[0] if '@' in account_name else account_name
    text_w = estimate_account_text_width(acc_clean)
    # Left padding to dot (12) + dot (9) + gap (6) + right pad (11) = 38.0
    return max(68.0 * scale, (38.0 + text_w) * scale)


def horizontal_layout(width: int, height: int, base_w: int, base_h: int, account_name: str = "", scale_factor: float = 1.0, teamwork_active: bool = False, compact_teamwork_only: bool = False) -> HorizontalLayout:
    """Return stable, pixel-perfect layout for horizontal quota monitor.

    CRITICAL RULE:
    - Khi có Antigravity: Hiển thị đầy đủ tất cả các chip (Account, 5h, Week, Teamwork, Actions).
    - Khi không có Antigravity (compact_teamwork_only=True): Thu gọn lại CHỈ HIỆN DUY NHẤT CHIP TEAMWORK (Nghiệm thu / Đề xuất) để không chiếm màn hình Desktop.
    """
    scale = max(0.5, float(scale_factor))
    pad = 5.0 * scale
    gap = 5.0 * scale
    # Prominent height: 38px * scale pill centered inside 48px * scale bar
    card_h = 38.0 * scale
    card_y = max(1.0, (float(height) - card_h) / 2.0)

    # Generous, crystal-clear, readable prominent widths for quota chips and actions
    w_teamwork = (152.0 if teamwork_active else 84.0) * scale

    if compact_teamwork_only:
        # Chế độ thu gọn: CHỈ DUY NHẤT CHIP TEAMWORK
        boxes: dict[str, Rect] = {}
        boxes["teamwork"] = Rect(pad, card_y, w_teamwork, card_h)
        return HorizontalLayout(scale=scale, boxes=boxes)

    w_5h = 196.0 * scale
    w_week = 190.0 * scale
    switch_w = 38.0 * scale
    action_w = 34.0 * scale

    # Only Chip 1 expands/contracts based on account name
    w_account = calculate_account_chip_width(account_name, scale)

    x = pad
    boxes: dict[str, Rect] = {}
    boxes["account"] = Rect(x, card_y, w_account, card_h)
    x += w_account + gap
    boxes["5h"] = Rect(x, card_y, w_5h, card_h)
    x += w_5h + gap
    boxes["week"] = Rect(x, card_y, w_week, card_h)
    x += w_week + gap
    boxes["teamwork"] = Rect(x, card_y, w_teamwork, card_h)
    x += w_teamwork + gap
    boxes["switch"] = Rect(x, card_y, switch_w, card_h)
    x += switch_w + gap
    boxes["refresh"] = Rect(x, card_y, action_w, card_h)
    x += action_w + gap
    boxes["lock"] = Rect(x, card_y, action_w, card_h)

    return HorizontalLayout(scale=scale, boxes=boxes)



