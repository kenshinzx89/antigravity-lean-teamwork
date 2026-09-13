"""Small, dependency-free tracker for the installed Antigravity IDE window."""

import ctypes as c
import os
from ctypes import wintypes as w

user32 = c.windll.user32
kernel32 = c.windll.kernel32

user32.GetWindowThreadProcessId.argtypes = [w.HWND, c.POINTER(w.DWORD)]
user32.GetWindowThreadProcessId.restype = w.DWORD
user32.GetWindowRect.argtypes = [w.HWND, c.POINTER(w.RECT)]
user32.GetWindowRect.restype = w.BOOL
user32.IsWindowVisible.argtypes = [w.HWND]
user32.IsWindowVisible.restype = w.BOOL
user32.IsIconic.argtypes = [w.HWND]
user32.IsIconic.restype = w.BOOL
kernel32.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
kernel32.OpenProcess.restype = w.HANDLE
kernel32.QueryFullProcessImageNameW.argtypes = [w.HANDLE, w.DWORD, w.LPWSTR, c.POINTER(w.DWORD)]
kernel32.QueryFullProcessImageNameW.restype = w.BOOL


def _image_path(pid: int) -> str:
    handle = kernel32.OpenProcess(0x1000, False, pid)
    if not handle:
        return ""
    try:
        buffer = c.create_unicode_buffer(1024)
        size = w.DWORD(len(buffer))
        return buffer.value.lower() if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, c.byref(size)) else ""
    finally:
        kernel32.CloseHandle(handle)


def find_window(preferred_hwnd=None):
    """Return (hwnd, left, top, right, bottom, minimized), or None.

    Matching the executable name avoids binding to a browser tab or another
    Electron program that merely happens to have Antigravity in its title.
    """
    visible, minimized = [], []
    callback_type = c.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)

    def visit(hwnd, _):
        if not (user32.IsWindowVisible(hwnd) or user32.IsIconic(hwnd)):
            return True
        pid = w.DWORD()
        user32.GetWindowThreadProcessId(hwnd, c.byref(pid))
        if os.path.basename(_image_path(pid.value)) != "antigravity ide.exe":
            return True
        rect = w.RECT()
        if not user32.GetWindowRect(hwnd, c.byref(rect)):
            return True
        item = (hwnd, rect.left, rect.top, rect.right, rect.bottom, bool(user32.IsIconic(hwnd)))
        (minimized if item[-1] else visible).append(item)
        return True

    user32.EnumWindows(callback_type(visit), 0)
    for collection in (visible, minimized):
        for item in collection:
            if preferred_hwnd and item[0] == preferred_hwnd:
                return item
    return visible[0] if visible else (minimized[0] if minimized else None)
