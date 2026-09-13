# -*- coding: utf-8 -*-
"""
Unified Win32 / GDI / GDI+ ctypes definitions for Cockpit Quota Widget V10 Pro.
Provides single-source-of-truth structures and function signatures to prevent
type collisions across modules.
"""

import ctypes as c
from ctypes import wintypes as w

kernel32 = c.WinDLL('kernel32', use_last_error=True)
user32 = c.WinDLL('user32', use_last_error=True)
gdi32 = c.WinDLL('gdi32', use_last_error=True)
comdlg32 = c.WinDLL('comdlg32', use_last_error=True)
gdiplus = c.WinDLL('gdiplus', use_last_error=True)

WNDPROC = c.WINFUNCTYPE(c.c_longlong, w.HWND, w.UINT, w.WPARAM, w.LPARAM)


class WNDCLASS(c.Structure):
    _fields_ = [
        ('style', w.UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', c.c_int),
        ('cbWndExtra', c.c_int),
        ('hInstance', w.HINSTANCE),
        ('hIcon', w.HANDLE),
        ('hCursor', w.HANDLE),
        ('hbrBackground', w.HBRUSH),
        ('lpszMenuName', w.LPCWSTR),
        ('lpszClassName', w.LPCWSTR),
    ]


class POINT(c.Structure):
    _fields_ = [('x', c.c_long), ('y', c.c_long)]


class MINMAXINFO(c.Structure):
    _fields_ = [
        ('ptReserved', POINT),
        ('ptMaxSize', POINT),
        ('ptMaxPosition', POINT),
        ('ptMinTrackSize', POINT),
        ('ptMaxTrackSize', POINT),
    ]


class SIZE(c.Structure):
    _fields_ = [('cx', c.c_long), ('cy', c.c_long)]


class MSG(c.Structure):
    _fields_ = [
        ('hwnd', w.HWND),
        ('message', w.UINT),
        ('wParam', w.WPARAM),
        ('lParam', w.LPARAM),
        ('time', w.DWORD),
        ('pt', POINT),
        ('lPrivate', w.DWORD),
    ]


class BLENDFUNCTION(c.Structure):
    _fields_ = [
        ('BlendOp', c.c_ubyte),
        ('BlendFlags', c.c_ubyte),
        ('SourceConstantAlpha', c.c_ubyte),
        ('AlphaFormat', c.c_ubyte),
    ]


class BITMAPINFOHEADER(c.Structure):
    _fields_ = [
        ('biSize', w.DWORD),
        ('biWidth', c.c_long),
        ('biHeight', c.c_long),
        ('biPlanes', w.WORD),
        ('biBitCount', w.WORD),
        ('biCompression', w.DWORD),
        ('biSizeImage', w.DWORD),
        ('biXPelsPerMeter', c.c_long),
        ('biYPelsPerMeter', c.c_long),
        ('biClrUsed', w.DWORD),
        ('biClrImportant', w.DWORD)
    ]


class BITMAPINFO(c.Structure):
    _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', w.DWORD * 3)]


class TOOLINFO(c.Structure):
    _fields_ = [
        ('cbSize', w.UINT),
        ('uFlags', w.UINT),
        ('hwnd', w.HWND),
        ('uId', w.HWND),
        ('rect', w.RECT),
        ('hinst', w.HINSTANCE),
        ('lpszText', w.LPCWSTR),
        ('lpReserved', c.c_void_p),
    ]


class CHOOSECOLOR(c.Structure):
    _fields_ = [
        ('lStructSize', w.DWORD),
        ('hwndOwner', w.HWND),
        ('hInstance', w.HWND),
        ('rgbResult', w.COLORREF),
        ('lpCustColors', c.POINTER(w.COLORREF)),
        ('Flags', w.DWORD),
        ('lCustData', w.LPARAM),
        ('lpfnHook', c.c_void_p),
        ('lpTemplateName', w.LPCWSTR),
    ]


class TRACKMOUSEEVENT(c.Structure):
    _fields_ = [
        ('cbSize', w.DWORD),
        ('dwFlags', w.DWORD),
        ('hwndTrack', c.c_void_p),
        ('dwHoverTime', w.DWORD),
    ]


class GdiplusStartupInput(c.Structure):
    _fields_ = [
        ('GdiplusVersion', w.UINT),
        ('DebugEventCallback', c.c_void_p),
        ('SuppressBackgroundThread', w.BOOL),
        ('SuppressExternalCodecs', w.BOOL),
    ]


# Function Signatures (64-bit Safe)
user32.TrackMouseEvent.argtypes = [c.POINTER(TRACKMOUSEEVENT)]
user32.TrackMouseEvent.restype = w.BOOL
kernel32.GetModuleHandleW.argtypes = [w.LPCWSTR]
kernel32.GetModuleHandleW.restype = c.c_void_p
kernel32.CreateMutexW.argtypes = [c.c_void_p, w.BOOL, w.LPCWSTR]
kernel32.CreateMutexW.restype = c.c_void_p

user32.DefWindowProcW.argtypes = [c.c_void_p, w.UINT, w.WPARAM, w.LPARAM]
user32.DefWindowProcW.restype = c.c_longlong
user32.RegisterClassW.argtypes = [c.POINTER(WNDCLASS)]
user32.RegisterClassW.restype = w.ATOM
user32.UnregisterClassW.argtypes = [w.LPCWSTR, c.c_void_p]
user32.UnregisterClassW.restype = w.BOOL

user32.CreateWindowExW.argtypes = [
    w.DWORD, w.LPCWSTR, w.LPCWSTR, w.DWORD,
    c.c_int, c.c_int, c.c_int, c.c_int,
    c.c_void_p, c.c_void_p, c.c_void_p, c.c_void_p
]
user32.CreateWindowExW.restype = c.c_void_p

user32.ShowWindow.argtypes = [c.c_void_p, c.c_int]
user32.ShowWindow.restype = w.BOOL
user32.UpdateWindow.argtypes = [c.c_void_p]
user32.UpdateWindow.restype = w.BOOL
user32.DestroyWindow.argtypes = [c.c_void_p]
user32.DestroyWindow.restype = w.BOOL
user32.SetWindowPos.argtypes = [c.c_void_p, c.c_void_p, c.c_int, c.c_int, c.c_int, c.c_int, w.UINT]
user32.SetWindowPos.restype = w.BOOL
user32.GetWindow.argtypes = [c.c_void_p, w.UINT]
user32.GetWindow.restype = c.c_void_p
user32.SetWindowLongPtrW.argtypes = [c.c_void_p, c.c_int, c.c_void_p]
user32.SetWindowLongPtrW.restype = c.c_longlong
user32.GetWindowRect.argtypes = [c.c_void_p, c.POINTER(w.RECT)]
user32.GetWindowRect.restype = w.BOOL
user32.GetCursorPos.argtypes = [c.POINTER(POINT)]
user32.GetCursorPos.restype = w.BOOL
user32.GetKeyState.argtypes = [c.c_int]
user32.GetKeyState.restype = c.c_short
user32.SetTimer.argtypes = [c.c_void_p, c.c_size_t, w.UINT, c.c_void_p]
user32.SetTimer.restype = c.c_size_t
user32.KillTimer.argtypes = [c.c_void_p, c.c_size_t]
user32.KillTimer.restype = w.BOOL
user32.SendMessageW.argtypes = [c.c_void_p, w.UINT, w.WPARAM, c.c_void_p]
user32.SendMessageW.restype = c.c_longlong
user32.PostQuitMessage.argtypes = [c.c_int]
user32.PostQuitMessage.restype = None
user32.LoadCursorW.argtypes = [c.c_void_p, c.c_void_p]
user32.LoadCursorW.restype = c.c_void_p
user32.GetDC.argtypes = [c.c_void_p]
user32.GetDC.restype = c.c_void_p
user32.ReleaseDC.argtypes = [c.c_void_p, c.c_void_p]
user32.ReleaseDC.restype = c.c_int
user32.GetSystemMetrics.argtypes = [c.c_int]
user32.GetSystemMetrics.restype = c.c_int
user32.IsWindow.argtypes = [c.c_void_p]
user32.IsWindow.restype = w.BOOL
user32.IsWindowVisible.argtypes = [c.c_void_p]
user32.IsWindowVisible.restype = w.BOOL
user32.IsIconic.argtypes = [c.c_void_p]
user32.IsIconic.restype = w.BOOL
user32.FindWindowW.argtypes = [w.LPCWSTR, w.LPCWSTR]
user32.FindWindowW.restype = c.c_void_p
user32.SetForegroundWindow.argtypes = [c.c_void_p]
user32.SetForegroundWindow.restype = w.BOOL
user32.GetForegroundWindow.argtypes = []
user32.GetForegroundWindow.restype = c.c_void_p
user32.GetWindowThreadProcessId.argtypes = [c.c_void_p, c.POINTER(w.DWORD)]
user32.GetWindowThreadProcessId.restype = w.DWORD
user32.AttachThreadInput.argtypes = [w.DWORD, w.DWORD, w.BOOL]
user32.AttachThreadInput.restype = w.BOOL
user32.BringWindowToTop.argtypes = [c.c_void_p]
user32.BringWindowToTop.restype = w.BOOL
user32.SetFocus.argtypes = [c.c_void_p]
user32.SetFocus.restype = c.c_void_p
user32.SendInput.argtypes = [w.UINT, c.c_void_p, c.c_int]
user32.SendInput.restype = w.UINT
kernel32.GetCurrentThreadId.argtypes = []
kernel32.GetCurrentThreadId.restype = w.DWORD

user32.OpenDesktopW.argtypes = [w.LPCWSTR, w.DWORD, w.BOOL, w.DWORD]
user32.OpenDesktopW.restype = c.c_void_p
user32.OpenInputDesktop.argtypes = [w.DWORD, w.BOOL, w.DWORD]
user32.OpenInputDesktop.restype = c.c_void_p
user32.SetThreadDesktop.argtypes = [c.c_void_p]
user32.SetThreadDesktop.restype = w.BOOL
user32.CloseDesktop.argtypes = [c.c_void_p]
user32.CloseDesktop.restype = w.BOOL

user32.GetMessageW.argtypes = [c.POINTER(MSG), c.c_void_p, w.UINT, w.UINT]
user32.GetMessageW.restype = c.c_int
user32.TranslateMessage.argtypes = [c.POINTER(MSG)]
user32.TranslateMessage.restype = w.BOOL
user32.DispatchMessageW.argtypes = [c.POINTER(MSG)]
user32.DispatchMessageW.restype = c.c_longlong
user32.PeekMessageW.argtypes = [c.POINTER(MSG), c.c_void_p, w.UINT, w.UINT, w.UINT]
user32.PeekMessageW.restype = w.BOOL

user32.UpdateLayeredWindow.argtypes = [
    c.c_void_p, c.c_void_p, c.POINTER(POINT), c.POINTER(SIZE),
    c.c_void_p, c.POINTER(POINT), w.COLORREF, c.POINTER(BLENDFUNCTION), w.DWORD
]
user32.UpdateLayeredWindow.restype = w.BOOL

# GDI Signatures
gdi32.CreateCompatibleDC.argtypes = [c.c_void_p]
gdi32.CreateCompatibleDC.restype = c.c_void_p
gdi32.DeleteDC.argtypes = [c.c_void_p]
gdi32.DeleteDC.restype = w.BOOL
gdi32.SelectObject.argtypes = [c.c_void_p, c.c_void_p]
gdi32.SelectObject.restype = c.c_void_p
gdi32.DeleteObject.argtypes = [c.c_void_p]
gdi32.DeleteObject.restype = w.BOOL
gdi32.CreateDIBSection.argtypes = [c.c_void_p, c.c_void_p, w.UINT, c.POINTER(c.c_void_p), c.c_void_p, w.DWORD]
gdi32.CreateDIBSection.restype = c.c_void_p

gdiplus.GdipCreateFromHDC.argtypes = [c.c_void_p, c.POINTER(c.c_void_p)]
gdiplus.GdipCreateFromHDC.restype = c.c_int
gdiplus.GdipDeleteGraphics.argtypes = [c.c_void_p]
gdiplus.GdipDeleteGraphics.restype = c.c_int
gdiplus.GdipLoadImageFromFile.argtypes = [w.LPCWSTR, c.POINTER(c.c_void_p)]
gdiplus.GdipLoadImageFromFile.restype = c.c_int
gdiplus.GdipDisposeImage.argtypes = [c.c_void_p]
gdiplus.GdipDisposeImage.restype = c.c_int
gdiplus.GdipDrawImageRectI.argtypes = [c.c_void_p, c.c_void_p, c.c_int, c.c_int, c.c_int, c.c_int]
gdiplus.GdipDrawImageRectI.restype = c.c_int
gdiplus.GdipGraphicsClear.argtypes = [c.c_void_p, w.DWORD]
gdiplus.GdipGraphicsClear.restype = c.c_int
gdiplus.GdipSetSmoothingMode.argtypes = [c.c_void_p, c.c_int]
gdiplus.GdipSetSmoothingMode.restype = c.c_int
gdiplus.GdipSetTextRenderingHint.argtypes = [c.c_void_p, c.c_int]
gdiplus.GdipSetTextRenderingHint.restype = c.c_int
gdiplus.GdipSetPixelOffsetMode.argtypes = [c.c_void_p, c.c_int]
gdiplus.GdipSetPixelOffsetMode.restype = c.c_int

gdiplus.GdipCreateSolidFill.argtypes = [w.DWORD, c.POINTER(c.c_void_p)]
gdiplus.GdipCreateSolidFill.restype = c.c_int
gdiplus.GdipDeleteBrush.argtypes = [c.c_void_p]
gdiplus.GdipDeleteBrush.restype = c.c_int

gdiplus.GdipCreatePen1.argtypes = [w.DWORD, c.c_float, c.c_int, c.POINTER(c.c_void_p)]
gdiplus.GdipCreatePen1.restype = c.c_int
gdiplus.GdipDeletePen.argtypes = [c.c_void_p]
gdiplus.GdipDeletePen.restype = c.c_int
gdiplus.GdipSetPenDashStyle.argtypes = [c.c_void_p, c.c_int]
gdiplus.GdipSetPenDashStyle.restype = c.c_int

gdiplus.GdipCreatePath.argtypes = [c.c_int, c.POINTER(c.c_void_p)]
gdiplus.GdipCreatePath.restype = c.c_int
gdiplus.GdipDeletePath.argtypes = [c.c_void_p]
gdiplus.GdipDeletePath.restype = c.c_int
gdiplus.GdipResetPath.argtypes = [c.c_void_p]
gdiplus.GdipResetPath.restype = c.c_int
gdiplus.GdipAddPathArc.argtypes = [c.c_void_p, c.c_float, c.c_float, c.c_float, c.c_float, c.c_float, c.c_float]
gdiplus.GdipAddPathArc.restype = c.c_int
gdiplus.GdipClosePathFigure.argtypes = [c.c_void_p]
gdiplus.GdipClosePathFigure.restype = c.c_int

gdiplus.GdipDrawPath.argtypes = [c.c_void_p, c.c_void_p, c.c_void_p]
gdiplus.GdipDrawPath.restype = c.c_int
gdiplus.GdipFillPath.argtypes = [c.c_void_p, c.c_void_p, c.c_void_p]
gdiplus.GdipFillPath.restype = c.c_int
gdiplus.GdipDrawLine.argtypes = [c.c_void_p, c.c_void_p, c.c_float, c.c_float, c.c_float, c.c_float]
gdiplus.GdipDrawLine.restype = c.c_int
gdiplus.GdipFillEllipse.argtypes = [c.c_void_p, c.c_void_p, c.c_float, c.c_float, c.c_float, c.c_float]
gdiplus.GdipFillEllipse.restype = c.c_int
gdiplus.GdipDrawArc.argtypes = [c.c_void_p, c.c_void_p, c.c_float, c.c_float, c.c_float, c.c_float, c.c_float, c.c_float]
gdiplus.GdipDrawArc.restype = c.c_int

gdiplus.GdipCreateFontFamilyFromName.argtypes = [w.LPCWSTR, c.c_void_p, c.POINTER(c.c_void_p)]
gdiplus.GdipCreateFontFamilyFromName.restype = c.c_int
gdiplus.GdipDeleteFontFamily.argtypes = [c.c_void_p]
gdiplus.GdipDeleteFontFamily.restype = c.c_int
gdiplus.GdipCreateFont.argtypes = [c.c_void_p, c.c_float, c.c_int, c.c_int, c.POINTER(c.c_void_p)]
gdiplus.GdipCreateFont.restype = c.c_int
gdiplus.GdipDeleteFont.argtypes = [c.c_void_p]
gdiplus.GdipDeleteFont.restype = c.c_int

gdiplus.GdipCreateStringFormat.argtypes = [c.c_int, w.LANGID, c.POINTER(c.c_void_p)]
gdiplus.GdipCreateStringFormat.restype = c.c_int
gdiplus.GdipDeleteStringFormat.argtypes = [c.c_void_p]
gdiplus.GdipDeleteStringFormat.restype = c.c_int
gdiplus.GdipSetStringFormatAlign.argtypes = [c.c_void_p, c.c_int]
gdiplus.GdipSetStringFormatAlign.restype = c.c_int
gdiplus.GdipSetStringFormatLineAlign.argtypes = [c.c_void_p, c.c_int]
gdiplus.GdipSetStringFormatLineAlign.restype = c.c_int
gdiplus.GdipDrawString.argtypes = [
    c.c_void_p, w.LPCWSTR, c.c_int, c.c_void_p,
    c.POINTER(c.c_float), c.c_void_p, c.c_void_p
]
gdiplus.GdipDrawString.restype = c.c_int

# Startup GDI+
_gp_token = c.c_ulong()
_gp_input = GdiplusStartupInput(1, None, False, False)
gdiplus.GdiplusStartup(c.byref(_gp_token), c.byref(_gp_input), None)
