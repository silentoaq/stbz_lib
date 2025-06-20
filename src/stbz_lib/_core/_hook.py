# src/stbz_lib/_hook.py
import ctypes
import threading
import time

from ._win32 import *


class HookManager:
    def __init__(self):
        self._hook_thread = None
        self._hook_active = False
        self._thread_id = None
        self._keyboard_hook = None
        self._mouse_hook = None
        self._keyboard_cb = None
        self._mouse_cb = None

    def start(self, keyboard_callback=None, mouse_callback=None):
        if self._hook_active:
            return

        self._keyboard_cb = keyboard_callback
        self._mouse_cb = mouse_callback

        self._hook_thread = threading.Thread(target=self._worker, daemon=True)
        self._hook_thread.start()
        time.sleep(0.1)

    def stop(self):
        if not self._hook_active or self._thread_id is None:
            return

        user32.PostThreadMessageW(self._thread_id, WM_QUIT, 0, 0)
        if self._hook_thread:
            self._hook_thread.join(timeout=2.0)
        self._thread_id = None

    def _worker(self):
        """Hook 工作執行緒"""
        self._thread_id = kernel32.GetCurrentThreadId()
        hmod = kernel32.GetModuleHandleW(None)

        if self._keyboard_cb:
            self._keyboard_hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, self._keyboard_cb, hmod, 0)
            if not self._keyboard_hook:
                raise ctypes.WinError(ctypes.get_last_error())

        if self._mouse_cb:
            self._mouse_hook = user32.SetWindowsHookExW(WH_MOUSE_LL, self._mouse_cb, hmod, 0)
            if not self._mouse_hook:
                if self._keyboard_hook:
                    user32.UnhookWindowsHookEx(self._keyboard_hook)
                raise ctypes.WinError(ctypes.get_last_error())

        self._hook_active = True

        msg = MSG()
        try:
            while True:
                ret = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if ret == 0 or msg.message == WM_QUIT:
                    break
                if ret == -1:
                    raise ctypes.WinError(ctypes.get_last_error())
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        finally:
            if self._keyboard_hook:
                user32.UnhookWindowsHookEx(self._keyboard_hook)
                self._keyboard_hook = None
            if self._mouse_hook:
                user32.UnhookWindowsHookEx(self._mouse_hook)
                self._mouse_hook = None
            self._keyboard_cb = None
            self._mouse_cb = None
            self._hook_active = False

    @property
    def is_active(self):
        return self._hook_active


_hook_manager = HookManager()


def start_hook(keyboard_callback=None, mouse_callback=None):
    _hook_manager.start(keyboard_callback, mouse_callback)


def stop_hook():
    _hook_manager.stop()


def is_hook_active():
    return _hook_manager.is_active


import atexit

atexit.register(stop_hook)
