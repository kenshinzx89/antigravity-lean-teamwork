# -*- coding: utf-8 -*-
"""
Compact Glass Popover HUD Card for Cockpit Quota Widget V10 Pro Ultimate
Renders a luxury, large, crystal-clear glassmorphism popover showing active accounts,
top quota accounts for fast switching on hover/click, glowing cyber quota bars,
and exact reset countdowns.
"""

import sys
import os
import time
import json
import math
from pathlib import Path
import ctypes as c
from ctypes import wintypes as w

from .glass_materials import ARGB, get_material_palette, get_status_colors
from .antigravity_service import (
    get_antigravity_detail_rows,
    get_recent_antigravity_rows,
    get_top_quota_accounts,
    switch_active_account,
)
from .win32_types import (
    WNDCLASS, WNDPROC, POINT, SIZE, BLENDFUNCTION, TRACKMOUSEEVENT,
    kernel32, user32, gdi32, gdiplus
)

USER_PROFILE = Path.home()
ROOT_COCKPIT = USER_PROFILE / '.antigravity_cockpit'
LOG_PATH = Path(__file__).resolve().parent.parent / 'widget_crash.log'


def fetch_active_pool_accounts(focus_type='account'):
    """Pool shows top 4 accounts with most quota for fast switching;
    quota chips show the current active account.
    """
    if focus_type == 'account':
        return get_top_quota_accounts(limit=4)
    return get_antigravity_detail_rows()


class CockpitGlassPopover:
    """Ultra-responsive glassmorphism HUD popover card with hover/click account switching."""

    def __init__(self, parent_app):
        self.parent = parent_app
        self.hwnd = None
        # Generous, proportionate luxury HUD popover: large, crisp typography matching chip standards.
        self.w = 620
        self.h = 406
        self.visible = False
        self.focus_type = '5h'  # '5h', 'week', 'account'
        self.accounts = []
        self.last_fetch = 0
        self.last_focus = None
        self.alpha = 255
        self.hover_idx = -1
        self.hover_start_time = 0.0
        self.switched_in_current_hover = False
        self.target_rect = None

        self.init_window()

    def init_window(self):
        self.cb = WNDPROC(self.proc)
        hinst = kernel32.GetModuleHandleW(None)

        user32.UnregisterClassW('CockpitGlassPopoverV10', hinst)
        wc = WNDCLASS(11, self.cb, 0, 0, hinst, None, user32.LoadCursorW(None, 32512), None, None, 'CockpitGlassPopoverV10')
        user32.RegisterClassW(c.byref(wc))

        # LAYERED | TOOLWINDOW | NOACTIVATE | TOPMOST
        # Ensures popover stays in topmost z-band and receives responsive hover/click.
        ex_style = 0x00080000 | 0x00000080 | 0x08000000 | 0x00000008
        self.hwnd = user32.CreateWindowExW(
            ex_style,
            'CockpitGlassPopoverV10',
            'Cockpit Glass Popover',
            0x80000000,
            0, 0, self.w, self.h,
            None, None, hinst, None
        )

    def contains_point(self, sx, sy):
        """Check if screen coordinates (sx, sy) are within popover or bridge to target chip."""
        if not self.visible or not self.hwnd:
            return False
        rect = w.RECT()
        if not user32.GetWindowRect(self.hwnd, c.byref(rect)):
            return False
        pad = 16
        if (rect.left - pad <= sx <= rect.right + pad and
                rect.top - pad <= sy <= rect.bottom + pad):
            return True
        # Check convex bridge between chip and popover so transitioning mouse never drops
        if self.target_rect:
            tx1, ty1, tx2, ty2 = self.target_rect
            bx1 = min(rect.left, tx1) - pad
            bx2 = max(rect.right, tx2) + pad
            by1 = min(rect.top, ty1) - pad
            by2 = max(rect.bottom, ty2) + pad
            if bx1 <= sx <= bx2 and by1 <= sy <= by2:
                return True
        return False

    def proc(self, hwnd, msg, wp, lp):
        try:
            if msg == 0x0200:  # WM_MOUSEMOVE
                tme = TRACKMOUSEEVENT(c.sizeof(TRACKMOUSEEVENT), 0x00000002, hwnd, 0)
                user32.TrackMouseEvent(c.byref(tme))

                # Exact physical coordinates matching UpdateLayeredWindow
                pt = POINT()
                user32.GetCursorPos(c.byref(pt))
                rect = w.RECT()
                user32.GetWindowRect(hwnd, c.byref(rect))
                cx = pt.x - rect.left
                cy = pt.y - rect.top

                # Keep popover alive while cursor is active inside
                self.parent.popover_until = time.monotonic() + 3.0

                if self.focus_type == 'account' and self.accounts:
                    limit = min(4, len(self.accounts))
                    cur_y = 56.0
                    target_idx = -1
                    for idx in range(limit):
                        if cur_y - 4.0 <= cy <= cur_y + 80.0 and 6.0 <= cx <= self.w - 6.0:
                            target_idx = idx
                            break
                        cur_y += 84.0

                    if target_idx != self.hover_idx:
                        self.hover_idx = target_idx
                        self.hover_start_time = time.monotonic()
                        self.render()
                return 0

            elif msg in (0x0201, 0x0202):  # WM_LBUTTONDOWN / WM_LBUTTONUP (Switch on explicit click)
                if self.focus_type == 'account' and 0 <= self.hover_idx < len(self.accounts):
                    target_acc = self.accounts[self.hover_idx]
                    if not target_acc.get('is_active'):
                        self.trigger_switch(self.hover_idx)
                return 0

            elif msg == 0x02A3:  # WM_MOUSELEAVE
                if self.hover_idx != -1:
                    self.hover_idx = -1
                    self.render()
                self.parent.popover_until = time.monotonic() + 1.2
                return 0

        except Exception:
            import traceback
            try:
                with LOG_PATH.open('a', encoding='utf-8') as f:
                    f.write("PopoverCard.proc exception:\n")
                    traceback.print_exc(file=f)
            except Exception:
                pass

        return user32.DefWindowProcW(hwnd, msg, wp, lp)

    def trigger_switch(self, idx):
        """Perform seamless account switch when clicking a card row."""
        if not (0 <= idx < len(self.accounts)):
            return
        target = self.accounts[idx]

        acc_id = target.get('id', '')
        email = target.get('email', '')
        if acc_id and email:
            switch_active_account(acc_id, email)
            self.parent.refresh_data()
            self.accounts = fetch_active_pool_accounts(self.focus_type)
            self.hover_idx = 0
            self.render()

    def show(self, target_rect, focus_type='5h'):
        """Shows popover positioned cleanly adjacent to target chip."""
        self.focus_type = focus_type
        self.target_rect = target_rect
        if (focus_type != self.last_focus or time.time() - self.last_fetch > 2.0
                or not self.accounts):
            self.accounts = fetch_active_pool_accounts(focus_type)
            self.last_fetch = time.time()
            self.last_focus = focus_type

        self.hover_idx = -1
        self.switched_in_current_hover = False

        limit = 4 if focus_type == 'account' else 3
        display_accs = self.accounts[:limit] if self.accounts else []
        self.h = 56 + len(display_accs) * 84 + 14
        if not display_accs:
            self.h = 100

        screen_w = user32.GetSystemMetrics(0)
        screen_h = user32.GetSystemMetrics(1)

        is_vertical = self.parent.s.get('orientation') == 'vertical'

        if is_vertical:
            pos_x = int(target_rect[0] - self.w - 10)
            if pos_x < 10:
                pos_x = int(target_rect[2] + 10)
            pos_y = int(target_rect[1] - 8)
        else:
            chip_cx = (target_rect[0] + target_rect[2]) / 2.0
            pos_x = int(chip_cx - self.w / 2.0)
            pos_y = int(target_rect[3] + 6)
            if pos_y + self.h > screen_h - 20:
                pos_y = int(target_rect[1] - self.h - 6)

        pos_x = max(10, min(pos_x, screen_w - self.w - 10))
        pos_y = max(10, min(pos_y, screen_h - self.h - 10))

        # HWND_TOPMOST (-1) ensures popover is always in the foremost interaction band
        user32.SetWindowPos(self.hwnd, -1, pos_x, pos_y, self.w, self.h, 0x0040 | 0x0010)
        self.visible = True
        self.alpha = 255
        self.render()
        user32.ShowWindow(self.hwnd, 8)  # SW_SHOWNA

    def hide(self):
        """Hides popover immediately."""
        if not self.visible:
            return
        self.visible = False
        user32.KillTimer(self.hwnd, 99)
        if self.hwnd:
            user32.ShowWindow(self.hwnd, 0)

    def render(self):
        if not self.hwnd:
            return

        screen_dc = user32.GetDC(None)
        mem_dc = gdi32.CreateCompatibleDC(screen_dc)
        bi = (w.DWORD * 11)(44, self.w, -self.h, (32 << 16) | 1, 0, 0, 0, 0, 0, 0, 0)
        p_bits = c.c_void_p()
        hbmp = gdi32.CreateDIBSection(screen_dc, c.byref(bi), 0, c.byref(p_bits), None, 0)
        old_bmp = gdi32.SelectObject(mem_dc, hbmp)

        gfx_p = c.c_void_p()
        gdiplus.GdipCreateFromHDC(mem_dc, c.byref(gfx_p))
        gfx = gfx_p.value
        gdiplus.GdipSetSmoothingMode(gfx, 4)
        gdiplus.GdipSetTextRenderingHint(gfx, 3)
        gdiplus.GdipSetPixelOffsetMode(gfx, 3)

        def make_brush(argb):
            b = c.c_void_p()
            gdiplus.GdipCreateSolidFill(argb, c.byref(b))
            return b.value

        def make_pen(argb, width=1.0):
            p = c.c_void_p()
            gdiplus.GdipCreatePen1(argb, c.c_float(width), 2, c.byref(p))
            return p.value

        def create_pill_path(x, y, w_val, h_val, r):
            path = c.c_void_p()
            gdiplus.GdipCreatePath(0, c.byref(path))
            p = path.value
            gdiplus.GdipAddPathArc(p, c.c_float(x + w_val - 2 * r), c.c_float(y), c.c_float(2 * r), c.c_float(2 * r), c.c_float(270), c.c_float(90))
            gdiplus.GdipAddPathArc(p, c.c_float(x + w_val - 2 * r), c.c_float(y + h_val - 2 * r), c.c_float(2 * r), c.c_float(2 * r), c.c_float(0), c.c_float(90))
            gdiplus.GdipAddPathArc(p, c.c_float(x), c.c_float(y + h_val - 2 * r), c.c_float(2 * r), c.c_float(2 * r), c.c_float(90), c.c_float(90))
            gdiplus.GdipAddPathArc(p, c.c_float(x), c.c_float(y), c.c_float(2 * r), c.c_float(2 * r), c.c_float(180), c.c_float(90))
            gdiplus.GdipClosePathFigure(p)
            return p

        glass_mode = self.parent.s.get('glass_mode', 'deep_obsidian')
        theme = self.parent.s.get('theme', 'cards')
        pal = get_material_palette(glass_mode, theme, self.parent.animation_tick)

        # 1. Popover Background Card
        bg_r = 12.0
        bg_path = create_pill_path(2.0, 2.0, self.w - 4.0, self.h - 4.0, bg_r)

        # Ambient Shadow
        sh_pen = make_pen(ARGB(70, 0, 0, 0), 3.5)
        gdiplus.GdipDrawPath(gfx, sh_pen, bg_path)
        gdiplus.GdipDeletePen(sh_pen)

        # Glass Fill
        bg_alpha = 250 if not pal['is_ghost'] else 225
        bg_color = ARGB(bg_alpha, 10, 14, 24) if pal['is_dark'] else ARGB(bg_alpha, 255, 255, 255)
        bg_b = make_brush(bg_color)
        gdiplus.GdipFillPath(gfx, bg_b, bg_path)
        gdiplus.GdipDeleteBrush(bg_b)

        # Specular Rim
        rim_color = ARGB(200, 56, 189, 248) if pal['is_ghost'] else pal['pill_border']
        rim_pen = make_pen(rim_color, 1.4)
        gdiplus.GdipDrawPath(gfx, rim_pen, bg_path)
        gdiplus.GdipDeletePen(rim_pen)
        gdiplus.GdipDeletePath(bg_path)

        # Fonts: Big, clear, prominent typography matching chip scale
        font_family = c.c_void_p()
        gdiplus.GdipCreateFontFamilyFromName("Segoe UI", None, c.byref(font_family))
        font_title = c.c_void_p()
        font_sub = c.c_void_p()
        font_bold = c.c_void_p()
        font_stat = c.c_void_p()
        font_badge = c.c_void_p()
        gdiplus.GdipCreateFont(font_family, c.c_float(17.5), 1, 2, c.byref(font_title))
        gdiplus.GdipCreateFont(font_family, c.c_float(13.5), 1, 2, c.byref(font_sub))
        gdiplus.GdipCreateFont(font_family, c.c_float(17.0), 1, 2, c.byref(font_bold))
        gdiplus.GdipCreateFont(font_family, c.c_float(14.5), 1, 2, c.byref(font_stat))
        gdiplus.GdipCreateFont(font_family, c.c_float(12.5), 1, 2, c.byref(font_badge))

        fmt_left = c.c_void_p()
        fmt_right = c.c_void_p()
        fmt_center = c.c_void_p()
        gdiplus.GdipCreateStringFormat(0, 0, c.byref(fmt_left))
        gdiplus.GdipCreateStringFormat(0, 0, c.byref(fmt_right))
        gdiplus.GdipCreateStringFormat(0, 0, c.byref(fmt_center))
        gdiplus.GdipSetStringFormatAlign(fmt_right, 2)
        gdiplus.GdipSetStringFormatAlign(fmt_center, 1)

        # 2. Header
        if self.focus_type == 'account':
            title_text = "⚡ CHUYỂN TÀI KHOẢN (NHÓM GIA ĐÌNH)"
            sub_text = "Mỗi Tag 1 TK nhiều Quota nhất"
        elif self.focus_type == '5h':

            title_text = "● ACC HIỆN TẠI · 5H QUOTA"
            pct = self.parent.data.get('five_hour_pct', 0)
            sub_text = f"G {pct}% · C {self.parent.data.get('claude_five_hour_pct', 0)}%"
        elif self.focus_type == 'week':
            title_text = "● ACC HIỆN TẠI · QUOTA TUẦN"
            pct = self.parent.data.get('weekly_pct', 0)
            sub_text = f"G {pct}% · C {self.parent.data.get('claude_weekly_pct', 0)}%"
        else:
            title_text = "● ANTIGRAVITY QUOTA"
            sub_text = f"{self.parent.data.get('accounts', 0)} TK Cockpit"

        title_color = ARGB(255, 56, 189, 248) if pal['is_dark'] else ARGB(255, 2, 132, 199)
        tb_b = make_brush(title_color)
        gdiplus.GdipDrawString(gfx, title_text, -1, font_title.value, (c.c_float * 4)(18, 12, 420, 26), fmt_left.value, tb_b)
        gdiplus.GdipDeleteBrush(tb_b)

        sub_color = ARGB(235, 224, 242, 254) if pal['is_dark'] else ARGB(235, 71, 85, 105)
        sb_b = make_brush(sub_color)
        gdiplus.GdipDrawString(gfx, sub_text, -1, font_sub.value, (c.c_float * 4)(420, 14, self.w - 438, 24), fmt_right.value, sb_b)
        gdiplus.GdipDeleteBrush(sb_b)

        # Divider
        div_pen = make_pen(ARGB(50, 148, 163, 184), 1.0)
        gdiplus.GdipDrawLine(gfx, div_pen, c.c_float(18), c.c_float(46), c.c_float(self.w - 18), c.c_float(46))
        gdiplus.GdipDeletePen(div_pen)

        # 3. Account Rows
        cur_y = 56.0
        limit = 4 if self.focus_type == 'account' else 3
        display_accs = self.accounts[:limit] if self.accounts else []

        if not display_accs:
            empty_b = make_brush(sub_color)
            empty_text = "Không tìm thấy dữ liệu quota tài khoản"
            gdiplus.GdipDrawString(gfx, empty_text, -1, font_sub.value, (c.c_float * 4)(18, 60, self.w - 36, 26), fmt_left.value, empty_b)
            gdiplus.GdipDeleteBrush(empty_b)
        else:
            for idx, acc in enumerate(display_accs):
                is_hover = (idx == self.hover_idx)
                is_active = acc.get('is_active', False)

                # Card Row Container
                row_h = 76.0
                row_w = self.w - 24.0
                row_path = create_pill_path(12.0, cur_y, row_w, row_h, 8.0)

                if is_hover:
                    # 1. Outer Neon Glow Halo
                    glow_pen = make_pen(ARGB(100, 56, 189, 248), 4.2)
                    gdiplus.GdipDrawPath(gfx, glow_pen, row_path)
                    gdiplus.GdipDeletePen(glow_pen)

                    # 2. Rich Deep Obsidian Glass Background (high contrast for bright white text)
                    hl_brush = make_brush(ARGB(160, 15, 23, 42) if pal['is_dark'] else ARGB(110, 224, 242, 254))
                    gdiplus.GdipFillPath(gfx, hl_brush, row_path)
                    gdiplus.GdipDeleteBrush(hl_brush)

                    # 3. Sharp Vibrant Neon Rim
                    hl_pen = make_pen(ARGB(255, 56, 189, 248), 2.0)
                    gdiplus.GdipDrawPath(gfx, hl_pen, row_path)
                    gdiplus.GdipDeletePen(hl_pen)

                    # 4. Left Accent Indicator Pillar (Vạch đèn LED nổi bật mép trái)
                    pill_path = create_pill_path(16.0, cur_y + 10.0, 4.8, row_h - 20.0, 2.4)
                    pill_b = make_brush(ARGB(255, 56, 189, 248))
                    gdiplus.GdipFillPath(gfx, pill_b, pill_path)
                    gdiplus.GdipDeleteBrush(pill_b)
                    gdiplus.GdipDeletePath(pill_path)

                elif is_active:
                    # Subtle green glow for active account
                    act_brush = make_brush(ARGB(35, 34, 197, 94))
                    gdiplus.GdipFillPath(gfx, act_brush, row_path)
                    gdiplus.GdipDeleteBrush(act_brush)

                    act_pen = make_pen(ARGB(140, 34, 197, 94), 1.4)
                    gdiplus.GdipDrawPath(gfx, act_pen, row_path)
                    gdiplus.GdipDeletePen(act_pen)

                    # Left Green Indicator Pillar
                    pill_path = create_pill_path(16.0, cur_y + 14.0, 4.2, row_h - 28.0, 2.1)
                    pill_b = make_brush(ARGB(255, 34, 197, 94))
                    gdiplus.GdipFillPath(gfx, pill_b, pill_path)
                    gdiplus.GdipDeleteBrush(pill_b)
                    gdiplus.GdipDeletePath(pill_path)
                else:
                    # Subtle quiet border for idle cards
                    norm_pen = make_pen(ARGB(35, 148, 163, 184), 1.0)
                    gdiplus.GdipDrawPath(gfx, norm_pen, row_path)
                    gdiplus.GdipDeletePen(norm_pen)

                gdiplus.GdipDeletePath(row_path)

                # Display Name (strip @gmail.com) and Family Group Tag
                clean_name = acc.get('clean_name') or acc.get('email', '')
                if '@' in clean_name:
                    clean_name = clean_name.split('@')[0]
                tag_name = acc.get('tag', '')

                # Status Badge
                badge_w = 126.0
                badge_h = 24.0
                badge_x = self.w - 12.0 - badge_w - 8.0
                badge_y = cur_y + 6.0

                if is_active:
                    badge_b = make_brush(ARGB(50, 34, 197, 94))
                    bp = create_pill_path(badge_x, badge_y, badge_w, badge_h, 4.5)
                    gdiplus.GdipFillPath(gfx, badge_b, bp)
                    gdiplus.GdipDeletePath(bp)
                    gdiplus.GdipDeleteBrush(badge_b)

                    badge_text_b = make_brush(ARGB(255, 34, 197, 94))
                    gdiplus.GdipDrawString(gfx, "● ĐANG DÙNG", -1, font_badge.value,
                                          (c.c_float * 4)(badge_x, badge_y + 2.0, badge_w, badge_h),
                                          fmt_center.value, badge_text_b)
                    gdiplus.GdipDeleteBrush(badge_text_b)
                elif is_hover:
                    badge_b = make_brush(ARGB(255, 56, 189, 248))
                    bp = create_pill_path(badge_x, badge_y, badge_w, badge_h, 4.5)
                    gdiplus.GdipFillPath(gfx, badge_b, bp)
                    gdiplus.GdipDeletePath(bp)
                    gdiplus.GdipDeleteBrush(badge_b)

                    badge_text_b = make_brush(ARGB(255, 10, 14, 24))
                    gdiplus.GdipDrawString(gfx, "⚡ CHUYỂN NGAY", -1, font_badge.value,
                                          (c.c_float * 4)(badge_x, badge_y + 2.0, badge_w, badge_h),
                                          fmt_center.value, badge_text_b)
                    gdiplus.GdipDeleteBrush(badge_text_b)

                # Name Text + Tag (Tương phản cao tuyệt đối theo dark/light theme, 17.0pt Bold)
                prefix = "⚡ " if is_hover else ("✔ " if is_active else "● ")
                title_str = f"{prefix}{clean_name}"
                if tag_name:
                    title_str += f"  [{tag_name}]"

                if is_hover:
                    name_color = ARGB(255, 255, 255, 255) if pal['is_dark'] else ARGB(255, 10, 15, 26)
                else:
                    name_color = ARGB(250, 248, 250, 252) if pal['is_dark'] else ARGB(255, 15, 23, 42)
                eb_b = make_brush(name_color)
                gdiplus.GdipDrawString(gfx, title_str, -1, font_bold.value,
                                      (c.c_float * 4)(30, cur_y + 6, badge_x - 36, 26),
                                      fmt_left.value, eb_b)
                gdiplus.GdipDeleteBrush(eb_b)


                # Quota stats text (Đậm đà 14.5pt, sáng rực rỡ và sắc nét)
                stat_str = acc.get('status_text') or f"5H: G {acc.get('prim_pct', 0)}% · C {acc.get('sec_pct', 0)}%"
                if is_hover:
                    stat_color = ARGB(255, 56, 189, 248) if pal['is_dark'] else ARGB(255, 2, 132, 199)
                else:
                    stat_color = ARGB(250, 224, 242, 254) if pal['is_dark'] else ARGB(255, 30, 41, 59)
                stat_b = make_brush(stat_color)
                gdiplus.GdipDrawString(gfx, stat_str, -1, font_stat.value,
                                      (c.c_float * 4)(30, cur_y + 34, self.w - 56, 22),
                                      fmt_left.value, stat_b)
                gdiplus.GdipDeleteBrush(stat_b)

                # Cyber Glowing Progress Bar
                bar_x = 30.0
                bar_y = cur_y + 58.0
                bar_w = self.w - 60.0
                bar_h = 7.5 if is_hover else 6.0
                bar_r = bar_h / 2.0

                # Progress Track
                track_path = create_pill_path(bar_x, bar_y, bar_w, bar_h, bar_r)
                tr_b = make_brush(ARGB(50, 255, 255, 255) if is_hover else (ARGB(32, 255, 255, 255) if pal['is_dark'] else ARGB(45, 148, 163, 184)))
                gdiplus.GdipFillPath(gfx, tr_b, track_path)
                gdiplus.GdipDeleteBrush(tr_b)
                gdiplus.GdipDeletePath(track_path)

                # Fill (based on primary quota: 5H)
                pct = acc.get('prim_pct', 0)
                fill_col, _ = get_status_colors(pct, pal['is_dark'], theme, tick=self.parent.animation_tick)
                fill_w = max(bar_h, bar_w * (pct / 100.0))
                fill_path = create_pill_path(bar_x, bar_y, fill_w, bar_h, bar_r)
                f_b = make_brush(fill_col)
                gdiplus.GdipFillPath(gfx, f_b, fill_path)
                gdiplus.GdipDeleteBrush(f_b)

                # Specular top light
                shim_pen = make_pen(ARGB(180, 255, 255, 255) if is_hover else ARGB(130, 255, 255, 255), 0.9)
                gdiplus.GdipDrawLine(gfx, shim_pen, c.c_float(bar_x + 1), c.c_float(bar_y + 0.8),
                                     c.c_float(bar_x + fill_w - 1), c.c_float(bar_y + 0.8))
                gdiplus.GdipDeletePen(shim_pen)
                gdiplus.GdipDeletePath(fill_path)

                cur_y += 84.0

        gdiplus.GdipDeleteFont(font_title)
        gdiplus.GdipDeleteFont(font_sub)
        gdiplus.GdipDeleteFont(font_bold)
        gdiplus.GdipDeleteFont(font_stat)
        gdiplus.GdipDeleteFont(font_badge)
        gdiplus.GdipDeleteFontFamily(font_family)
        gdiplus.GdipDeleteStringFormat(fmt_left)
        gdiplus.GdipDeleteStringFormat(fmt_right)
        gdiplus.GdipDeleteStringFormat(fmt_center)
        gdiplus.GdipDeleteGraphics(gfx)

        rect = w.RECT()
        user32.GetWindowRect(self.hwnd, c.byref(rect))
        pt_dest = POINT(rect.left, rect.top)
        sz_dest = SIZE(self.w, self.h)
        pt_src = POINT(0, 0)
        blend = BLENDFUNCTION(0, 0, 255, 1)

        user32.UpdateLayeredWindow(
            self.hwnd, screen_dc, c.byref(pt_dest), c.byref(sz_dest),
            mem_dc, c.byref(pt_src), 0, c.byref(blend), 2
        )

        gdi32.SelectObject(mem_dc, old_bmp)
        gdi32.DeleteObject(hbmp)
        gdi32.DeleteDC(mem_dc)
        user32.ReleaseDC(None, screen_dc)
