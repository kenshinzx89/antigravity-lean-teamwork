# -*- coding: utf-8 -*-
"""
Window Tracker for Cockpit Quota Widget V9.0
Identifies and tracks the Codex Desktop window position and state in real-time.
"""

import os
import ctypes as c
from ctypes import wintypes as w

user32 = c.windll.user32
kernel32 = c.windll.kernel32

# 64-bit Win32 Argtypes & Restypes
user32.IsWindow.argtypes = [w.HWND]
user32.IsWindow.restype = w.BOOL
user32.GetForegroundWindow.argtypes = []
user32.GetForegroundWindow.restype = w.HWND
user32.IsWindowVisible.argtypes = [w.HWND]
user32.IsWindowVisible.restype = w.BOOL
user32.IsIconic.argtypes = [w.HWND]
user32.IsIconic.restype = w.BOOL
user32.GetWindowRect.argtypes = [w.HWND, c.POINTER(w.RECT)]
user32.GetWindowRect.restype = w.BOOL
user32.GetWindowThreadProcessId.argtypes = [w.HWND, c.POINTER(w.DWORD)]
user32.GetWindowThreadProcessId.restype = w.DWORD
user32.GetCursorPos.argtypes = [c.c_void_p]
user32.GetCursorPos.restype = w.BOOL
user32.GetSystemMetrics.argtypes = [c.c_int]
user32.GetSystemMetrics.restype = c.c_int

kernel32.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
kernel32.OpenProcess.restype = w.HANDLE
kernel32.CloseHandle.argtypes = [w.HANDLE]
kernel32.CloseHandle.restype = w.BOOL
kernel32.QueryFullProcessImageNameW.argtypes = [w.HANDLE, w.DWORD, w.LPWSTR, c.POINTER(w.DWORD)]
kernel32.QueryFullProcessImageNameW.restype = w.BOOL


def get_process_image_path(pid):
    """Gets the executable path for a process ID."""
    h = kernel32.OpenProcess(0x1000, False, pid)
    if not h:
        return ""
    buf = c.create_unicode_buffer(1024)
    size = w.DWORD(1024)
    res = kernel32.QueryFullProcessImageNameW(h, 0, buf, c.byref(size))
    kernel32.CloseHandle(h)
    if res:
        return os.path.normcase(buf.value)
    return ""


def is_codex_desktop_image(image_path):
    """Compatibility name: accepts both supported Antigravity desktop apps.

    Cockpit's Antigravity and Antigravity IDE are installed in different
    directories and use different executable names.  Match only the basename
    so the tracker remains installation-path independent.
    """
    path = (image_path or "").replace('/', '\\').lower()
    return os.path.basename(path) in {'antigravity.exe', 'antigravity ide.exe'}


def find_codex_window(include_minimized=False, preferred_hwnd=None, strict_preferred=False):
    """Enumerates visible windows to find the main Codex Desktop window rect."""
    codex_hwnds = []
    minimized_codex_hwnds = []
    foreground = user32.GetForegroundWindow()
    foreground_pid = w.DWORD()
    if foreground:
        user32.GetWindowThreadProcessId(foreground, c.byref(foreground_pid))
    WNDENUMPROC = c.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)

    def enum_wnd(hwnd, lparam):
        if user32.IsWindowVisible(hwnd) or user32.IsIconic(hwnd):
            pid = w.DWORD()
            user32.GetWindowThreadProcessId(hwnd, c.byref(pid))
            image_path = get_process_image_path(pid.value)

            r = w.RECT()
            user32.GetWindowRect(hwnd, c.byref(r))
            w_win = r.right - r.left
            h_win = r.bottom - r.top

            is_minimized = bool(user32.IsIconic(hwnd)) or (r.left <= -10000 and r.top <= -10000)
            is_codex = is_codex_desktop_image(image_path)

            if is_codex and (is_minimized or (w_win > 300 and h_win > 250)):
                title_buf = c.create_unicode_buffer(256)
                user32.GetWindowTextW(hwnd, title_buf, 256)
                title_str = title_buf.value.strip()
                # Score: prefer titled main window and larger area
                area = w_win * h_win
                score = area + (10000000 if title_str and title_str != 'Default IME' and title_str != 'MSCTFIME UI' else 0)
                target = minimized_codex_hwnds if is_minimized else codex_hwnds
                target.append((hwnd, r.left, r.top, r.right, r.bottom, True, pid.value, score))
        return True

    cb = WNDENUMPROC(enum_wnd)
    hdesk = user32.OpenInputDesktop(0, False, 0x01FF) or user32.OpenDesktopW("Default", 0, False, 0x01FF)
    if hdesk:
        user32.EnumDesktopWindows(hdesk, cb, 0)
        user32.CloseDesktop(hdesk)
    if not codex_hwnds and not minimized_codex_hwnds:
        user32.EnumWindows(cb, 0)

    # Sort each list by score descending (largest, titled main window first)
    codex_hwnds.sort(key=lambda x: x[7], reverse=True)
    minimized_codex_hwnds.sort(key=lambda x: x[7], reverse=True)

    # Once an overlay is owned by a specific Codex HWND, finding a different
    # Codex window is not a valid fallback.  During minimize/restore Windows
    # can briefly omit the owner from EnumWindows; choosing another candidate
    # made the widget reappear detached from the window the user minimized.
    if preferred_hwnd:
        for candidates in (codex_hwnds, minimized_codex_hwnds):
            for item in candidates:
                if item[0] == preferred_hwnd:
                    return item[:6]
        if strict_preferred:
            return None

    def choose(candidates):
        if not candidates:
            return None
        # Foreground match if it is one of the candidates
        for item in candidates:
            if foreground_pid.value and item[6] == foreground_pid.value and item[7] > 10000000:
                return item[:6]
        return candidates[0][:6]

    if codex_hwnds:
        return choose(codex_hwnds)
    if include_minimized and minimized_codex_hwnds:
        return choose(minimized_codex_hwnds)
    return None
