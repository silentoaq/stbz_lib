# src/stbz_lib/_win32.py
"""
Windows API 定義與結構
"""
import ctypes
from ctypes import wintypes

# ── 32/64 位元指標相容性 ─────────────────────────────
PTR = ctypes.sizeof(ctypes.c_void_p)
ULONG_PTR = ctypes.c_ulonglong if PTR == 8 else ctypes.c_ulong
LONG_PTR = ctypes.c_longlong if PTR == 8 else ctypes.c_long
WPARAM = ULONG_PTR
LPARAM = LONG_PTR
LRESULT = LONG_PTR
HHOOK = ctypes.c_void_p

# ── Hook 相關常數 ────────────────────────────────────
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14

# ── 訊息常數 ─────────────────────────────────────────
WM_QUIT = 0x0012
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_XBUTTONDOWN = 0x020B
WM_XBUTTONUP = 0x020C

# ── 滑鼠按鈕常數 ─────────────────────────────────────
XBUTTON1 = 0x0001
XBUTTON2 = 0x0002

# ── 輸入相關常數 ─────────────────────────────────────
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# 鍵盤事件標誌
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

# 滑鼠事件標誌
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x1000
MOUSEEVENTF_ABSOLUTE = 0x8000

# Hook 標誌
LLKHF_INJECTED = 0x00000010
LLMHF_INJECTED = 0x00000001

# MapVirtualKey 常數
MAPVK_VK_TO_VSC = 0

# ── 共用結構定義 ─────────────────────────────────────
class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG)
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", wintypes.DWORD),
        ("pt", POINT)
    ]


LPMSG = ctypes.POINTER(MSG)


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]


class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]


# ── 輸入結構定義 ─────────────────────────────────────
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", INPUT_UNION)
    ]


# ── DLL 載入 ─────────────────────────────────────────
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

# ── 回調函數類型定義 ─────────────────────────────────
LowLevelKeyboardProc = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, WPARAM, LPARAM)
LowLevelMouseProc = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, WPARAM, LPARAM)

# ── API 函數定義 ─────────────────────────────────────
# SetWindowsHookEx
user32.SetWindowsHookExW.restype = HHOOK
user32.SetWindowsHookExW.argtypes = (
    ctypes.c_int,
    ctypes.c_void_p,  # 使用 c_void_p 以相容不同的回調類型
    wintypes.HMODULE,
    wintypes.DWORD
)

# CallNextHookEx
user32.CallNextHookEx.restype = LRESULT
user32.CallNextHookEx.argtypes = (HHOOK, ctypes.c_int, WPARAM, LPARAM)

# UnhookWindowsHookEx
user32.UnhookWindowsHookEx.restype = wintypes.BOOL
user32.UnhookWindowsHookEx.argtypes = (HHOOK,)

# GetMessage
user32.GetMessageW.restype = wintypes.BOOL
user32.GetMessageW.argtypes = (LPMSG, wintypes.HWND, wintypes.UINT, wintypes.UINT)

# TranslateMessage
user32.TranslateMessage.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = (LPMSG,)

# DispatchMessage
user32.DispatchMessageW.restype = LRESULT
user32.DispatchMessageW.argtypes = (LPMSG,)

# PostThreadMessage
user32.PostThreadMessageW.restype = wintypes.BOOL
user32.PostThreadMessageW.argtypes = (wintypes.DWORD, wintypes.UINT, WPARAM, LPARAM)

# SendInput
user32.SendInput.restype = wintypes.UINT
user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)

# MapVirtualKey
user32.MapVirtualKeyW.restype = wintypes.UINT
user32.MapVirtualKeyW.argtypes = (wintypes.UINT, wintypes.UINT)

# GetSystemMetrics
user32.GetSystemMetrics.restype = ctypes.c_int
user32.GetSystemMetrics.argtypes = (ctypes.c_int,)

# GetCursorPos
user32.GetCursorPos.restype = wintypes.BOOL
user32.GetCursorPos.argtypes = (ctypes.POINTER(POINT),)

# SetCursorPos
user32.SetCursorPos.restype = wintypes.BOOL
user32.SetCursorPos.argtypes = (ctypes.c_int, ctypes.c_int)

# GetModuleHandle
kernel32.GetModuleHandleW.restype = wintypes.HMODULE
kernel32.GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)

# GetCurrentThreadId
kernel32.GetCurrentThreadId.restype = wintypes.DWORD
kernel32.GetCurrentThreadId.argtypes = ()

# ── 系統指標常數 ─────────────────────────────────────
SM_CXSCREEN = 0  # 螢幕寬度
SM_CYSCREEN = 1  # 螢幕高度