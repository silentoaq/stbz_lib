# src/stbz_lib/_kb.py
import ctypes
import threading
import time

from ._core._hook import start_hook
from ._core._win32 import *

_kb_block_set = set()
_kb_lock = threading.Lock()
_scancode_cache = {}
_pressed_keys = set()
_held_keys = set()
_hook_initialized = False


def _global_keyboard_callback(nCode, wParam, lParam):
    if nCode >= 0 and (wParam == WM_KEYDOWN or wParam == WM_KEYUP):
        info = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk = info.vkCode
        is_injected = (info.flags & LLKHF_INJECTED) != 0

        if not is_injected:
            with _kb_lock:
                if vk in _held_keys:
                    return 1
                if vk in _kb_block_set:
                    return 1

    return user32.CallNextHookEx(None, nCode, wParam, lParam)


_keyboard_callback = LowLevelKeyboardProc(_global_keyboard_callback)


def _ensure_hook_started():
    global _hook_initialized
    if not _hook_initialized:
        start_hook(keyboard_callback=_keyboard_callback)
        _hook_initialized = True


def _get_scancode(vk):
    if vk not in _scancode_cache:
        _scancode_cache[vk] = user32.MapVirtualKeyW(vk, MAPVK_VK_TO_VSC)
    return _scancode_cache[vk]


def _send_kb_event(vk, is_keyup=False, use_scancode=True):
    inp = INPUT()
    inp.type = INPUT_KEYBOARD

    if use_scancode:
        scancode = _get_scancode(vk)
        inp.u.ki.wVk = 0
        inp.u.ki.wScan = scancode
        inp.u.ki.dwFlags = KEYEVENTF_SCANCODE
    else:
        inp.u.ki.wVk = vk
        inp.u.ki.wScan = _get_scancode(vk)
        inp.u.ki.dwFlags = 0

    if is_keyup:
        inp.u.ki.dwFlags |= KEYEVENTF_KEYUP

    inp.u.ki.time = 0
    inp.u.ki.dwExtraInfo = 0

    result = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())


def _keydown(vk):
    _send_kb_event(vk, is_keyup=False)
    _pressed_keys.add(vk)


def _keyup(vk):
    _send_kb_event(vk, is_keyup=True)
    _pressed_keys.discard(vk)


def _release_all_keys():
    keys_to_release = list(_pressed_keys)
    for vk in keys_to_release:
        _send_kb_event(vk, is_keyup=True)
    _pressed_keys.clear()
    _held_keys.clear()


def kb_block(keys=None):
    _ensure_hook_started()

    with _kb_lock:
        if keys is None:
            _kb_block_set.update(range(0x08, 0xFF))
        else:
            _kb_block_set.update(keys)


def kb_unblock(keys=None):
    with _kb_lock:
        if keys is None:
            _kb_block_set.clear()
        else:
            for key in keys:
                _kb_block_set.discard(key)


def kb_tap(key, count=1, interval_ms=50):
    for i in range(count):
        if i > 0:
            time.sleep(interval_ms / 1000.0)
        _keydown(key)
        time.sleep(0.01)
        _keyup(key)


def kb_hold(key, duration_ms=100, count=1, interval_ms=50):
    _ensure_hook_started()

    for i in range(count):
        if i > 0:
            time.sleep(interval_ms / 1000.0)

        with _kb_lock:
            _held_keys.add(key)

        try:
            _keydown(key)
            time.sleep(duration_ms / 1000.0)
            _keyup(key)
        finally:
            with _kb_lock:
                _held_keys.discard(key)


def get_blocked_keys():
    with _kb_lock:
        return list(_kb_block_set)


def is_key_blocked(key):
    with _kb_lock:
        return key in _kb_block_set


def _cleanup():
    _release_all_keys()
    kb_unblock()
    global _hook_initialized
    _hook_initialized = False


import atexit

atexit.register(_cleanup)
