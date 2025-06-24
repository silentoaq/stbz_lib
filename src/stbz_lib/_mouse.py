# src/stbz_lib/_mouse.py
import ctypes
import threading
import time

from ._core._hook import start_hook
from ._core._win32 import *

MOUSE_LEFT = 0x01
MOUSE_RIGHT = 0x02
MOUSE_MIDDLE = 0x03
MOUSE_X1 = 0x04
MOUSE_X2 = 0x05
MOUSE_MOVE = 0x06

MOVE_UP = 0x10
MOVE_DOWN = 0x11
MOVE_LEFT = 0x12
MOVE_RIGHT = 0x13

_mouse_block_set = set()
_mouse_lock = threading.Lock()
_pressed_buttons = set()
_held_buttons = set()
_hook_initialized = False


def _global_mouse_callback(nCode, wParam, lParam):
    if nCode >= 0:
        info = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
        is_injected = (info.flags & LLMHF_INJECTED) != 0

        if not is_injected:
            with _mouse_lock:
                if wParam in (WM_LBUTTONDOWN, WM_LBUTTONUP) and MOUSE_LEFT in _held_buttons:
                    return 1
                elif wParam in (WM_RBUTTONDOWN, WM_RBUTTONUP) and MOUSE_RIGHT in _held_buttons:
                    return 1
                elif wParam in (WM_MBUTTONDOWN, WM_MBUTTONUP) and MOUSE_MIDDLE in _held_buttons:
                    return 1
                elif wParam in (WM_XBUTTONDOWN, WM_XBUTTONUP):
                    button = (info.mouseData >> 16) & 0xFFFF
                    if button == XBUTTON1 and MOUSE_X1 in _held_buttons:
                        return 1
                    elif button == XBUTTON2 and MOUSE_X2 in _held_buttons:
                        return 1

                if wParam == WM_MOUSEMOVE and MOUSE_MOVE in _mouse_block_set:
                    return 1
                elif wParam in (WM_LBUTTONDOWN, WM_LBUTTONUP) and MOUSE_LEFT in _mouse_block_set:
                    return 1
                elif wParam in (WM_RBUTTONDOWN, WM_RBUTTONUP) and MOUSE_RIGHT in _mouse_block_set:
                    return 1
                elif wParam in (WM_MBUTTONDOWN, WM_MBUTTONUP) and MOUSE_MIDDLE in _mouse_block_set:
                    return 1
                elif wParam in (WM_XBUTTONDOWN, WM_XBUTTONUP):
                    button = (info.mouseData >> 16) & 0xFFFF
                    if button == XBUTTON1 and MOUSE_X1 in _mouse_block_set:
                        return 1
                    elif button == XBUTTON2 and MOUSE_X2 in _mouse_block_set:
                        return 1

    return user32.CallNextHookEx(None, nCode, wParam, lParam)


_mouse_callback = LowLevelMouseProc(_global_mouse_callback)


def _ensure_hook_started():
    global _hook_initialized
    if not _hook_initialized:
        start_hook(mouse_callback=_mouse_callback)
        _hook_initialized = True


def _send_mouse_event(dx=0, dy=0, dwData=0, dwFlags=0):
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.u.mi.dx = dx
    inp.u.mi.dy = dy
    inp.u.mi.mouseData = dwData
    inp.u.mi.dwFlags = dwFlags
    inp.u.mi.time = 0
    inp.u.mi.dwExtraInfo = 0

    result = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())


def _mousedown(button):
    if button == MOUSE_LEFT:
        _send_mouse_event(dwFlags=MOUSEEVENTF_LEFTDOWN)
    elif button == MOUSE_RIGHT:
        _send_mouse_event(dwFlags=MOUSEEVENTF_RIGHTDOWN)
    elif button == MOUSE_MIDDLE:
        _send_mouse_event(dwFlags=MOUSEEVENTF_MIDDLEDOWN)
    elif button == MOUSE_X1:
        _send_mouse_event(dwData=XBUTTON1, dwFlags=MOUSEEVENTF_XDOWN)
    elif button == MOUSE_X2:
        _send_mouse_event(dwData=XBUTTON2, dwFlags=MOUSEEVENTF_XDOWN)
    _pressed_buttons.add(button)


def _mouseup(button):
    if button == MOUSE_LEFT:
        _send_mouse_event(dwFlags=MOUSEEVENTF_LEFTUP)
    elif button == MOUSE_RIGHT:
        _send_mouse_event(dwFlags=MOUSEEVENTF_RIGHTUP)
    elif button == MOUSE_MIDDLE:
        _send_mouse_event(dwFlags=MOUSEEVENTF_MIDDLEUP)
    elif button == MOUSE_X1:
        _send_mouse_event(dwData=XBUTTON1, dwFlags=MOUSEEVENTF_XUP)
    elif button == MOUSE_X2:
        _send_mouse_event(dwData=XBUTTON2, dwFlags=MOUSEEVENTF_XUP)
    _pressed_buttons.discard(button)


def _release_all_buttons():
    buttons_to_release = list(_pressed_buttons)
    for button in buttons_to_release:
        _mouseup(button)
    _pressed_buttons.clear()
    _held_buttons.clear()


def mouse_block(button_list=None):
    _ensure_hook_started()

    with _mouse_lock:
        if button_list is None:
            _mouse_block_set.update([MOUSE_LEFT, MOUSE_RIGHT, MOUSE_MIDDLE, MOUSE_X1, MOUSE_X2, MOUSE_MOVE])
        else:
            _mouse_block_set.update(button_list)


def mouse_unblock(button_list=None):
    with _mouse_lock:
        if button_list is None:
            _mouse_block_set.clear()
        else:
            for button in button_list:
                _mouse_block_set.discard(button)


def mouse_tap(button, count=1, interval_ms=50):
    for i in range(count):
        if i > 0:
            time.sleep(interval_ms / 1000.0)
        _mousedown(button)
        time.sleep(0.01)
        _mouseup(button)


def mouse_hold(button, duration_ms=100, count=1, interval_ms=50):
    _ensure_hook_started()

    for i in range(count):
        if i > 0:
            time.sleep(interval_ms / 1000.0)

        with _mouse_lock:
            _held_buttons.add(button)

        try:
            _mousedown(button)
            time.sleep(duration_ms / 1000.0)
            _mouseup(button)
        finally:
            with _mouse_lock:
                _held_buttons.discard(button)


def mouse_pos(x, y):
    result = user32.SetCursorPos(x, y)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())


def mouse_move(direction, duration_ms=1000, speed=5):
    screen_width = user32.GetSystemMetrics(SM_CXSCREEN)
    screen_height = user32.GetSystemMetrics(SM_CYSCREEN)

    cursor_pos = POINT()
    user32.GetCursorPos(ctypes.byref(cursor_pos))

    if direction == MOVE_UP:
        user32.SetCursorPos(cursor_pos.x, 0)
        dx, dy = 0, -speed
    elif direction == MOVE_DOWN:
        user32.SetCursorPos(cursor_pos.x, screen_height - 1)
        dx, dy = 0, speed
    elif direction == MOVE_LEFT:
        user32.SetCursorPos(0, cursor_pos.y)
        dx, dy = -speed, 0
    elif direction == MOVE_RIGHT:
        user32.SetCursorPos(screen_width - 1, cursor_pos.y)
        dx, dy = speed, 0
    else:
        raise ValueError(f"Invalid direction: {direction}")

    start_time = time.time()
    while (time.time() - start_time) * 1000 < duration_ms:
        _send_mouse_event(dx=dx, dy=dy, dwFlags=MOUSEEVENTF_MOVE)
        time.sleep(0.01)


def get_blocked_buttons():
    with _mouse_lock:
        return list(_mouse_block_set)


def is_button_blocked(button):
    with _mouse_lock:
        return button in _mouse_block_set


def get_mouse_pos():
    pos = POINT()
    user32.GetCursorPos(ctypes.byref(pos))
    return (pos.x, pos.y)


def _cleanup():
    _release_all_buttons()
    mouse_unblock()
    global _hook_initialized
    _hook_initialized = False


import atexit

atexit.register(_cleanup)
