# -*- coding: utf-8 -*-
"""
Main Entry Point for Cockpit Quota Widget V10 Pro Ultimate
High-Performance, Multi-Theme, Liquid Glassmorphism Monitor for Antigravity & Cockpit Tools.
"""

import sys
import os
import traceback

# Fix pythonw.exe stdout/stderr NoneType crash safely without file locking
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

LOG_PATH = os.path.join(SCRIPT_DIR, 'widget_crash.log')


def log_error(msg):
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(f"{msg}\n")
    except Exception:
        pass


def main():
    try:
        import ctypes
        # Window size, rendered pixels and WM_NCHITTEST coordinates must use
        # one DPI space.  The former best-effort call ignored a False return,
        # leaving some launches system-DPI virtualised: visual cards were wide
        # but their hit areas/resizing behaved as if the bar were much smaller.
        try:
            user32 = ctypes.windll.user32
            user32.SetProcessDpiAwarenessContext.argtypes = [ctypes.c_void_p]
            user32.SetProcessDpiAwarenessContext.restype = ctypes.c_bool
            user32.SetThreadDpiAwarenessContext.argtypes = [ctypes.c_void_p]
            user32.SetThreadDpiAwarenessContext.restype = ctypes.c_void_p
            per_monitor_v2 = ctypes.c_void_p(-4)
            if not user32.SetProcessDpiAwarenessContext(per_monitor_v2):
                # The process may already have an inherited mode; a thread
                # override still keeps this native window and its messages in
                # physical pixels.
                user32.SetThreadDpiAwarenessContext(per_monitor_v2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass
        kernel32 = ctypes.windll.kernel32
        # New runtime generation: stale pre-fix Python processes sometimes
        # retained the former mutex after their native HWND vanished.  Keeping
        # a versioned mutex lets this corrected build recover without killing
        # an unrelated ``pythonw main.py`` process.
        mutex = kernel32.CreateMutexW(None, True, "Local\\AntigravityQuotaWidgetV10ProMutexV2")
        if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            return
        # Ensure the widget is bound to the interactive user desktop ("Default").
        # When launched from background services, secondary desktops or tools,
        # GetThreadDesktop may point to an isolated desktop where the user cannot see it.
        try:
            hdesk = user32.OpenInputDesktop(0, False, 0x01FF) or user32.OpenDesktopW("Default", 0, False, 0x01FF)
            if hdesk:
                user32.SetThreadDesktop(hdesk)
        except Exception:
            pass

        from core.overlay_window import CockpitOverlayApp
        app = CockpitOverlayApp()
        app.run()
    except Exception:
        log_error(f"FATAL ERROR IN MAIN: {traceback.format_exc()}")


if __name__ == '__main__':
    main()
