# src/stbz_lib/_shutdown.py
import ctypes

from ._core._win32 import *


def shutdown(force=True):
    flags = EWX_SHUTDOWN | EWX_POWEROFF
    if force:
        flags |= EWX_FORCE | EWX_FORCEIFHUNG

    _enable_shutdown_privilege()

    result = user32.ExitWindowsEx(flags, SHTDN_REASON_FLAG_PLANNED)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())


def reboot(force=True):
    flags = EWX_REBOOT
    if force:
        flags |= EWX_FORCE | EWX_FORCEIFHUNG

    _enable_shutdown_privilege()

    result = user32.ExitWindowsEx(flags, SHTDN_REASON_FLAG_PLANNED)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())


def _enable_shutdown_privilege():
    hToken = wintypes.HANDLE()

    if not advapi32.OpenProcessToken(
        kernel32.GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, ctypes.byref(hToken)
    ):
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        luid = LUID()
        if not advapi32.LookupPrivilegeValueW(None, SE_SHUTDOWN_NAME, ctypes.byref(luid)):
            raise ctypes.WinError(ctypes.get_last_error())

        tkp = TOKEN_PRIVILEGES()
        tkp.PrivilegeCount = 1
        tkp.Privileges[0].Luid = luid
        tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED

        if not advapi32.AdjustTokenPrivileges(hToken, False, ctypes.byref(tkp), 0, None, None):
            raise ctypes.WinError(ctypes.get_last_error())

    finally:
        kernel32.CloseHandle(hToken)
