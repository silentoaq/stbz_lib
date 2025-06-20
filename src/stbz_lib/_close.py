# src/stbz_lib/_close.py
import ctypes
import time

from ._core._win32 import *


# ── 內部函數 ─────────────────────────────────────────
def _find_windows(name):
    found_hwnds = []
    name_lower = name.lower()

    @WNDENUMPROC
    def enum_proc(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        ln = user32.GetWindowTextLengthW(hwnd)
        if ln == 0:
            return True
        buf = ctypes.create_unicode_buffer(ln + 1)
        user32.GetWindowTextW(hwnd, buf, ln + 1)
        if name_lower in buf.value.lower():
            found_hwnds.append(hwnd)
        return True

    user32.EnumWindows(enum_proc, 0)
    return found_hwnds


# ── 公開 API ─────────────────────────────────────────
def close(name, delay_ms=0):
    """
    關閉所有符合名稱的視窗
    name     : 視窗標題（部分匹配）
    delay_ms : 每個視窗關閉之間的延遲（毫秒）
    返回     : 關閉的視窗數量
    """
    hwnds = _find_windows(name)

    if not hwnds:
        return 0

    for i, hwnd in enumerate(hwnds):
        if i > 0 and delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)

    return len(hwnds)
