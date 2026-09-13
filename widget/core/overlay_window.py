# -*- coding: utf-8 -*-
"""
Overlay Window Engine for Antigravity Quota Widget V10 Pro Ultimate
High-Performance GDI+ Layered Window with Multi-Layer Liquid Glassmorphism,
6 Optical Glass Materials, 6 Pro Ultimate Themes, Smooth 60 FPS Micro-Animations,
and Precision Pixel-Perfect Optical Alignment (Zero Clipping, Zero Letterbox).
"""

import sys
import os
import math
import time
import subprocess
import ctypes as c
from ctypes import wintypes as w
from pathlib import Path

from .config_manager import (
    BASE_W, BASE_H, MAX_HORIZONTAL_W, MAX_HORIZONTAL_H, NANO_BASE_W, NANO_BASE_H,
    VERTICAL_BASE_W, VERTICAL_BASE_H,
    PILL_H, TOP_Y, THEMES, COCKPIT_EXE,
    load_state, save_state
)
from .glass_materials import (
    GLASS_MODES, GLASS_NAMES, ARGB,
    get_material_palette, get_status_colors, get_model_colors
)
from .popover_card import CockpitGlassPopover
from .teamwork_service import get_teamwork_service
from .teamwork_popover import TeamworkGlassPopover
from .antigravity_service import (
    query_antigravity_data, get_cockpit_account_groups,
    get_cockpit_accounts_with_quota, switch_active_account
)
from .context_service import get_context_status
from .layout import horizontal_layout, calculate_account_chip_width
from .window_tracker import find_codex_window

from .win32_types import (
    kernel32, user32, gdi32, comdlg32, gdiplus,
    WNDCLASS, WNDPROC, POINT, MINMAXINFO, SIZE, MSG, BLENDFUNCTION,
    BITMAPINFO, BITMAPINFOHEADER,
    TOOLINFO, CHOOSECOLOR, TRACKMOUSEEVENT, GdiplusStartupInput
)


ASSETS_DIR = Path(__file__).resolve().parent.parent / 'assets'
LOG_PATH = Path(__file__).resolve().parent.parent / 'widget_crash.log'


def create_pill_path(x, y, w, h, radius):
    path = c.c_void_p()
    gdiplus.GdipCreatePath(0, c.byref(path))
    d = min(w, h, radius * 2.0)
    gdiplus.GdipAddPathArc(path, c.c_float(x), c.c_float(y), c.c_float(d), c.c_float(d), c.c_float(180), c.c_float(90))
    gdiplus.GdipAddPathArc(path, c.c_float(x + w - d), c.c_float(y), c.c_float(d), c.c_float(d), c.c_float(270), c.c_float(90))
    gdiplus.GdipAddPathArc(path, c.c_float(x + w - d), c.c_float(y + h - d), c.c_float(d), c.c_float(d), c.c_float(0), c.c_float(90))
    gdiplus.GdipAddPathArc(path, c.c_float(x), c.c_float(y + h - d), c.c_float(d), c.c_float(d), c.c_float(90), c.c_float(90))
    gdiplus.GdipClosePathFigure(path)
    return path


class CockpitOverlayApp:
    def __init__(self):
        self.s = load_state()
        self.data = query_antigravity_data()
        self.sync_dimensions()

        screen_w = user32.GetSystemMetrics(0)
        screen_h = user32.GetSystemMetrics(1)
        self.s['x'] = max(8, min(self.s['x'], max(8, screen_w - self.w - 8)))
        self.s['y'] = max(8, min(self.s['y'], max(8, screen_h - self.h - 8)))

        self.context = {'available': False, 'error': 'Đang tải context'}
        self.hover_btn = None
        self.drag = None
        self.drag_cursor_start = None
        self.drag_window_start = None
        self.drag_moved = False
        self.pending_click = None
        self.popover_until = 0.0
        self.native_drag = False
        self.hwnd = None
        self.hwnd_tt = None
        self.zones = []
        self.is_visible = True
        self.last_codex_rect = None
        self.last_codex_hwnd = None
        self.owner_hwnd = None
        self.codex_minimized_ticks = 0
        self.has_confirmed_codex = False
        self.current_tooltip_text = ""
        self.context_click_at = 0.0
        self.context_last_fire_at = 0.0
        self.animation_tick = 0
        self.refreshing_spin = 0
        self.popover = None
        self.teamwork_service = get_teamwork_service()
        self.teamwork_popover = None
        self._normalizing_size = False
        self.resizing = False
        self.lock_images = {}
        for state, filename in (('pinned', 'lock-pinned.png'), ('unlocked', 'lock-unlocked.png')):
            image = c.c_void_p()
            if gdiplus.GdipLoadImageFromFile(str(ASSETS_DIR / filename), c.byref(image)) == 0:
                self.lock_images[state] = image

    def get_account_display_name(self):
        if not hasattr(self, 'data') or not self.data:
            return ""
        if not self.data.get('healthy'):
            return "Offline"
        acc_email = self.data.get('active_email', '')
        if acc_email:
            return acc_email.split('@')[0] if '@' in acc_email else acc_email
        pool_cnt = self.data.get('accounts', 0)
        return f"{pool_cnt} TK" if pool_cnt > 0 else "No Acc"

    def sync_dimensions(self):
        vertical = self.s.get('orientation') == 'vertical'
        is_nano = self.s.get('theme') == 'nano'
        is_compact_tw = not getattr(self, 'has_active_antigravity', True)

        if is_compact_tw and not vertical and not is_nano:
            user_scale = float(self.s.get('scale_percent', 125)) / 100.0
            tw_info = self.teamwork_service.get_display_info() if hasattr(self, 'teamwork_service') else {'active': False}
            tw_w = (152.0 if tw_info.get('active') else 84.0) * user_scale
            pad = 5.0 * user_scale
            self.base_w = round(tw_w + pad * 2.0)
            self.base_h = round(BASE_H * user_scale)
        elif vertical:
            self.base_w, self.base_h = VERTICAL_BASE_W, VERTICAL_BASE_H
        elif is_nano:
            self.base_w, self.base_h = NANO_BASE_W, NANO_BASE_H
        else:
            user_scale = float(self.s.get('scale_percent', 125)) / 100.0
            acc_name = self.get_account_display_name()
            acc_w = calculate_account_chip_width(acc_name, user_scale)
            tw_info = self.teamwork_service.get_display_info() if hasattr(self, 'teamwork_service') else {'active': False}
            tw_w = 152.0 if tw_info.get('active') else 84.0
            # pad*2(10) + gap*6(30) + 5h(196) + week(190) + teamwork(tw_w) + switch(38) + refresh(34) + lock(34) = 532.0 + tw_w
            self.base_w = round((532.0 + tw_w) * user_scale + acc_w)
            self.base_h = round(BASE_H * user_scale)

        self.w = self.base_w
        self.h = self.base_h
        self.s['width'] = self.w
        self.s['height'] = self.h
        self.s['horizontal_width'] = self.w

        if hasattr(self, 'hwnd') and self.hwnd:
            user32.SetWindowPos(self.hwnd, 0, 0, 0, self.w, self.h, 0x0002 | 0x0004 | 0x0010)

    def _dock_to_visible_antigravity(self):
        """Follow the live Antigravity window when present, or stay floating on desktop in compact mode."""
        host = find_codex_window(include_minimized=True, preferred_hwnd=self.last_codex_hwnd)

        is_active = False
        if host:
            hwnd_host, left, top, right, bottom, _ = host
            is_min = bool(user32.IsIconic(hwnd_host)) or (left <= -10000 and top <= -10000)
            if user32.IsWindow(hwnd_host) and not is_min:
                is_active = True
                self.last_codex_hwnd = hwnd_host
                self.last_codex_rect = (left, top, right, bottom)

        old_active = getattr(self, 'has_active_antigravity', None)
        self.has_active_antigravity = is_active

        # Đảm bảo widget luôn hiển thị trên màn hình
        if not user32.IsWindowVisible(self.hwnd):
            user32.ShowWindow(self.hwnd, 8)  # SW_SHOWNA
        self.is_visible = True

        # Khi chuyển đổi giữa Có Antigravity <-> Không có Antigravity:
        if is_active != old_active:
            self.sync_dimensions()
            self.update_layered_render()

        if not is_active:
            # Khi KHÔNG CÓ Antigravity hoặc đang dùng app khác: Thu lại về chỉ mỗi chip Nghiệm thu nổi trên desktop
            return

        # Khi CÓ Antigravity: Dock vào góc trên cửa sổ IDE
        if not self.s.get('locked'):
            return

        if self.resizing or getattr(self, 'native_drag', False) or getattr(self, 'in_sizemove', False) or self.drag:
            return
        rel_x, rel_y = self.s.get('rel_x'), self.s.get('rel_y')
        if rel_x is None or rel_y is None:
            self.s['rel_x'] = max(8, right - left - self.w - 18)
            self.s['rel_y'] = 40
            save_state(self.s)

        cur_rel_x = self.s.get('rel_x', 8)
        cur_rel_y = self.s.get('rel_y', 40)
        if cur_rel_y > 400 or cur_rel_y < 0:
            cur_rel_y = 40
            self.s['rel_y'] = 40

        target_x = max(left, min(left + cur_rel_x, max(left, right - self.w)))
        target_y = max(top, min(top + cur_rel_y, max(top, bottom - self.h)))

        if (target_x, target_y) == (self.s['x'], self.s['y']):
            return
        self.s['x'], self.s['y'] = target_x, target_y
        user32.SetWindowPos(self.hwnd, -1, int(target_x), int(target_y), self.w, self.h,
                             0x0010 | 0x0004)  # SWP_NOACTIVATE | SWP_NOZORDER

    def set_locked(self, locked):
        self.s['locked'] = bool(locked)
        rect = w.RECT()
        user32.GetWindowRect(self.hwnd, c.byref(rect))
        self.s['x'], self.s['y'] = rect.left, rect.top
        if self.s['locked']:
            if self.last_codex_rect:
                left, top, _, _ = self.last_codex_rect
                self.s['rel_x'] = rect.left - left
                self.s['rel_y'] = rect.top - top
            elif self.s.get('rel_x') is None:
                self.s['rel_x'] = 100
                self.s['rel_y'] = 40
        save_state(self.s)
        self.move_in_codex_layer(self.s['x'], self.s['y'])
        self.update_layered_render()

    def snap_to_preset(self, preset):
        """Snap widget to predefined anchor on host window."""
        if not self.last_codex_rect:
            return
        left, top, right, bottom = self.last_codex_rect
        host_w = right - left
        host_h = bottom - top

        if preset == 'top_right':
            self.s['rel_x'] = max(8, host_w - self.w - 18)
            self.s['rel_y'] = 40
        elif preset == 'top_center':
            self.s['rel_x'] = max(8, int((host_w - self.w) / 2))
            self.s['rel_y'] = 40
        elif preset == 'bottom_right':
            self.s['rel_x'] = max(8, host_w - self.w - 18)
            self.s['rel_y'] = max(8, host_h - self.h - 14)
        elif preset == 'bottom_center':
            self.s['rel_x'] = max(8, int((host_w - self.w) / 2))
            self.s['rel_y'] = max(8, host_h - self.h - 14)
        elif preset == 'top_left':
            self.s['rel_x'] = 80
            self.s['rel_y'] = 40

        self.s['locked'] = True
        save_state(self.s)
        self._dock_to_visible_antigravity()
        self.update_layered_render()

    def move_in_codex_layer(self, x, y, *, show=True, dragging=False):
        """Move widget at (x, y) preserving topmost z-order."""
        flags = 0x0001 | 0x0010  # SWP_NOSIZE | SWP_NOACTIVATE
        if dragging:
            flags |= 0x0004  # SWP_NOZORDER - ultra fast position update without z-order recalculation
            insert_after = 0
        else:
            if show:
                flags |= 0x0040  # SWP_SHOWWINDOW
            insert_after = -1  # HWND_TOPMOST floating reliably above Antigravity
        return user32.SetWindowPos(self.hwnd, insert_after, int(x), int(y), self.w, self.h, flags)

    def bind_to_codex_owner(self, hwnd_c):
        """Track Antigravity window handle cleanly without invasive Win32 reparenting."""
        if not hwnd_c or not user32.IsWindow(hwnd_c) or user32.IsIconic(hwnd_c):
            return
        self.owner_hwnd = hwnd_c

    def forget_closed_codex_owner(self):
        """Drop only a dead native handle; never persist or reuse HWNDs."""
        if self.last_codex_hwnd and not user32.IsWindow(self.last_codex_hwnd):
            self.last_codex_hwnd = None
            self.owner_hwnd = None
            self.last_codex_rect = None

    def get_theme_colors(self):
        # A theme is a renderer contract, not merely a colour preference.
        # Never substitute Cards for an active horizontal Battery/Bar/Ring/
        # Orbit/Nano selection: that was why Antigravity appeared to have six
        # menu entries but only one visual theme.
        theme = self.s.get('theme', 'cards')
        return get_material_palette(
            self.s.get('glass_mode', 'deep_obsidian'),
            theme,
            self.animation_tick
        )

    def get_status_color(self, pct):
        palette = self.get_theme_colors()
        fill_col, _ = get_status_colors(
            pct, palette['is_dark'],
            self.s.get('theme', 'cards'),
            self.s.get('orbit_green', 'blue'),
            self.animation_tick
        )
        return fill_col

    def get_context_color(self, used_pct, available=True):
        """One color source for every CTX surface: text, bar, indicator, and orbit."""
        if not available:
            return ARGB(255, 148, 163, 184)
        if used_pct >= 80:
            return ARGB(255, 255, 77, 109)
        if used_pct >= 60:
            return ARGB(255, 250, 204, 21)
        # CTX has its own direction: 0–59% used is always healthy.
        return self.get_status_color(100)

    def get_quota_text_color(self, pct):
        palette = self.get_theme_colors()
        _, text_col = get_status_colors(
            pct, palette['is_dark'],
            self.s.get('theme', 'cards'),
            self.s.get('orbit_green', 'blue'),
            self.animation_tick
        )
        # Always prioritize dynamic yellow/red warning colors when quota is low
        if pct < 50:
            return text_col

        custom = self.get_custom_chip_text_color()
        if custom:
            return custom
        return text_col

    def animate_chip_text_color(self, base_color):
        if self.s.get('theme') != 'orbit':
            return base_color
        glow = 0.20 + 0.25 * ((math.sin(self.animation_tick * math.pi / 12.0) + 1.0) / 2.0)
        r, g, b = (base_color >> 16) & 0xFF, (base_color >> 8) & 0xFF, base_color & 0xFF
        return ARGB(255, int(r + (255 - r) * glow), int(g + (255 - g) * glow), int(b + (255 - b) * glow))

    def get_custom_chip_text_color(self):
        rgb = self.s.get('chip_text_rgb')
        if not isinstance(rgb, int):
            return None
        return ARGB(255, (rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF)

    def choose_chip_text_color(self):
        custom_rgb = (self.s.get('custom_colors') or [])[:16]
        colors = (w.DWORD * 16)(*[((v & 0xFF) << 16) | (v & 0xFF00) | ((v >> 16) & 0xFF) for v in (custom_rgb + [0] * 16)[:16]])
        current = self.s.get('chip_text_rgb')
        if not isinstance(current, int):
            current = 0x38BDF8
        colorref = ((current & 0xFF) << 16) | (current & 0xFF00) | ((current >> 16) & 0xFF)
        chooser = CHOOSECOLOR(c.sizeof(CHOOSECOLOR), self.hwnd, None, colorref, colors, 0x00000103, 0, None, None)
        if not comdlg32.ChooseColorW(c.byref(chooser)):
            return
        selected = chooser.rgbResult
        self.s['chip_text_rgb'] = ((selected & 0xFF) << 16) | (selected & 0xFF00) | ((selected >> 16) & 0xFF)
        self.s['custom_colors'] = [((v & 0xFF) << 16) | (v & 0xFF00) | ((v >> 16) & 0xFF) for v in colors]
        save_state(self.s)
        self.update_layered_render()

    def update_layered_render(self):
        if not self.hwnd:
            return
        # ``WM_SIZE`` is the sole authority while the user resizes.  Calling
        # sync_dimensions here reloaded the persisted width on every paint and
        # immediately snapped the native resize back to its old value.

        screen_dc = user32.GetDC(None)
        mem_dc = gdi32.CreateCompatibleDC(screen_dc)

        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = c.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = self.w
        bmi.bmiHeader.biHeight = -self.h
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0

        bits = c.c_void_p()
        hbmp = gdi32.CreateDIBSection(screen_dc, c.byref(bmi), 0, c.byref(bits), None, 0)
        old_bmp = gdi32.SelectObject(mem_dc, hbmp)

        gfx = c.c_void_p()
        gdiplus.GdipCreateFromHDC(mem_dc, c.byref(gfx))
        gdiplus.GdipSetSmoothingMode(gfx, 4)  # HighQuality Anti-Alias
        # AntiAliasGridFit (3) provides crisp, smooth, non-jagged antialiased typography on layered glass
        gdiplus.GdipSetTextRenderingHint(gfx, 3)  # AntiAliasGridFit
        gdiplus.GdipSetPixelOffsetMode(gfx, 3)  # PixelOffsetModeNone

        gdiplus.GdipGraphicsClear(gfx, 0x00000000)

        theme_col = self.get_theme_colors()
        text_color = theme_col['text_primary']
        custom_chip_text_color = self.get_custom_chip_text_color()
        chip_text_color = self.animate_chip_text_color(custom_chip_text_color or text_color)
        pill_bg_normal = theme_col['pill_bg_normal']
        pill_bg_hover = theme_col['pill_bg_hover']
        pill_border = theme_col['pill_border']
        inner_refraction = theme_col['inner_refraction']
        shadow_color = theme_col['shadow_color']
        shine_alpha = theme_col.get('shine_alpha', 80)

        font_family = c.c_void_p()
        # The static Segoe UI face has stronger hinting at this 8–10pt size.
        gdiplus.GdipCreateFontFamilyFromName("Segoe UI", None, c.byref(font_family))
        # One scale drives the complete horizontal composition: card details,
        # labels and action icons grow together, but never past the space the
        content_scale = float(self.s.get('scale_percent', 125)) / 100.0 if self.s.get('orientation') != 'vertical' else 1.0
        tw_info = self.teamwork_service.get_display_info() if hasattr(self, 'teamwork_service') else {'active': False}
        is_compact_tw = not getattr(self, 'has_active_antigravity', True)
        if self.s['orientation'] == 'horizontal':
            layout_obj = horizontal_layout(
                self.w, self.h, self.base_w, self.base_h,
                self.get_account_display_name(), content_scale,
                teamwork_active=tw_info.get('active', False),
                compact_teamwork_only=is_compact_tw
            )
            content_scale = layout_obj.scale

        font_main = c.c_void_p()
        gdiplus.GdipCreateFont(font_family, c.c_float(14.0 * content_scale), 1, 2, c.byref(font_main))
        font_nano = c.c_void_p()
        gdiplus.GdipCreateFont(font_family, c.c_float(12.0 * content_scale), 1, 2, c.byref(font_nano))
        font_micro = c.c_void_p()
        gdiplus.GdipCreateFont(font_family, c.c_float(10.5 * content_scale), 1, 2, c.byref(font_micro))
        font_badge = c.c_void_p()
        gdiplus.GdipCreateFont(font_family, c.c_float(10.5 * content_scale), 1, 2, c.byref(font_badge))


        fmt_left = c.c_void_p()
        # Every horizontal card is intentionally one line; wrapping turns a
        # resize into overlapping, unreadable text.
        gdiplus.GdipCreateStringFormat(0x1000, 0, c.byref(fmt_left))
        gdiplus.GdipSetStringFormatAlign(fmt_left, 0)
        gdiplus.GdipSetStringFormatLineAlign(fmt_left, 1)

        fmt_quota = c.c_void_p()
        gdiplus.GdipCreateStringFormat(0x1000, 0, c.byref(fmt_quota))
        gdiplus.GdipSetStringFormatAlign(fmt_quota, 0)
        gdiplus.GdipSetStringFormatLineAlign(fmt_quota, 1)

        fmt_center = c.c_void_p()
        gdiplus.GdipCreateStringFormat(0, 0, c.byref(fmt_center))
        gdiplus.GdipSetStringFormatAlign(fmt_center, 1)
        gdiplus.GdipSetStringFormatLineAlign(fmt_center, 1)

        def make_brush(argb):
            b = c.c_void_p()
            gdiplus.GdipCreateSolidFill(argb, c.byref(b))
            return b

        def make_pen(argb, width=1.0):
            p = c.c_void_p()
            gdiplus.GdipCreatePen1(argb, c.c_float(width), 2, c.byref(p))
            return p

        def draw_raised_text(txt, rect, fmt, argb, font_use=None):
            f_use = font_use or font_main
            # A single opaque pass prevents the old 0.8px shadow from
            # duplicating and softening every small glyph.
            main = make_brush(argb | 0xFF000000)
            gdiplus.GdipDrawString(gfx, txt, -1, f_use, rect, fmt, main)
            gdiplus.GdipDeleteBrush(main)

        # Concentric Liquid Glass Container
        def draw_liquid_glass_chip(x, y, w_box, h_box, btn_id, pct, drawer):
            corner = min(10.0 * content_scale, h_box / 2.0)
            is_hover = (self.hover_btn == btn_id)
            bg_col = pill_bg_hover if is_hover else pill_bg_normal
            bg_alpha = max(18, int(((bg_col >> 24) & 0xFF) * 0.35))
            bg_col = ARGB(bg_alpha, (bg_col >> 16) & 0xFF, (bg_col >> 8) & 0xFF, bg_col & 0xFF)

            # Soft ambient drop shadow
            if shadow_color:
                sh_a = int(((shadow_color >> 24) & 0xFF) * 0.18)
                s_brush = make_brush(ARGB(sh_a, (shadow_color >> 16) & 0xFF, (shadow_color >> 8) & 0xFF, shadow_color & 0xFF))
                s_path = create_pill_path(x, y + 1.2, w_box, h_box, corner)
                gdiplus.GdipFillPath(gfx, s_brush, s_path)
                gdiplus.GdipDeletePath(s_path)
                gdiplus.GdipDeleteBrush(s_brush)

            # Main Glass Body
            bg_b = make_brush(bg_col)
            path = create_pill_path(x, y, w_box, h_box, corner)
            gdiplus.GdipFillPath(gfx, bg_b, path)
            gdiplus.GdipDeleteBrush(bg_b)

            # Subtle top specular highlight rim
            top_pen = make_pen(ARGB(int(shine_alpha * 0.40), 255, 255, 255), 1.0)
            gdiplus.GdipDrawLine(gfx, top_pen, c.c_float(x + corner), c.c_float(y + 0.8), c.c_float(x + w_box - corner), c.c_float(y + 0.8))
            gdiplus.GdipDeletePen(top_pen)

            # Cyber Slim Bar Embedded inside Glass for single-value cards
            if self.s['orientation'] == 'horizontal' and self.s['theme'] == 'bar' and btn_id == 'context':
                BAR_H = 2.8 * content_scale
                bar_x, bar_y, bar_w = x + 6.0 * content_scale, y + h_box - 4.5 * content_scale, w_box - 12.0 * content_scale
                tb = make_brush(theme_col['ring_track'])
                track_path = create_pill_path(bar_x, bar_y, bar_w, BAR_H, BAR_H / 2.0)
                gdiplus.GdipFillPath(gfx, tb, track_path)
                gdiplus.GdipDeletePath(track_path)
                gdiplus.GdipDeleteBrush(tb)

                st_col = self.get_context_color(pct) if btn_id == 'context' else self.get_status_color(pct)
                fill_w = max(BAR_H, bar_w * (pct / 100.0))
                gb = make_brush(st_col)
                fill_path = create_pill_path(bar_x, bar_y, fill_w, BAR_H, BAR_H / 2.0)
                gdiplus.GdipFillPath(gfx, gb, fill_path)
                gdiplus.GdipDeletePath(fill_path)
                gdiplus.GdipDeleteBrush(gb)

            # Outer Specular Border & Aurora Orbit Progress Stroke
            if self.s['theme'] == 'orbit':
                # 1. Subtle glass border base track
                base_pen = make_pen(ARGB(45, 148, 163, 184) if theme_col['is_dark'] else ARGB(40, 100, 116, 139), 1.0)
                gdiplus.GdipDrawPath(gfx, base_pen, path)
                gdiplus.GdipDeletePen(base_pen)

                # 2. Aurora Orbit Progress Stroke along the chip boundary
                if btn_id in ('5h', 'week', 'context') and pct > 0:
                    r = min(corner, 6.0 * content_scale)
                    horizontal = max(0.0, w_box - 2 * r)
                    vertical = max(0.0, h_box - 2 * r)
                    quarter = math.pi * r / 2.0
                    total_len = 2 * horizontal + 2 * vertical + 4 * quarter
                    remaining = total_len * max(0.0, min(100.0, float(pct))) / 100.0

                    orbit_col = self.get_context_color(pct) if btn_id == 'context' else self.get_status_color(pct)
                    nr, ng, nb = (orbit_col >> 16) & 0xFF, (orbit_col >> 8) & 0xFF, orbit_col & 0xFF

                    orbit_pens = (
                        make_pen(ARGB(36, nr, ng, nb), 3.6 * content_scale),
                        make_pen(ARGB(90, nr, ng, nb), 2.2 * content_scale),
                        make_pen(ARGB(255, nr, ng, nb), 1.3 * content_scale),
                    )

                    def line(x1, y1, x2, y2, length):
                        nonlocal remaining
                        if remaining <= 0 or length <= 0:
                            return
                        take = min(remaining, length)
                        t = take / length
                        for p in orbit_pens:
                            gdiplus.GdipDrawLine(gfx, p, c.c_float(x1), c.c_float(y1), c.c_float(x1 + (x2 - x1) * t), c.c_float(y1 + (y2 - y1) * t))
                        remaining -= take

                    def arc(ax, ay, start):
                        nonlocal remaining
                        if remaining <= 0 or quarter <= 0:
                            return
                        take = min(remaining, quarter)
                        for p in orbit_pens:
                            gdiplus.GdipDrawArc(gfx, p, c.c_float(ax), c.c_float(ay), c.c_float(2 * r), c.c_float(2 * r), c.c_float(start), c.c_float(90.0 * take / quarter))
                        remaining -= take

                    line(x + w_box, y + r, x + w_box, y + h_box - r, vertical)
                    arc(x + w_box - 2 * r, y + h_box - 2 * r, 0)
                    line(x + w_box - r, y + h_box, x + r, y + h_box, horizontal)
                    arc(x, y + h_box - 2 * r, 90)
                    line(x, y + h_box - r, x, y + r, vertical)
                    arc(x, y, 180)
                    line(x + r, y, x + w_box - r, y, horizontal)
                    arc(x + w_box - 2 * r, y, 270)

                    for p in orbit_pens:
                        gdiplus.GdipDeletePen(p)
                else:
                    pulse = (math.sin(self.animation_tick * math.pi / 12.0) + 1.0) / 2.0
                    glow_a = int(45 + 35 * pulse) if is_hover else int(30 + 25 * pulse)
                    aura_pen = make_pen(ARGB(glow_a, 56, 189, 248), 1.2 * content_scale)
                    gdiplus.GdipDrawPath(gfx, aura_pen, path)
                    gdiplus.GdipDeletePen(aura_pen)
            else:
                pen = make_pen(pill_border, 1.0)
                gdiplus.GdipDrawPath(gfx, pen, path)
                gdiplus.GdipDeletePen(pen)

            gdiplus.GdipDeletePath(path)
            drawer(x, y, w_box, h_box)

        # Content Drawers
        def draw_account_content(x, y, w_box, h_box):
            dot_cx = x + 12.0 * content_scale
            dot_cy = y + h_box / 2.0

            # Glowing status dot (vibrant purple/green neon)
            dot_col = theme_col['purple_dot'] if self.data['healthy'] else ARGB(255, 239, 68, 68)
            dot_size = 9.0 * content_scale
            halo_size = 18.0 * content_scale

            # Ambient halo
            halo_b = make_brush(ARGB(80, (dot_col >> 16) & 0xFF, (dot_col >> 8) & 0xFF, dot_col & 0xFF))
            gdiplus.GdipFillEllipse(gfx, halo_b, c.c_float(dot_cx - halo_size / 2.0), c.c_float(dot_cy - halo_size / 2.0), c.c_float(halo_size), c.c_float(halo_size))
            gdiplus.GdipDeleteBrush(halo_b)

            # Core dot
            dot_b = make_brush(dot_col)
            gdiplus.GdipFillEllipse(gfx, dot_b, c.c_float(dot_cx - dot_size / 2.0), c.c_float(dot_cy - dot_size / 2.0), c.c_float(dot_size), c.c_float(dot_size))
            gdiplus.GdipDeleteBrush(dot_b)

            text_x = dot_cx + dot_size / 2.0 + 6.0 * content_scale
            text_w = max(20.0, x + w_box - text_x - 3.0 * content_scale)
            text_rect = (c.c_float * 4)(text_x, y, text_w, h_box)

            if not self.data['healthy']:
                txt = "Offline"
            else:
                acc_email = self.data.get('active_email', '')
                if acc_email:
                    txt = acc_email.split('@')[0] if '@' in acc_email else acc_email
                else:
                    pool_cnt = self.data.get('accounts', 0)
                    txt = f"{pool_cnt} TK" if pool_cnt > 0 else "No Acc"

            # Always display full text - dynamic chip stretching ensures full visibility!
            display_txt = txt
            f_acc = font_main
            acc_color = self.animate_chip_text_color(custom_chip_text_color) if custom_chip_text_color else (ARGB(255, 255, 255, 255) if theme_col['is_dark'] else ARGB(255, 15, 23, 42))
            draw_raised_text(display_txt, text_rect, fmt_left, acc_color, f_acc)

        def draw_quota_indicator(cx, cy, pct, st_color, theme):
            if theme == 'battery':
                bw, bh = 14.0 * content_scale, 8.0 * content_scale
                bx = cx - bw / 2.0
                by = cy - bh / 2.0

                pen = make_pen(st_color, 1.1 * content_scale)
                b_path = create_pill_path(bx, by, bw, bh, 2.2 * content_scale)
                gdiplus.GdipDrawPath(gfx, pen, b_path)
                gdiplus.GdipDeletePath(b_path)

                cap_x = bx + bw + 0.2
                cap_y = cy - 1.6 * content_scale
                gdiplus.GdipDrawLine(gfx, pen, c.c_float(cap_x), c.c_float(cap_y), c.c_float(cap_x), c.c_float(cap_y + 3.2 * content_scale))
                gdiplus.GdipDeletePen(pen)

                fill_w = max(1.5 * content_scale, (bw - 2.8 * content_scale) * (pct / 100.0))
                fb = make_brush(st_color)
                f_path = create_pill_path(bx + 1.4 * content_scale, by + 1.4 * content_scale, fill_w, bh - 2.8 * content_scale, 1.2 * content_scale)
                gdiplus.GdipFillPath(gfx, fb, f_path)
                gdiplus.GdipDeletePath(f_path)
                gdiplus.GdipDeleteBrush(fb)

            elif theme == 'ring':
                rw = 12.0 * content_scale
                rx = cx - rw / 2.0
                ry = cy - rw / 2.0

                track_p = make_pen(theme_col['ring_track'], 1.8 * content_scale)
                gdiplus.GdipDrawEllipse(gfx, track_p, c.c_float(rx), c.c_float(ry), c.c_float(rw), c.c_float(rw))
                gdiplus.GdipDeletePen(track_p)

                sweep_angle = max(12.0, 360.0 * (pct / 100.0))
                ring_p = make_pen(st_color, 1.8 * content_scale)
                gdiplus.GdipDrawArc(gfx, ring_p, c.c_float(rx), c.c_float(ry), c.c_float(rw), c.c_float(rw), c.c_float(-90), c.c_float(sweep_angle))
                gdiplus.GdipDeletePen(ring_p)

            elif theme == 'cards':
                halo = make_brush(ARGB(70, (st_color >> 16) & 0xFF, (st_color >> 8) & 0xFF, st_color & 0xFF))
                dot = make_brush(st_color)
                gdiplus.GdipFillEllipse(gfx, halo, c.c_float(cx - 7.5 * content_scale), c.c_float(cy - 7.5 * content_scale), c.c_float(15.0 * content_scale), c.c_float(15.0 * content_scale))
                gdiplus.GdipFillEllipse(gfx, dot, c.c_float(cx - 4.0 * content_scale), c.c_float(cy - 4.0 * content_scale), c.c_float(8.0 * content_scale), c.c_float(8.0 * content_scale))
                gdiplus.GdipDeleteBrush(halo)
                gdiplus.GdipDeleteBrush(dot)

            elif theme == 'bar':
                bar_w, bar_h = 14.0 * content_scale, 4.0 * content_scale
                bar_x, bar_y = cx - bar_w / 2.0, cy - bar_h / 2.0
                tb = make_brush(ARGB(35, 148, 163, 184))
                tp = create_pill_path(bar_x, bar_y, bar_w, bar_h, bar_h / 2.0)
                gdiplus.GdipFillPath(gfx, tb, tp)
                gdiplus.GdipDeleteBrush(tb)
                gdiplus.GdipDeletePath(tp)
                fill_w = max(bar_h, bar_w * (pct / 100.0))
                fb = make_brush(st_color)
                fp = create_pill_path(bar_x, bar_y, fill_w, bar_h, bar_h / 2.0)
                gdiplus.GdipFillPath(gfx, fb, fp)
                gdiplus.GdipDeleteBrush(fb)
                gdiplus.GdipDeletePath(fp)

            elif theme == 'orbit':
                rw = 12.0 * content_scale
                rx = cx - rw / 2.0
                ry = cy - rw / 2.0
                ring_p = make_pen(st_color, 1.6 * content_scale)
                sweep_angle = max(15.0, 360.0 * (pct / 100.0))
                gdiplus.GdipDrawArc(gfx, ring_p, c.c_float(rx), c.c_float(ry), c.c_float(rw), c.c_float(rw), c.c_float(-90), c.c_float(sweep_angle))
                gdiplus.GdipDeletePen(ring_p)

        def draw_quota_text(x, y, w_box, h_box, label, pct, has_indicator):
            text_x = x + (23.0 if has_indicator else 9.0) * content_scale
            text_w = x + w_box - text_x - 5.0 * content_scale
            quota_text = f"{label} {pct}%" if self.data['healthy'] else f"{label} --"
            quota_color = self.animate_chip_text_color(self.get_quota_text_color(pct)) if self.data['healthy'] else ARGB(255, 148, 163, 184)
            text_rect = (c.c_float * 4)(text_x, y, text_w, h_box)
            draw_raised_text(quota_text, text_rect, fmt_quota, quota_color)

        def draw_dual_quota_content(x, y, w_box, h_box, period, gemini, claude):
            """Two balanced, elegant model quota halves inside one shared glass chip."""
            theme = self.s.get('theme', 'cards')
            tag_w = 22.0 * content_scale
            inner_x = x + 3.5 * content_scale
            inner_w = max(2.0, w_box - 7.0 * content_scale)
            quota_x = inner_x + tag_w
            quota_w = max(2.0, inner_w - tag_w)
            half_w = quota_w / 2.0

            # 1. Period Tag Badge (5H / W)
            tag_badge_w = 22.0 * content_scale
            tag_badge_h = 18.0 * content_scale
            tag_badge_x = inner_x + (tag_w - tag_badge_w) / 2.0
            tag_badge_y = y + (h_box - tag_badge_h) / 2.0

            tag_bg_b = make_brush(ARGB(25, 148, 163, 184) if theme_col['is_dark'] else ARGB(20, 100, 116, 139))
            tag_path = create_pill_path(tag_badge_x, tag_badge_y, tag_badge_w, tag_badge_h, 4.0 * content_scale)
            gdiplus.GdipFillPath(gfx, tag_bg_b, tag_path)
            gdiplus.GdipDeletePath(tag_path)
            gdiplus.GdipDeleteBrush(tag_bg_b)

            draw_raised_text(period, (c.c_float * 4)(tag_badge_x, tag_badge_y, tag_badge_w, tag_badge_h),
                             fmt_center, theme_col['text_secondary'], font_micro)

            # 2. Dual Model Quotas (Gemini & Claude)
            for index, (label, pct) in enumerate((('G', gemini), ('C', claude))):
                left = quota_x + index * half_w
                valid = self.data['healthy']
                m_colors = get_model_colors(label, theme_col['is_dark'])
                st_fill, st_text = get_status_colors(pct, theme_col['is_dark'], theme, self.s.get('orbit_green', 'blue'), self.animation_tick)

                badge_d = 16.0 * content_scale
                badge_x = left + 3.0 * content_scale
                badge_y = y + (h_box - badge_d) / 2.0 - (1.5 * content_scale if theme in ('cards', 'bar', 'battery') else 0)

                # Circular model badge with brand tint
                badge_b = make_brush(m_colors['badge_bg'])
                gdiplus.GdipFillEllipse(gfx, badge_b, c.c_float(badge_x), c.c_float(badge_y), c.c_float(badge_d), c.c_float(badge_d))
                gdiplus.GdipDeleteBrush(badge_b)

                # Badge letter 'G' or 'C'
                draw_raised_text(label, (c.c_float * 4)(badge_x, badge_y, badge_d, badge_d), fmt_center, m_colors['badge_text'], font_badge)

                # Value text (e.g. 78% or 100%) - full width with zero clipping
                pct_str = f"{pct}%" if valid else "--"
                val_x = badge_x + badge_d + 3.0 * content_scale
                val_w = max(42.0, left + half_w - val_x - 1.0 * content_scale)
                val_y = y + (h_box - 18.0 * content_scale) / 2.0 - (1.5 * content_scale if theme in ('cards', 'bar', 'battery') else 0)

                val_col = st_text if pct < 50 else (self.get_custom_chip_text_color() or theme_col['text_primary'])
                val_font = font_nano if pct >= 100 else font_main
                draw_raised_text(pct_str, (c.c_float * 4)(val_x, val_y, val_w, 18.0 * content_scale), fmt_left, val_col, val_font)

                # Theme-specific micro gauge for BOTH G and C:
                if theme == 'battery':
                    # Micro battery gauge representing individual model quota
                    bat_w = max(12.0, (left + half_w) - badge_x - 6.0 * content_scale)
                    bat_h = max(2.8, 3.5 * content_scale)
                    bat_x = badge_x
                    bat_y = y + h_box - 5.0 * content_scale

                    bat_p = make_pen(ARGB(70, 148, 163, 184) if theme_col['is_dark'] else ARGB(80, 100, 116, 139), 0.8)
                    bp = create_pill_path(bat_x, bat_y, bat_w, bat_h, 1.2 * content_scale)
                    gdiplus.GdipDrawPath(gfx, bat_p, bp)
                    gdiplus.GdipDeletePath(bp)
                    gdiplus.GdipDeletePen(bat_p)

                    if valid and pct > 0:
                        fill_w = max(1.5 * content_scale, (bat_w - 1.6 * content_scale) * max(0, min(100, pct)) / 100.0)
                        fill_b = make_brush(st_fill)
                        fp = create_pill_path(bat_x + 0.8 * content_scale, bat_y + 0.6 * content_scale, fill_w, bat_h - 1.2 * content_scale, 0.8 * content_scale)
                        gdiplus.GdipFillPath(gfx, fill_b, fp)
                        gdiplus.GdipDeletePath(fp)
                        gdiplus.GdipDeleteBrush(fill_b)

                elif theme in ('cards', 'bar'):
                    bar_x = badge_x
                    bar_w = max(6.0, (left + half_w) - bar_x - 4.0 * content_scale)
                    bar_h = max(2.8, 3.2 * content_scale)
                    bar_y = y + h_box - 5.0 * content_scale

                    tr_b = make_brush(ARGB(30, 255, 255, 255) if theme_col['is_dark'] else ARGB(35, 148, 163, 184))
                    tr_p = create_pill_path(bar_x, bar_y, bar_w, bar_h, bar_h / 2.0)
                    gdiplus.GdipFillPath(gfx, tr_b, tr_p)
                    gdiplus.GdipDeletePath(tr_p)
                    gdiplus.GdipDeleteBrush(tr_b)

                    if valid and pct > 0:
                        fill_w = max(bar_h, bar_w * max(0, min(100, pct)) / 100.0)
                        fill_b = make_brush(st_fill)
                        fill_p = create_pill_path(bar_x, bar_y, fill_w, bar_h, bar_h / 2.0)
                        gdiplus.GdipFillPath(gfx, fill_b, fill_p)
                        gdiplus.GdipDeletePath(fill_p)
                        gdiplus.GdipDeleteBrush(fill_b)

                elif theme == 'ring':
                    # Progress ring 360 degree for BOTH models
                    ring_p = make_pen(st_fill, 1.8 * content_scale)
                    sweep = max(10.0, 360.0 * (pct / 100.0))
                    gdiplus.GdipDrawArc(gfx, ring_p, c.c_float(badge_x - 1.4), c.c_float(badge_y - 1.4),
                                        c.c_float(badge_d + 2.8), c.c_float(badge_d + 2.8),
                                        c.c_float(-90), c.c_float(sweep))
                    gdiplus.GdipDeletePen(ring_p)

                elif theme == 'orbit':
                    # 2 separate Neon Orbit Progress Rings for G and C
                    # Progress arc ring around each badge representing individual quota
                    sweep_angle = max(15.0, 360.0 * (pct / 100.0))
                    nr, ng, nb = (st_fill >> 16) & 0xFF, (st_fill >> 8) & 0xFF, st_fill & 0xFF
                    
                    # Outer neon glow aura for this model
                    o_halo = make_pen(ARGB(75, nr, ng, nb), 2.8 * content_scale)
                    gdiplus.GdipDrawArc(gfx, o_halo, c.c_float(badge_x - 1.8), c.c_float(badge_y - 1.8),
                                        c.c_float(badge_d + 3.6), c.c_float(badge_d + 3.6),
                                        c.c_float(-90), c.c_float(sweep_angle))
                    gdiplus.GdipDeletePen(o_halo)
                    
                    # Sharp vibrant core progress ring for this model
                    o_pen = make_pen(ARGB(255, nr, ng, nb), 1.4 * content_scale)
                    gdiplus.GdipDrawArc(gfx, o_pen, c.c_float(badge_x - 1.8), c.c_float(badge_y - 1.8),
                                        c.c_float(badge_d + 3.6), c.c_float(badge_d + 3.6),
                                        c.c_float(-90), c.c_float(sweep_angle))
                    gdiplus.GdipDeletePen(o_pen)

            # Hairline vertical separator between G and C
            sep_x = quota_x + half_w
            sep_pen = make_pen(ARGB(35, 148, 163, 184) if theme_col['is_dark'] else ARGB(30, 100, 116, 139), 1.0)
            gdiplus.GdipDrawLine(gfx, sep_pen, c.c_float(sep_x), c.c_float(y + 4.5 * content_scale),
                                 c.c_float(sep_x), c.c_float(y + h_box - 4.5 * content_scale))
            gdiplus.GdipDeletePen(sep_pen)

        def draw_5h_content(x, y, w_box, h_box):
            draw_dual_quota_content(x, y, w_box, h_box, '5H',
                                    self.data.get('five_hour_pct', 0),
                                    self.data.get('claude_five_hour_pct', 0))

        def draw_week_content(x, y, w_box, h_box):
            draw_dual_quota_content(x, y, w_box, h_box, 'W',
                                    self.data.get('weekly_pct', 0),
                                    self.data.get('claude_weekly_pct', 0))

        def draw_teamwork_content(x, y, w_box, h_box):
            tw_info = self.teamwork_service.get_display_info() if hasattr(self, 'teamwork_service') else {'active': False, 'status': 'IDLE'}
            col_type = tw_info.get('color_type', 'idle')
            label = tw_info.get('label', '✨ Lean')

            if col_type == 'proposal':
                dot_col = ARGB(255, 56, 189, 248)
            elif col_type == 'acceptance':
                dot_col = ARGB(255, 52, 211, 153)
            elif col_type == 'executing':
                dot_col = ARGB(255, 168, 85, 247)
            else:
                dot_col = ARGB(180, 148, 163, 184)

            dot_cx = x + 12.0 * content_scale
            dot_cy = y + h_box / 2.0
            dot_size = 7.5 * content_scale
            halo_size = 15.0 * content_scale

            halo_b = make_brush(ARGB(65, (dot_col >> 16) & 0xFF, (dot_col >> 8) & 0xFF, dot_col & 0xFF))
            gdiplus.GdipFillEllipse(gfx, halo_b, c.c_float(dot_cx - halo_size / 2.0), c.c_float(dot_cy - halo_size / 2.0), c.c_float(halo_size), c.c_float(halo_size))
            gdiplus.GdipDeleteBrush(halo_b)

            dot_b = make_brush(dot_col)
            gdiplus.GdipFillEllipse(gfx, dot_b, c.c_float(dot_cx - dot_size / 2.0), c.c_float(dot_cy - dot_size / 2.0), c.c_float(dot_size), c.c_float(dot_size))
            gdiplus.GdipDeleteBrush(dot_b)

            text_x = dot_cx + dot_size / 2.0 + 5.0 * content_scale
            text_w = max(20.0, x + w_box - text_x - 4.0 * content_scale)
            text_rect = (c.c_float * 4)(text_x, y, text_w, h_box)
            tw_color = ARGB(255, 255, 255, 255) if theme_col['is_dark'] else ARGB(255, 15, 23, 42)
            draw_raised_text(label, text_rect, fmt_left, tw_color, font_nano)

        def draw_refresh_icon(cx, cy, icon_scale=content_scale):
            angle = (self.refreshing_spin * 36) % 360 if self.refreshing_spin > 0 else 0
            pen = make_pen(text_color, 1.4 * icon_scale)
            r = 4.2 * icon_scale
            gdiplus.GdipDrawArc(gfx, pen, c.c_float(cx - r), c.c_float(cy - r), c.c_float(r * 2), c.c_float(r * 2), c.c_float(45 + angle), c.c_float(270))
            gdiplus.GdipDeletePen(pen)

            b = make_brush(text_color)
            path = c.c_void_p()
            gdiplus.GdipCreatePath(0, c.byref(path))
            rad = math.radians(45 + angle)
            ax, ay = cx + r * math.cos(rad), cy + r * math.sin(rad)
            gdiplus.GdipAddPathLine(path, c.c_float(ax - 2.5 * icon_scale), c.c_float(ay - 2.0 * icon_scale), c.c_float(ax + 1.5 * icon_scale), c.c_float(ay - 0.5 * icon_scale))
            gdiplus.GdipAddPathLine(path, c.c_float(ax + 1.5 * icon_scale), c.c_float(ay - 0.5 * icon_scale), c.c_float(ax - 0.5 * icon_scale), c.c_float(ay + 3.0 * icon_scale))
            gdiplus.GdipClosePathFigure(path)
            gdiplus.GdipFillPath(gfx, b, path)
            gdiplus.GdipDeletePath(path)
            gdiplus.GdipDeleteBrush(b)

        def draw_lock_icon(cx, cy, is_locked, icon_scale=content_scale):
            # Twemoji PNGs retain their intended emoji appearance in a layered
            # GDI+ window; colour-font glyphs do not and were rendering corrupt.
            image = self.lock_images.get('pinned' if is_locked else 'unlocked')
            if image:
                icon_box = max(16, int(round(22.0 * icon_scale)))
                gdiplus.GdipDrawImageRectI(
                    gfx, image, int(round(cx - icon_box / 2.0)),
                    int(round(cy - icon_box / 2.0)), icon_box, icon_box
                )

        def draw_circle_action(x, y, d_btn, btn_id, icon_drawer):
            is_hover = (self.hover_btn == btn_id)
            bg_col = pill_bg_hover if is_hover else pill_bg_normal

            if shadow_color:
                s_brush = make_brush(shadow_color)
                gdiplus.GdipFillEllipse(gfx, s_brush, c.c_float(x), c.c_float(y + 1.2), c.c_float(d_btn), c.c_float(d_btn))
                gdiplus.GdipDeleteBrush(s_brush)

            bg_b = make_brush(bg_col)
            gdiplus.GdipFillEllipse(gfx, bg_b, c.c_float(x), c.c_float(y), c.c_float(d_btn), c.c_float(d_btn))
            gdiplus.GdipDeleteBrush(bg_b)

            pen = make_pen(pill_border, 1.0)
            gdiplus.GdipDrawEllipse(gfx, pen, c.c_float(x), c.c_float(y), c.c_float(d_btn), c.c_float(d_btn))
            gdiplus.GdipDeletePen(pen)

            icon_drawer(x + d_btn / 2.0, y + d_btn / 2.0)

        def draw_switch_content(x, y, w_box, h_box):
            draw_raised_text("⇄", (c.c_float * 4)(x, y - 1, w_box, h_box), fmt_center, text_color, font_main)

        # Layout Dispatcher
        self.zones = []

        if self.s['theme'] == 'nano':
            # Nano keeps its compact proportions using the full horizontal budget
            nano_y = 3.0
            nano_h = max(22.0, float(self.h) - 6.0)
            nano_action_d = 22.0 * content_scale
            nano_action_y = (float(self.h) - nano_action_d) / 2.0
            nano_text_min = 72.0 + 72.0 + 72.0
            nano_text_budget = max(nano_text_min, float(self.w) - 8.0 - 4.0 * 4.0 - 2.0 * nano_action_d)
            nano_extra = nano_text_budget - nano_text_min
            cur_x = 5.0
            w_acc = 72.0 + nano_extra * 0.36
            draw_liquid_glass_chip(cur_x, nano_y, w_acc, nano_h, 'account', 0, lambda px, py, pw, ph: draw_raised_text(f"● {self.data['accounts']}", (c.c_float * 4)(px + 4, py + 1, pw - 8, ph - 2), fmt_center, chip_text_color, font_nano))
            self.zones.append(('account', cur_x, nano_y, w_acc, nano_h))
            cur_x += w_acc + 4.0

            w_5h = 72.0 + nano_extra * 0.32
            draw_liquid_glass_chip(cur_x, nano_y, w_5h, nano_h, '5h', self.data['five_hour_pct'], lambda px, py, pw, ph: draw_raised_text(f"G{self.data['five_hour_pct']} C{self.data.get('claude_five_hour_pct', 0)}", (c.c_float * 4)(px + 3, py + 1, pw - 6, ph - 2), fmt_center, self.get_quota_text_color(self.data['five_hour_pct']), font_nano))
            self.zones.append(('5h', cur_x, nano_y, w_5h, nano_h))
            cur_x += w_5h + 4.0

            w_wk = 72.0 + nano_extra * 0.32
            draw_liquid_glass_chip(cur_x, nano_y, w_wk, nano_h, 'week', self.data['weekly_pct'], lambda px, py, pw, ph: draw_raised_text(f"G{self.data['weekly_pct']} C{self.data.get('claude_weekly_pct', 0)}", (c.c_float * 4)(px + 3, py + 1, pw - 6, ph - 2), fmt_center, self.get_quota_text_color(self.data['weekly_pct']), font_nano))
            self.zones.append(('week', cur_x, nano_y, w_wk, nano_h))
            cur_x += w_wk + 4.0

            draw_circle_action(cur_x, nano_action_y, nano_action_d, 'refresh', lambda cx, cy: draw_refresh_icon(cx, cy))
            self.zones.append(('refresh', cur_x, nano_action_y, nano_action_d, nano_action_d))
            cur_x += nano_action_d + 4.0

            draw_circle_action(cur_x, nano_action_y, nano_action_d, 'lock', lambda cx, cy: draw_lock_icon(cx, cy, self.s['locked']))
            self.zones.append(('lock', cur_x, nano_action_y, nano_action_d, nano_action_d))

        elif self.s['orientation'] == 'vertical':
            # Ultra-Sleek Streamlined Vertical Mode (40 x 282) - 100% straight 32px column
            chip_w = 32.0
            chip_h = 60.0
            x = 4.0

            # 1. Vertical Account Card
            def draw_vert_account(px, py, pw, ph):
                dot_cx = px + pw / 2.0
                dot_cy = py + 12.0
                pulse = (math.sin(self.animation_tick * math.pi / 15.0) + 1.0) / 2.0
                halo_size = 6.0 + 3.0 * pulse
                halo_b = make_brush(ARGB(int(70 + 40 * pulse), 168, 85, 247))
                gdiplus.GdipFillEllipse(gfx, halo_b, c.c_float(dot_cx - halo_size / 2.0), c.c_float(dot_cy - halo_size / 2.0), c.c_float(halo_size), c.c_float(halo_size))
                gdiplus.GdipDeleteBrush(halo_b)

                dot_b = make_brush(theme_col['purple_dot'] if self.data['healthy'] else ARGB(255, 239, 68, 68))
                gdiplus.GdipFillEllipse(gfx, dot_b, c.c_float(dot_cx - 2.0), c.c_float(dot_cy - 2.0), c.c_float(4.0), c.c_float(4.0))
                gdiplus.GdipDeleteBrush(dot_b)

                val_txt = str(self.data['accounts']) if self.data['healthy'] else "-"
                val_rect = (c.c_float * 4)(px + 1, py + 18.0, pw - 2, 20.0)
                draw_raised_text(val_txt, val_rect, fmt_center, chip_text_color, font_main)

                sub_rect = (c.c_float * 4)(px + 1, py + 39.0, pw - 2, 16.0)
                draw_raised_text("TK", sub_rect, fmt_center, theme_col['text_secondary'], font_micro)

            draw_liquid_glass_chip(x, 5.0, chip_w, chip_h, 'account', 0, draw_vert_account)
            self.zones.append(('account', x, 5.0, chip_w, chip_h))

            # 2. Vertical 5h Quota Card
            def draw_vert_5h(px, py, pw, ph):
                pct = self.data['five_hour_pct']
                lbl_rect = (c.c_float * 4)(px + 1, py + 5.0, pw - 2, 14.0)
                draw_raised_text("5h", lbl_rect, fmt_center, theme_col['text_secondary'], font_micro)

                val_txt = f"{pct}%" if self.data['healthy'] else "--"
                val_rect = (c.c_float * 4)(px + 1, py + 18.0, pw - 2, 20.0)
                st_col = self.get_quota_text_color(pct) if self.data['healthy'] else ARGB(255, 148, 163, 184)
                draw_raised_text(val_txt, val_rect, fmt_center, st_col, font_main)

                # Mini bottom indicator
                ind_cx = px + pw / 2.0
                ind_cy = py + 46.0
                if self.data['healthy']:
                    draw_quota_indicator(ind_cx, ind_cy, pct, self.get_status_color(pct), self.s['theme'])

            draw_liquid_glass_chip(x, 69.0, chip_w, chip_h, '5h', self.data['five_hour_pct'], draw_vert_5h)
            self.zones.append(('5h', x, 69.0, chip_w, chip_h))

            # 3. Vertical Week Quota Card
            def draw_vert_week(px, py, pw, ph):
                pct = self.data['weekly_pct']
                lbl_rect = (c.c_float * 4)(px + 1, py + 5.0, pw - 2, 14.0)
                draw_raised_text("Tuần", lbl_rect, fmt_center, theme_col['text_secondary'], font_micro)

                val_txt = f"{pct}%" if self.data['healthy'] else "--"
                val_rect = (c.c_float * 4)(px + 1, py + 18.0, pw - 2, 20.0)
                st_col = self.get_quota_text_color(pct) if self.data['healthy'] else ARGB(255, 148, 163, 184)
                draw_raised_text(val_txt, val_rect, fmt_center, st_col, font_main)

                ind_cx = px + pw / 2.0
                ind_cy = py + 46.0
                if self.data['healthy']:
                    draw_quota_indicator(ind_cx, ind_cy, pct, self.get_status_color(pct), self.s['theme'])

            draw_liquid_glass_chip(x, 133.0, chip_w, chip_h, 'week', self.data['weekly_pct'], draw_vert_week)
            self.zones.append(('week', x, 133.0, chip_w, chip_h))

            # Vertical Actions (All width = 32.0, x = 4.0, perfectly straight column)
            draw_circle_action(x, 199.0, 32.0, 'refresh', lambda cx, cy: draw_refresh_icon(cx, cy))
            self.zones.append(('refresh', x, 199.0, 32.0, 32.0))

            draw_circle_action(x, 237.0, 32.0, 'lock', lambda cx, cy: draw_lock_icon(cx, cy, self.s['locked']))
            self.zones.append(('lock', x, 237.0, 32.0, 32.0))

        else:
            layout = layout_obj
            self.zones = []

            if is_compact_tw:
                # Chế độ thu gọn: CHỈ VẼ DUY NHẤT CHIP TEAMWORK (NGHIỆM THU / ĐỀ XUẤT)
                if 'teamwork' in layout.boxes:
                    teamwork = layout.boxes['teamwork']
                    draw_liquid_glass_chip(teamwork.x, teamwork.y, teamwork.w, teamwork.h, 'teamwork', 0, draw_teamwork_content)
                    self.zones.append(('teamwork', teamwork.x, teamwork.y, teamwork.w, teamwork.h))
            else:
                # All normal horizontal themes use exactly the same rectangles.
                # Order: account -> 5h -> week -> switch -> refresh -> lock
                account = layout.boxes['account']
                five_hour = layout.boxes['5h']
                week = layout.boxes['week']
                switch = layout.boxes['switch']
                refresh = layout.boxes['refresh']
                lock = layout.boxes['lock']

                draw_liquid_glass_chip(account.x, account.y, account.w, account.h, 'account', 0, draw_account_content)
                self.zones.append(('account', account.x, account.y, account.w, account.h))
                draw_liquid_glass_chip(five_hour.x, five_hour.y, five_hour.w, five_hour.h, '5h', self.data['five_hour_pct'], draw_5h_content)
                self.zones.append(('5h', five_hour.x, five_hour.y, five_hour.w, five_hour.h))
                draw_liquid_glass_chip(week.x, week.y, week.w, week.h, 'week', self.data['weekly_pct'], draw_week_content)
                self.zones.append(('week', week.x, week.y, week.w, week.h))

                if 'teamwork' in layout.boxes:
                    teamwork = layout.boxes['teamwork']
                    draw_liquid_glass_chip(teamwork.x, teamwork.y, teamwork.w, teamwork.h, 'teamwork', 0, draw_teamwork_content)
                    self.zones.append(('teamwork', teamwork.x, teamwork.y, teamwork.w, teamwork.h))

                draw_liquid_glass_chip(switch.x, switch.y, switch.w, switch.h, 'switch', 0, draw_switch_content)
                self.zones.append(('switch', switch.x, switch.y, switch.w, switch.h))

                # Actions use a capped visual size even in a tall widget; their
                # glass column stretches with the bar but the symbols stay clear.
                for name, rect, painter in (
                    ('refresh', refresh, lambda cx, cy, s: draw_refresh_icon(cx, cy, s)),
                    ('lock', lock, lambda cx, cy, s: draw_lock_icon(cx, cy, self.s['locked'], s)),
                ):
                    icon_scale = min(1.85, min(rect.w, rect.h) / PILL_H)
                    draw_liquid_glass_chip(rect.x, rect.y, rect.w, rect.h, name, 0,
                        lambda cx, cy, cw, ch, painter=painter, icon_scale=icon_scale: painter(cx + cw / 2.0, cy + ch / 2.0, icon_scale))
                    self.zones.append((name, rect.x, rect.y, rect.w, rect.h))

        # Viền nét đứt màu xanh cyan bao quanh chính xác cụm chip khi mở khóa
        if not self.s.get('locked') and self.zones:
            min_x = min(z[1] for z in self.zones)
            min_y = min(z[2] for z in self.zones)
            max_x = max(z[1] + z[3] for z in self.zones)
            max_y = max(z[2] + z[4] for z in self.zones)

            pad_x = 3.0 * content_scale
            pad_y = 3.0 * content_scale
            bx = max(1.0, min_x - pad_x)
            by = max(1.0, min_y - pad_y)
            bw = min(float(self.w) - bx - 1.0, (max_x - min_x) + pad_x * 2.0)
            bh = min(float(self.h) - by - 1.0, (max_y - min_y) + pad_y * 2.0)

            corner_r = min(12.0 * content_scale, bh / 2.0)
            grab_path = create_pill_path(bx, by, bw, bh, corner_r)
            grab_pen = make_pen(ARGB(255, 56, 189, 248), 1.6)
            gdiplus.GdipSetPenDashStyle(grab_pen, 1)  # DashStyleDash
            gdiplus.GdipDrawPath(gfx, grab_pen, grab_path)
            gdiplus.GdipDeletePen(grab_pen)
            gdiplus.GdipDeletePath(grab_path)

        # Cleanup GDI+
        gdiplus.GdipDeleteGraphics(gfx)
        gdiplus.GdipDeleteFont(font_main)
        gdiplus.GdipDeleteFont(font_nano)
        gdiplus.GdipDeleteFont(font_micro)
        gdiplus.GdipDeleteFont(font_badge)
        gdiplus.GdipDeleteFontFamily(font_family)
        gdiplus.GdipDeleteStringFormat(fmt_left)
        gdiplus.GdipDeleteStringFormat(fmt_quota)
        gdiplus.GdipDeleteStringFormat(fmt_center)

        # Update layered window with exact physical dimensions.  State may have
        # been saved before a monitor/DPI change, so never let a valid card be
        # restored outside the current virtual desktop.
        rect = w.RECT()
        if self.hwnd and user32.GetWindowRect(self.hwnd, c.byref(rect)) and rect.right > rect.left:
            cur_x, cur_y = rect.left, rect.top
            self.s['x'], self.s['y'] = cur_x, cur_y
        else:
            cur_x, cur_y = self.s['x'], self.s['y']
        pt_dest = POINT(cur_x, cur_y)
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

    def hit_test(self, px, py):
        for btn_id, x, y, w_pill, h_pill in self.zones:
            if x <= px <= x + w_pill and y <= py <= y + h_pill:
                return btn_id
        return None

    def resolve_hit_point(self, px, py):
        """Use physical client coordinates first; fall back only for legacy DPI."""
        if self.hit_test(px, py) is not None:
            return px, py
        return self.render_point(px, py)

    def render_point(self, px, py):
        """Map a Win32 client point into the layered-render bitmap space.

        On mixed-DPI desktops Windows can deliver client mouse coordinates in
        virtual pixels even when the DIB is in physical pixels.  The old code
        fed those values straight into physical card rectangles, making the
        right-hand chips look present but impossible to click or drag.
        """
        rect = w.RECT()
        if not self.hwnd or not user32.GetWindowRect(self.hwnd, c.byref(rect)):
            return px, py
        raw_w = max(1, rect.right - rect.left)
        try:
            dpi = int(user32.GetDpiForWindow(self.hwnd) or 96)
        except Exception:
            dpi = 96
        factor = max(1.0, dpi / 96.0)
        scaled_w = raw_w * factor
        # Only scale if it demonstrably restores the known render width. This
        # keeps 100% DPI and already-physical coordinate paths unchanged.
        if factor > 1.0 and abs(scaled_w - self.w) + 1.0 < abs(raw_w - self.w):
            return px * factor, py * factor
        return px, py

    def begin_drag(self, hwnd, px, py, pending_click=None, immediate=False):
        cursor = POINT()
        rect = w.RECT()
        if not user32.GetCursorPos(c.byref(cursor)) or not user32.GetWindowRect(hwnd, c.byref(rect)):
            return
        self.drag = POINT(px, py)
        self.drag_cursor_start = POINT(cursor.x, cursor.y)
        self.drag_window_start = POINT(rect.left, rect.top)
        self.drag_moved = bool(immediate)
        self.pending_click = pending_click
        user32.SetCapture(hwnd)

    def activate_button(self, btn):
        if btn == 'lock':
            self.set_locked(not self.s['locked'])
            self.update_tooltip(btn)
        elif btn == 'refresh':
            self.refresh_data()
        elif btn in ('switch', 'context'):
            self.open_account_picker()
        elif btn == 'account':
            self.toggle_account_popover()
        elif btn == 'teamwork':
            self.toggle_teamwork_popover()

    def toggle_teamwork_popover(self):
        if not self.teamwork_popover:
            return
        if self.teamwork_popover.visible:
            self.teamwork_popover.hide()
            return
        for z_id, zx, zy, zw, zh in self.zones:
            if z_id == 'teamwork':
                wrect = w.RECT()
                user32.GetWindowRect(self.hwnd, c.byref(wrect))
                chip_rect = (wrect.left + zx, wrect.top + zy, wrect.left + zx + zw, wrect.top + zy + zh)
                self.teamwork_popover.show(chip_rect)
                self.popover_until = time.monotonic() + 4.0
                break

    def toggle_account_popover(self):
        if not self.popover:
            return
        if self.popover.visible and self.popover.focus_type == 'account':
            self.popover.hide()
            return
        for z_id, zx, zy, zw, zh in self.zones:
            if z_id == 'account':
                wrect = w.RECT()
                user32.GetWindowRect(self.hwnd, c.byref(wrect))
                chip_rect = (wrect.left + zx, wrect.top + zy, wrect.left + zx + zw, wrect.top + zy + zh)
                self.popover.show(chip_rect, 'account')
                self.popover_until = time.monotonic() + 4.0
                break


    def refresh_data(self):
        self.refreshing_spin = 10
        self.data = query_antigravity_data()
        self.context = get_context_status()
        old_w, old_h = self.w, self.h
        self.sync_dimensions()
        if (self.w != old_w or self.h != old_h) and self.hwnd:
            user32.SetWindowPos(self.hwnd, 0, self.s['x'], self.s['y'], self.w, self.h, 0x0002 | 0x0010 | 0x0004)
        self.update_layered_render()

    def open_cockpit_tools(self, product=None, account_id=None):
        """Open Cockpit's owner UI; only it performs encrypted account switching."""
        self.selected_account_product = product
        self.selected_account_id = account_id
        cockpit_hwnd = user32.FindWindowW(None, 'Cockpit Tools')
        if cockpit_hwnd:
            user32.ShowWindow(cockpit_hwnd, 9)  # SW_RESTORE
            user32.SetForegroundWindow(cockpit_hwnd)
            return
        if COCKPIT_EXE.exists():
            subprocess.Popen([str(COCKPIT_EXE)])

    def open_account_picker(self):
        """Show unified Cockpit Antigravity accounts with real-time quota stats in a single flat menu.
        No split submenus (không chia đôi), showing exact quota parameters for each account
        so the user can immediately pick the richest account to switch to.
        """
        acc_data = get_cockpit_accounts_with_quota()
        root_menu = user32.CreatePopupMenu()
        item_map = {}
        next_id = 520

        try:
            # 1. Active account at the very top
            active_list = acc_data.get('active', [])
            if active_list:
                for row in active_list:
                    label = f"● {row['clean_name']} (Hiện tại)\t{row['status_text']}"
                    user32.AppendMenuW(root_menu, 0x0008, next_id, label)  # MF_CHECKED
                    item_map[next_id] = row
                    next_id += 1
                user32.AppendMenuW(root_menu, 0x0800, 0, None)  # MF_SEPARATOR

            # 2. Ready accounts with quota (sorted from highest quota to lowest)
            ready_list = acc_data.get('ready', [])
            if ready_list:
                for row in ready_list:
                    label = f"   {row['clean_name']}\t{row['status_text']}"
                    user32.AppendMenuW(root_menu, 0, next_id, label)
                    item_map[next_id] = row
                    next_id += 1

            # 3. Empty / No-cache accounts
            empty_list = acc_data.get('empty', [])
            if empty_list:
                if ready_list:
                    user32.AppendMenuW(root_menu, 0x0800, 0, None)  # MF_SEPARATOR
                for row in empty_list:
                    label = f"   {row['clean_name']}\t{row['status_text']}"
                    user32.AppendMenuW(root_menu, 0, next_id, label)
                    item_map[next_id] = row
                    next_id += 1

            # Bottom controls
            user32.AppendMenuW(root_menu, 0x0800, 0, None)  # MF_SEPARATOR
            user32.AppendMenuW(root_menu, 0, 598, "⟳ Làm mới dữ liệu Quota")
            user32.AppendMenuW(root_menu, 0, 599, "⚙ Mở Cockpit Tools…")

            point = POINT()
            user32.GetCursorPos(c.byref(point))
            user32.SetForegroundWindow(self.hwnd)
            command = user32.TrackPopupMenu(root_menu, 0x0100 | 0x0002, point.x, point.y, 0, self.hwnd, None)
        finally:
            user32.DestroyMenu(root_menu)

        if command in item_map:
            target = item_map[command]
            switch_active_account(target['id'], target['email'])
            self.open_cockpit_tools('antigravity', target['id'])
            self.refresh_data()
        elif command == 598:
            self.refresh_data()
        elif command == 599:
            self.open_cockpit_tools()

    def refresh_context_from_antigravity(self):
        """Refresh the read-only Antigravity context indicator.

        Antigravity does not expose a documented equivalent of Codex's /compact
        command or local token counter.  Never inject an unsupported command into
        the IDE merely because the old Codex widget had that shortcut.
        """
        def trace(message):
            with LOG_PATH.open('a', encoding='utf-8') as f:
                f.write(f"compact: {message}\n")

        trace('CTX action: refresh only; unsupported command injection is disabled')
        self.refresh_data()

    def handle_context_double_click(self):
        """Layered windows can lose WM_LBUTTONDBLCLK, so detect the pair ourselves."""
        now = time.monotonic()
        if now - self.context_last_fire_at < 0.8:
            return
        if now - self.context_click_at <= 0.60:
            self.context_click_at = 0.0
            self.context_last_fire_at = now
            self.refresh_context_from_antigravity()
        else:
            self.context_click_at = now

    def track_codex_window(self):
        # HWNDs are valid only for one live native window.  On a real close,
        # forget it and dynamically discover the next Codex window; on a mere
        # minimize, keep it so the widget never jumps to a parallel session.
        self.forget_closed_codex_owner()
        codex_info = find_codex_window(
            include_minimized=True,
            preferred_hwnd=self.last_codex_hwnd,
            strict_preferred=bool(self.s['locked'] and self.last_codex_hwnd),
        )
        if not codex_info:
            old_active = getattr(self, 'has_active_antigravity', None)
            self.has_active_antigravity = False
            if old_active is not False:
                self.sync_dimensions()
                self.update_layered_render()
            if not self.is_visible:
                user32.ShowWindow(self.hwnd, 8)
                self.is_visible = True
            user32.SetWindowPos(self.hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040)
            return

        hwnd_c, cl, ct, cr, cb, confirmed = codex_info
        self.bind_to_codex_owner(hwnd_c)
        self.last_codex_hwnd = hwnd_c
        if user32.IsIconic(hwnd_c):
            old_active = getattr(self, 'has_active_antigravity', None)
            self.has_active_antigravity = False
            if old_active is not False:
                self.sync_dimensions()
                self.update_layered_render()
            self.codex_minimized_ticks += 1
            if self.owner_hwnd == hwnd_c:
                self.owner_hwnd = None
            if not self.is_visible:
                user32.ShowWindow(self.hwnd, 8)
                self.is_visible = True
            user32.SetWindowPos(self.hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010 | 0x0040)
            return

        old_active = getattr(self, 'has_active_antigravity', None)
        self.has_active_antigravity = True
        if old_active is not True:
            self.sync_dimensions()
            self.update_layered_render()

        self.codex_minimized_ticks = 0
        if not user32.IsWindowVisible(self.hwnd):
            user32.ShowWindow(self.hwnd, 8)  # SW_SHOWNA
        self.is_visible = True

        self.has_confirmed_codex = self.has_confirmed_codex or confirmed
        self.last_codex_rect = (cl, ct, cr, cb)
        user32.SetWindowPos(self.hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002 | 0x0010)

        self.sync_dimensions()

        if self.native_drag:
            return

        if self.s['locked'] and self.s['rel_x'] is not None and self.s['rel_y'] is not None:
            target_x = cl + self.s['rel_x']
            target_y = ct + self.s['rel_y']
        elif self.s['locked']:
            if self.s['orientation'] == 'vertical':
                target_x = cr - self.w - 12
                target_y = max(ct + 12, int(ct + (cb - ct - self.h) / 2.0))
            else:
                target_x = max(cl + 12, cr - self.w - 12)
                target_y = cb - self.h - 14
        else:
            target_x = self.s['x']
            target_y = self.s['y']

        if self.s['locked']:
            target_x = max(cl + 12, min(target_x, cr - self.w - 12))
            target_y = max(ct + 12, min(target_y, cb - self.h - 14))
            self.s['rel_x'] = target_x - cl
            self.s['rel_y'] = target_y - ct

        if not self.is_visible:
            user32.ShowWindow(self.hwnd, 8)
            self.is_visible = True

        position_changed = target_x != self.s['x'] or target_y != self.s['y']
        if position_changed:
            self.s['x'] = target_x
            self.s['y'] = target_y

        # Z-order is a separate invariant from position.  A restored widget can
        # already have the right coordinates while sitting below Codex; always
        # reinsert a locked widget directly above its owner window.
        if self.s['locked']:
            self.move_in_codex_layer(target_x, target_y)

        if position_changed:
            self.update_layered_render()

    def update_tooltip(self, btn_id):
        if not self.hwnd_tt:
            return

        text = ""
        if btn_id == 'account':
            text = (f"TÀI KHOẢN ANTIGRAVITY\n{self.data.get('accounts', 0)} tài khoản · Hover để xem Top 4 quota và chuyển nhanh")
        elif btn_id == '5h':
            text = (f"ACC HIỆN TẠI · 5 GIỜ\nGemini: {self.data.get('five_hour_pct', 0)}% · Claude/GPT: {self.data.get('claude_five_hour_pct', 0)}%\n"
                    f"Reset Gemini: {self.data.get('five_hour_reset', 'chưa rõ')}") if self.data['healthy'] else "ACC HIỆN TẠI\nKhông có dữ liệu quota"
        elif btn_id == 'week':
            text = (f"QUOTA TUẦN\nGemini: {self.data.get('weekly_pct', 0)}% · Claude/GPT: {self.data.get('claude_weekly_pct', 0)}%\n"
                    f"Reset Gemini: {self.data.get('weekly_reset', 'chưa rõ')}") if self.data['healthy'] else "QUOTA TUẦN\nKhông có dữ liệu quota"
        elif btn_id == 'switch':
            text = "⇄ TẤT CẢ TÀI KHOẢN\nXem danh sách đầy đủ tất cả tài khoản trong Cockpit Tools"
        elif btn_id == 'refresh':
            text = "Làm mới dữ liệu quota ngay"
        elif btn_id == 'lock':
            text = "🔒 Đang ghim vào Antigravity (Bấm để mở khóa kéo thả)" if self.s['locked'] else "🔓 Đã mở khóa (Bấm để ghim vào Antigravity)"

        if text != self.current_tooltip_text:
            self.current_tooltip_text = text
            ti = TOOLINFO()
            ti.cbSize = c.sizeof(TOOLINFO)
            ti.uFlags = 0x0001 | 0x0010 | 0x0020
            ti.hwnd = self.hwnd
            ti.uId = self.hwnd
            ti.lpszText = text
            user32.SendMessageW(self.hwnd_tt, 0x0439, 0, c.byref(ti))
            if text:
                pt = POINT()
                user32.GetCursorPos(c.byref(pt))
                tip_x = pt.x + 12
                tip_y = pt.y + 22
                user32.SendMessageW(self.hwnd_tt, 0x0412, 0, (tip_y << 16) | (tip_x & 0xFFFF))
                user32.SendMessageW(self.hwnd_tt, 0x0411, 1, c.byref(ti))
            else:
                user32.SendMessageW(self.hwnd_tt, 0x0411, 0, c.byref(ti))

    def open_context_menu(self, screen_x, screen_y):
        hmenu = user32.CreatePopupMenu()

        theme_menu = user32.CreatePopupMenu()
        user32.AppendMenuW(theme_menu, 0x0008 if self.s['theme'] == 'battery' else 0, 101, "🔋 Liquid Battery (Pin năng lượng)")
        user32.AppendMenuW(theme_menu, 0x0008 if self.s['theme'] == 'bar' else 0, 102, "▬ Cyber Slim Bar (Thanh phát sáng)")
        user32.AppendMenuW(theme_menu, 0x0008 if self.s['theme'] == 'ring' else 0, 103, "◯ Holographic Ring (Vòng tiến trình)")
        user32.AppendMenuW(theme_menu, 0x0008 if self.s['theme'] == 'orbit' else 0, 104, "⚡ Aurora Orbit (Viền Neon thở)")
        user32.AppendMenuW(theme_menu, 0x0008 if self.s['theme'] == 'cards' else 0, 105, "🎴 Frosted Pill Cards (Thẻ kính)")
        user32.AppendMenuW(theme_menu, 0x0008 if self.s['theme'] == 'nano' else 0, 106, "▫️ Nano Minimalist (Siêu mảnh 20px)")
        user32.AppendMenuW(hmenu, 0x0010, theme_menu, "🎨 Giao diện (Themes)")

        glass_menu = user32.CreatePopupMenu()
        cur_glass = self.s.get('glass_mode', 'deep_obsidian')
        user32.AppendMenuW(glass_menu, 0x0008 if cur_glass == 'deep_obsidian' else 0, 121, GLASS_NAMES['deep_obsidian'])
        user32.AppendMenuW(glass_menu, 0x0008 if cur_glass == 'smoked_glass' else 0, 122, GLASS_NAMES['smoked_glass'])
        user32.AppendMenuW(glass_menu, 0x0008 if cur_glass == 'frosted_diamond' else 0, 123, GLASS_NAMES['frosted_diamond'])
        user32.AppendMenuW(glass_menu, 0x0008 if cur_glass == 'pure_frost' else 0, 124, GLASS_NAMES['pure_frost'])
        user32.AppendMenuW(glass_menu, 0x0008 if cur_glass == 'aurora_borealis' else 0, 125, GLASS_NAMES['aurora_borealis'])
        user32.AppendMenuW(glass_menu, 0x0008 if cur_glass == 'ghost_glass' else 0, 126, GLASS_NAMES['ghost_glass'])
        user32.AppendMenuW(hmenu, 0x0010, glass_menu, "💎 Chất liệu Kính (Glass Material)")

        scale_menu = user32.CreatePopupMenu()
        cur_scale = int(self.s.get('scale_percent', 140))
        scale_options = [
            (80, "🔍 80% (Nhỏ gọn)"),
            (100, "🔍 100% (Tiêu chuẩn)"),
            (110, "🔍 110% (Vừa vặn)"),
            (125, "🔍 125% (To rõ)"),
            (140, "🔍 140% (Lớn rõ nét - Khuyên dùng)"),
            (150, "🔍 150% (Rất lớn)"),
            (160, "🔍 160% (Cực đại)"),
            (180, "🔍 180% (Khổng lồ)"),
            (200, "🔍 200% (Gấp đôi)"),
        ]
        for idx, (sc_val, sc_txt) in enumerate(scale_options):
            user32.AppendMenuW(scale_menu, 0x0008 if cur_scale == sc_val else 0, 501 + idx, sc_txt)
        user32.AppendMenuW(hmenu, 0x0010, scale_menu, "🔎 Kích thước / Tỉ lệ (Resize)")

        user32.AppendMenuW(hmenu, 0x0800, 0, None)

        user32.AppendMenuW(hmenu, 0, 108, "🎨 Tùy chỉnh màu chữ Neon...")
        user32.AppendMenuW(hmenu, 0, 109, "↺ Đặt lại màu chữ tự động theo Quota")
        user32.AppendMenuW(hmenu, 0x0800, 0, None)

        rotate_txt = "↕ Xoay sang Hàng Ngang" if self.s['orientation'] == 'vertical' else "↔ Xoay sang Cột Dọc"
        user32.AppendMenuW(hmenu, 0, 201, rotate_txt)
        user32.AppendMenuW(hmenu, 0x0800, 0, None)

        lock_txt = "🔓 Mở khóa để kéo tự do & Resize" if self.s['locked'] else "🔒 Khóa và ghim vào cửa sổ Antigravity"
        user32.AppendMenuW(hmenu, 0, 301, lock_txt)

        anchor_menu = user32.CreatePopupMenu()
        user32.AppendMenuW(anchor_menu, 0, 311, "↗ Góc Trên - Phải (Header / Tab bar)")
        user32.AppendMenuW(anchor_menu, 0, 312, "⬆ Góc Trên - Giữa")
        user32.AppendMenuW(anchor_menu, 0, 313, "↘ Góc Dưới - Phải (Status bar)")
        user32.AppendMenuW(anchor_menu, 0, 314, "⬇ Góc Dưới - Giữa")
        user32.AppendMenuW(anchor_menu, 0, 315, "↖ Góc Trên - Trái")
        user32.AppendMenuW(hmenu, 0x0010, anchor_menu, "📌 Vị trí Neo trên Antigravity (Anchors)")

        user32.AppendMenuW(hmenu, 0, 302, "📍 Đặt lại vị trí mặc định trên Antigravity")
        user32.AppendMenuW(hmenu, 0, 303, "↻ Làm mới hạn mức ngay lập tức")
        user32.AppendMenuW(hmenu, 0x0800, 0, None)

        user32.AppendMenuW(hmenu, 0, 401, "🚀 Mở Cockpit Tools...")
        user32.AppendMenuW(hmenu, 0, 402, "❌ Đóng Widget")

        user32.SetForegroundWindow(self.hwnd)
        cmd = user32.TrackPopupMenu(hmenu, 0x0100 | 0x0002, screen_x, screen_y, 0, self.hwnd, None)
        user32.DestroyMenu(theme_menu)
        user32.DestroyMenu(glass_menu)
        user32.DestroyMenu(scale_menu)
        user32.DestroyMenu(anchor_menu)
        user32.DestroyMenu(hmenu)

        if 501 <= cmd < 501 + len(scale_options):
            selected_scale = scale_options[cmd - 501][0]
            self.s['scale_percent'] = selected_scale
            self.sync_dimensions()
            self.move_in_codex_layer(self.s['x'], self.s['y'])
            save_state(self.s)
            self.update_layered_render()
            return

        if cmd == 101:
            self.s['theme'] = 'battery'
        elif cmd == 102:
            self.s['theme'] = 'bar'
        elif cmd == 103:
            self.s['theme'] = 'ring'
        elif cmd == 104:
            self.s['theme'] = 'orbit'
        elif cmd == 105:
            self.s['theme'] = 'cards'
        elif cmd == 106:
            self.s['theme'] = 'nano'
        elif cmd == 121:
            self.s['glass_mode'] = 'deep_obsidian'
        elif cmd == 122:
            self.s['glass_mode'] = 'smoked_glass'
        elif cmd == 123:
            self.s['glass_mode'] = 'frosted_diamond'
        elif cmd == 124:
            self.s['glass_mode'] = 'pure_frost'
        elif cmd == 125:
            self.s['glass_mode'] = 'aurora_borealis'
        elif cmd == 126:
            self.s['glass_mode'] = 'ghost_glass'
        elif cmd == 108:
            self.choose_chip_text_color()
            return
        elif cmd == 109:
            self.s['chip_text_rgb'] = None
        elif cmd == 201:
            self.set_orientation('horizontal' if self.s['orientation'] == 'vertical' else 'vertical')
            return
        elif cmd == 301:
            self.set_locked(not self.s['locked'])
            return
        elif 311 <= cmd <= 315:
            presets = {
                311: 'top_right',
                312: 'top_center',
                313: 'bottom_right',
                314: 'bottom_center',
                315: 'top_left'
            }
            self.snap_to_preset(presets[cmd])
            return
        elif cmd == 302:
            self.snap_to_preset('top_right')
            return
        elif cmd == 303:
            self.refresh_data()
            return
        elif cmd == 401:
            self.open_cockpit_tools()
            return
        elif cmd == 402:
            user32.PostQuitMessage(0)
            return

        self.sync_dimensions()
        self.move_in_codex_layer(self.s['x'], self.s['y'])
        save_state(self.s)
        self.update_layered_render()

    def set_orientation(self, orientation):
        if orientation not in ('horizontal', 'vertical'):
            return
        self.s['orientation'] = orientation
        self.sync_dimensions()
        save_state(self.s)
        self.move_in_codex_layer(self.s['x'], self.s['y'])
        self.update_layered_render()

    def _on_drag_finished(self, hwnd):
        self.drag = None
        self.drag_cursor_start = None
        self.drag_window_start = None
        self.drag_moved = False
        self.pending_click = None
        self.native_drag = False
        self.resizing = False
        self.in_sizemove = False
        user32.ReleaseCapture()

        rect = w.RECT()
        user32.GetWindowRect(hwnd, c.byref(rect))
        self.s['x'], self.s['y'] = rect.left, rect.top
        if self.last_codex_rect:
            cl, ct, _, _ = self.last_codex_rect
            self.s['rel_x'] = rect.left - cl
            self.s['rel_y'] = rect.top - ct
        save_state(self.s)
        self.move_in_codex_layer(self.s['x'], self.s['y'])
        self.update_layered_render()

    def proc(self, hwnd, msg, wp, lp):
        try:
            if msg in (2, 16, 0x0010, 0x0012):  # WM_DESTROY, WM_CLOSE, WM_QUIT
                with LOG_PATH.open('a', encoding='utf-8') as f:
                    f.write(f"proc(): received exit msg={msg}, wp={wp}, lp={lp}\n")
                    f.flush()
            return self._proc_impl(hwnd, msg, wp, lp)
        except Exception:
            import traceback
            with LOG_PATH.open('a', encoding='utf-8') as f:
                traceback.print_exc(file=f)
            return user32.DefWindowProcW(hwnd, msg, wp, lp)

    def _proc_impl(self, hwnd, msg, wp, lp):
        if msg == 0x0084:  # WM_NCHITTEST
            rect = w.RECT()
            user32.GetWindowRect(hwnd, c.byref(rect))
            sx = c.c_short(lp & 0xFFFF).value
            sy = c.c_short((lp >> 16) & 0xFFFF).value
            client_x = sx - rect.left
            client_y = sy - rect.top
            raw_btn = self.hit_test(client_x, client_y)
            mapped_x, mapped_y = self.render_point(client_x, client_y)
            btn = raw_btn or self.hit_test(mapped_x, mapped_y)

            # Interactive chips receive clicks directly
            if btn is not None:
                return 1  # HTCLIENT

            # All background and padding areas provide smooth 144Hz native dragging
            return 2  # HTCAPTION

        if msg == 0x0024:  # WM_GETMINMAXINFO: allow smooth desktop sizing
            limits = c.cast(c.c_void_p(lp), c.POINTER(MINMAXINFO)).contents
            limits.ptMinTrackSize.x = 350
            limits.ptMinTrackSize.y = 24
            limits.ptMaxTrackSize.x = 2500
            limits.ptMaxTrackSize.y = 250
            return 0

        if msg == 0x0005:  # WM_SIZE
            return 0

        if msg == 0x0231:  # WM_ENTERSIZEMOVE
            self.resizing = True
            self.in_sizemove = True
            self.native_drag = True
            return 0

        if msg == 1:
            self.hwnd = hwnd
            hinst = kernel32.GetModuleHandleW(None)
            self.hwnd_tt = user32.CreateWindowExW(
                0x00000008 | 0x00000020 | 0x08000000, "tooltips_class32", None,
                0x80000000 | 0x01 | 0x02, 0, 0, 0, 0,
                hwnd, None, hinst, None
            )
            user32.SendMessageW(self.hwnd_tt, 0x0403, 3, 150)
            user32.SendMessageW(self.hwnd_tt, 0x0403, 2, 3500)

            ti = TOOLINFO()
            ti.cbSize = c.sizeof(TOOLINFO)
            ti.uFlags = 0x0001 | 0x0010 | 0x0020
            ti.hwnd = hwnd
            ti.uId = hwnd
            ti.lpszText = "Cockpit Quota Widget V10 Pro Ultimate"
            user32.SendMessageW(self.hwnd_tt, 0x0432, 0, c.byref(ti))

            try:
                self.popover = CockpitGlassPopover(self)
                self.teamwork_popover = TeamworkGlassPopover(self)
            except Exception:
                pass

            user32.SetTimer(hwnd, 1, 15000, None)
            user32.SetTimer(hwnd, 2, 250, None)
            self.refresh_data()
            self._dock_to_visible_antigravity()
            return 0

        elif msg == 275:
            if wp == 1:
                self.refresh_data()
            elif wp == 2:
                # If window is currently dragging or in sizemove modal loop, NEVER redock or interfere!
                if self.drag or self.resizing or getattr(self, 'native_drag', False) or getattr(self, 'in_sizemove', False):
                    return 0
                self.animation_tick = (self.animation_tick + 1) % 120
                if self.refreshing_spin > 0:
                    self.refreshing_spin -= 1
                self._dock_to_visible_antigravity()
                if self.popover and self.popover.visible:
                    pt = POINT()
                    user32.GetCursorPos(c.byref(pt))
                    if self.popover.contains_point(pt.x, pt.y):
                        self.popover_until = max(self.popover_until, time.monotonic() + 2.5)
                    elif time.monotonic() >= self.popover_until:
                        self.popover.hide()
                tw_info = self.teamwork_service.get_display_info() if hasattr(self, 'teamwork_service') else {'active': False, 'status': 'IDLE'}
                tw_active = tw_info.get('active', False)
                current_tw_st = tw_info.get('status', 'IDLE')
                last_tw_st = getattr(self, '_last_tw_status', None)
                tw_updated_at = tw_info.get('updated_at', 0.0)
                last_tw_updated_at = getattr(self, '_last_tw_updated_at', 0.0)

                # Auto-popup when a new proposal or acceptance arrives from Antigravity IDE
                has_pending_response = bool(tw_service and tw_service.get_state().get('response'))
                is_new_event = (current_tw_st in ('PROPOSAL', 'ACCEPTANCE')) and not has_pending_response and (
                    current_tw_st != last_tw_st or tw_updated_at > last_tw_updated_at
                )
                if is_new_event:
                    self._last_tw_status = current_tw_st
                    self._last_tw_updated_at = tw_updated_at
                    self._proposal_auto_handled = False
                    if self.teamwork_popover:
                        chip_rect = None
                        if user32.IsWindowVisible(hwnd):
                            for z_id, zx, zy, zw, zh in self.zones:
                                if z_id == 'teamwork':
                                    wrect = w.RECT()
                                    user32.GetWindowRect(hwnd, c.byref(wrect))
                                    chip_rect = (wrect.left + zx, wrect.top + zy, wrect.left + zx + zw, wrect.top + zy + zh)
                                    break
                        if not chip_rect:
                            rc_work = w.RECT()
                            user32.SystemParametersInfoW(0x0030, 0, c.byref(rc_work), 0)
                            chip_rect = (rc_work.right - 260, rc_work.top + 40, rc_work.right - 40, rc_work.top + 72)

                        self.teamwork_popover.show(chip_rect)
                        if current_tw_st == 'PROPOSAL':
                            rem_sec = max(5, tw_info.get('remaining_seconds', 150))
                            self.popover_until = time.monotonic() + rem_sec + 5.0
                        else:
                            self.popover_until = time.monotonic() + 86400.0
                elif current_tw_st in ('IDLE', 'EXECUTING') and last_tw_st not in ('IDLE', 'EXECUTING'):
                    self._last_tw_status = current_tw_st
                    if self.teamwork_popover and self.teamwork_popover.visible:
                        self.teamwork_popover.hide()

                # Auto-fallback: Khi Proposal đếm hết thời gian (rem_sec <= 0), tự động trả số 1 về Antigravity IDE
                if current_tw_st == 'PROPOSAL':
                    rem_sec = tw_info.get('remaining_seconds', 0)
                    if rem_sec <= 0 and not getattr(self, '_proposal_auto_handled', False):
                        self._proposal_auto_handled = True
                        if self.teamwork_popover:
                            self.teamwork_popover.feedback_text = "⏱️ Hết giờ: Đã tự động chọn [1] (Khuyên dùng) & Gửi về IDE!"
                            self.teamwork_popover.feedback_until = time.monotonic() + 3.0
                            self.teamwork_popover.render()
                            self.teamwork_popover.send_to_antigravity("1")
                            self.teamwork_popover.auto_hide_at = time.monotonic() + 1.8
                        if hasattr(self, 'teamwork_service'):
                            self.teamwork_service.submit_response('SELECT_OPTION', option_id=1, note="Auto-selected [1] on countdown timeout")

                if self.teamwork_popover and self.teamwork_popover.visible:
                    pt = POINT()
                    user32.GetCursorPos(c.byref(pt))
                    if self.teamwork_popover.contains_point(pt.x, pt.y):
                        self.popover_until = max(self.popover_until, time.monotonic() + 3.0)
                        self.teamwork_popover.render()
                    elif time.monotonic() >= self.popover_until:
                        self.teamwork_popover.hide()
                    else:
                        if tw_active and self.animation_tick % 4 == 0:
                            self.teamwork_popover.render()

                # Zero-Jitter optimization: Redraw when refreshing, when teamwork countdown is active, or every few seconds
                should_render = (self.refreshing_spin > 0) or (tw_active and self.animation_tick % 4 == 0) or (self.animation_tick % 12 == 0)
                if self.is_visible and should_render:
                    self.update_layered_render()
            return 0

        elif msg == 0x0200:
            tme = TRACKMOUSEEVENT(c.sizeof(TRACKMOUSEEVENT), 0x00000002, hwnd, 0)
            user32.TrackMouseEvent(c.byref(tme))
            px = c.c_short(lp & 0xFFFF).value
            py = c.c_short((lp >> 16) & 0xFFFF).value
            raw_btn = self.hit_test(px, py)
            mapped_x, mapped_y = self.render_point(px, py)
            btn = raw_btn or self.hit_test(mapped_x, mapped_y)

            # If user pressed mouse on a chip and starts moving >= 8px, transfer immediately to native smooth drag
            if self.drag:
                pt = POINT()
                user32.GetCursorPos(c.byref(pt))
                dx = pt.x - self.drag_cursor_start.x
                dy = pt.y - self.drag_cursor_start.y
                if not self.drag_moved and max(abs(dx), abs(dy)) >= 8:
                    self.drag_moved = True
                    self.pending_click = None
                    self.native_drag = True
                    self.resizing = True
                    self.in_sizemove = True
                    user32.ReleaseCapture()
                    # Engage native 144Hz Windows compositor drag!
                    user32.SendMessageW(hwnd, 0x00A1, 2, 0)  # WM_NCLBUTTONDOWN, HTCAPTION
                    self._on_drag_finished(hwnd)
                    return 0
                return 0

            if btn != self.hover_btn:
                self.hover_btn = btn
                self.update_tooltip(None if btn in ('5h', 'week', 'account') else btn)
                self.update_layered_render()

                if btn in ('5h', 'week', 'account') and self.popover and self.s.get('locked'):
                    wrect = w.RECT()
                    user32.GetWindowRect(hwnd, c.byref(wrect))
                    for z_id, zx, zy, zw, zh in self.zones:
                        if z_id == btn:
                            chip_rect = (wrect.left + zx, wrect.top + zy, wrect.left + zx + zw, wrect.top + zy + zh)
                            self.popover.show(chip_rect, btn)
                            self.popover_until = time.monotonic() + 3.5
                            break
                elif btn == 'teamwork' and self.teamwork_popover and self.s.get('locked'):
                    wrect = w.RECT()
                    user32.GetWindowRect(hwnd, c.byref(wrect))
                    for z_id, zx, zy, zw, zh in self.zones:
                        if z_id == 'teamwork':
                            chip_rect = (wrect.left + zx, wrect.top + zy, wrect.left + zx + zw, wrect.top + zy + zh)
                            self.teamwork_popover.show(chip_rect)
                            self.popover_until = time.monotonic() + 3.5
                            break
                else:
                    if self.popover and self.popover.visible:
                        pt = POINT()
                        user32.GetCursorPos(c.byref(pt))
                        if not self.popover.contains_point(pt.x, pt.y) and time.monotonic() >= self.popover_until:
                            self.popover.hide()
                    if self.teamwork_popover and self.teamwork_popover.visible:
                        pt = POINT()
                        user32.GetCursorPos(c.byref(pt))
                        if not self.teamwork_popover.contains_point(pt.x, pt.y) and time.monotonic() >= self.popover_until:
                            self.teamwork_popover.hide()
            return 0

        elif msg == 0x02A3:
            if self.hover_btn is not None:
                self.hover_btn = None
                self.update_tooltip(None)
                self.update_layered_render()
            if self.popover and self.popover.visible:
                pt = POINT()
                user32.GetCursorPos(c.byref(pt))
                if not self.popover.contains_point(pt.x, pt.y):
                    self.popover_until = max(self.popover_until, time.monotonic() + 0.8)
            if self.teamwork_popover and self.teamwork_popover.visible:
                pt = POINT()
                user32.GetCursorPos(c.byref(pt))
                if not self.teamwork_popover.contains_point(pt.x, pt.y):
                    self.popover_until = max(self.popover_until, time.monotonic() + 0.8)
            return 0

        elif msg == 0x0201:
            px = c.c_short(lp & 0xFFFF).value
            py = c.c_short((lp >> 16) & 0xFFFF).value
            px, py = self.resolve_hit_point(px, py)
            btn = self.hit_test(px, py)

            # Start drag tracking: click-to-activate or drag-to-move both supported seamlessly
            self.begin_drag(hwnd, px, py, pending_click=btn)
            return 0

        elif msg == 0x0203:
            px = c.c_short(lp & 0xFFFF).value
            py = c.c_short((lp >> 16) & 0xFFFF).value
            px, py = self.resolve_hit_point(px, py)
            btn = self.hit_test(px, py)
            if btn == '5h':
                cur_idx = THEMES.index(self.s['theme']) if self.s['theme'] in THEMES else 0
                self.s['theme'] = THEMES[(cur_idx + 1) % len(THEMES)]
                self.sync_dimensions()
                self.move_in_codex_layer(self.s['x'], self.s['y'])
                save_state(self.s)
                self.update_tooltip(btn)
                self.update_layered_render()
            elif btn == 'week':
                cur_idx = GLASS_MODES.index(self.s.get('glass_mode', 'deep_obsidian')) if self.s.get('glass_mode') in GLASS_MODES else 0
                self.s['glass_mode'] = GLASS_MODES[(cur_idx + 1) % len(GLASS_MODES)]
                save_state(self.s)
                self.update_tooltip(btn)
                self.update_layered_render()
            elif btn == 'account':
                self.toggle_account_popover()
            return 0

        elif msg in (0x0202, 0x0215):  # WM_LBUTTONUP / WM_CAPTURECHANGED
            if self.drag:
                pending_click = self.pending_click
                was_moved = self.drag_moved
                if was_moved:
                    self._on_drag_finished(hwnd)
                else:
                    self.drag = None
                    self.drag_cursor_start = None
                    self.drag_window_start = None
                    self.drag_moved = False
                    self.pending_click = None
                    self.native_drag = False
                    self.resizing = False
                    self.in_sizemove = False
                    user32.ReleaseCapture()
                    if msg == 0x0202 and pending_click:
                        self.activate_button(pending_click)
            return 0

        elif msg in (0x0232, 0x00A2):  # WM_EXITSIZEMOVE / WM_NCLBUTTONUP
            self._on_drag_finished(hwnd)
            return 0

        elif msg in (0x0205, 0x00A5):
            pt = POINT()
            user32.GetCursorPos(c.byref(pt))
            self.open_context_menu(pt.x, pt.y)
            return 0

        elif msg == 2:
            if self.popover and self.popover.hwnd:
                user32.DestroyWindow(self.popover.hwnd)
            if self.teamwork_popover and self.teamwork_popover.hwnd:
                user32.DestroyWindow(self.teamwork_popover.hwnd)
            for image in self.lock_images.values():
                gdiplus.GdipDisposeImage(image)
            self.lock_images.clear()
            user32.KillTimer(hwnd, 1)
            user32.KillTimer(hwnd, 2)
            user32.PostQuitMessage(0)
            return 0

        return user32.DefWindowProcW(hwnd, msg, wp, lp)

    def run(self):
        try:
            hdesk = user32.OpenInputDesktop(0, False, 0x01FF) or user32.OpenDesktopW("Default", 0, False, 0x01FF)
            if hdesk:
                user32.SetThreadDesktop(hdesk)
        except Exception:
            pass

        with LOG_PATH.open('a', encoding='utf-8') as f:
            f.write("run(): registering window class...\n")
            f.flush()

        self.cb = WNDPROC(self.proc)
        hinst = kernel32.GetModuleHandleW(None)

        user32.UnregisterClassW('AntigravityQuotaWidgetV10Pro', hinst)
        wc = WNDCLASS(11, self.cb, 0, 0, hinst, None, user32.LoadCursorW(None, 32512), None, None, 'AntigravityQuotaWidgetV10Pro')
        user32.RegisterClassW(c.byref(wc))

        with LOG_PATH.open('a', encoding='utf-8') as f:
            f.write(f"run(): calling CreateWindowExW (x={self.s['x']}, y={self.s['y']}, w={self.w}, h={self.h})...\n")
            f.flush()

        # Create independently first so an Electron owner in transition cannot
        # suppress the initial render. The periodic tracker attaches it once a
        # usable Antigravity window is confirmed.
        owner_info = None
        owner_hwnd = None
        if owner_info:
            owner_hwnd, cl, ct, cr, cb, _ = owner_info
            self.last_codex_hwnd = owner_hwnd
            self.last_codex_rect = (cl, ct, cr, cb)

        # Layered tool window with WS_EX_TOPMOST so widget stays reliably above Antigravity
        ex_style = 0x00080000 | 0x00000080 | 0x00000008
        hwnd = user32.CreateWindowExW(
            ex_style,
            'AntigravityQuotaWidgetV10Pro',
            'Antigravity Quota Widget V10 Pro Ultimate',
            0x80000000,  # WS_POPUP; pure borderless layered glass HUD
            self.s['x'], self.s['y'], self.w, self.h,
            None, None, hinst, None
        )
        if not hwnd:
            with LOG_PATH.open('a', encoding='utf-8') as f:
                f.write(f"run(): CreateWindowExW FAILED: {kernel32.GetLastError()}\n")
                f.flush()
            raise OSError(f'CreateWindowExW failed: {kernel32.GetLastError()}')

        with LOG_PATH.open('a', encoding='utf-8') as f:
            f.write(f"run(): CreateWindowExW SUCCEEDED, HWND={hwnd}\n")
            f.flush()

        self.hwnd = hwnd
        self.owner_hwnd = None
        self.is_visible = True
        user32.ShowWindow(hwnd, 5 if self.is_visible else 0)
        # Always float topmost (-1) so clicks never pass through or get swallowed by Electron IDE
        user32.SetWindowPos(hwnd, -1, self.s['x'], self.s['y'], self.w, self.h, 0x0040 | 0x0010)
        user32.UpdateWindow(hwnd)
        self.update_layered_render()

        with LOG_PATH.open('a', encoding='utf-8') as f:
            f.write("run(): entering GetMessageW message loop...\n")
            f.flush()

        m = MSG()
        while True:
            ret = user32.GetMessageW(c.byref(m), None, 0, 0)
            if ret <= 0:
                with LOG_PATH.open('a', encoding='utf-8') as f:
                    f.write(f"run(): GetMessageW returned {ret}, exiting loop.\n")
                    f.flush()
                break
            user32.TranslateMessage(c.byref(m))
            user32.DispatchMessageW(c.byref(m))

        with LOG_PATH.open('a', encoding='utf-8') as f:
            f.write("run(): GetMessageW loop EXITED.\n")
            f.flush()
