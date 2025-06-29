# src/stbz_lib/_mic.py
import ctypes
import threading
from ctypes import HRESULT, POINTER, c_float
from ctypes.wintypes import BOOL, DWORD, UINT
from enum import Enum

from ._core._win32 import (
    CLSCTX_ALL,
    GUID,
    LPCWSTR,
    CLSID_MMDeviceEnumerator,
    IID_IAudioEndpointVolume,
    IID_IMMDevice,
    IID_IMMDeviceEnumerator,
    IUnknown,
    ole32,
)


class EDataFlow(Enum):
    eRender = 0
    eCapture = 1
    eAll = 2


class ERole(Enum):
    eConsole = 0
    eMultimedia = 1
    eCommunications = 2


class IAudioEndpointVolume(IUnknown):
    _iid_ = IID_IAudioEndpointVolume
    _methods_ = (
        # RegisterControlChangeNotify
        ('RegisterControlChangeNotify', HRESULT, [ctypes.c_void_p]),
        # UnregisterControlChangeNotify
        ('UnregisterControlChangeNotify', HRESULT, [ctypes.c_void_p]),
        # GetChannelCount
        ('GetChannelCount', HRESULT, [POINTER(UINT)]),
        # SetMasterVolumeLevel
        ('SetMasterVolumeLevel', HRESULT, [c_float, POINTER(GUID)]),
        # SetMasterVolumeLevelScalar
        ('SetMasterVolumeLevelScalar', HRESULT, [c_float, POINTER(GUID)]),
        # GetMasterVolumeLevel
        ('GetMasterVolumeLevel', HRESULT, [POINTER(c_float)]),
        # GetMasterVolumeLevelScalar
        ('GetMasterVolumeLevelScalar', HRESULT, [POINTER(c_float)]),
        # SetChannelVolumeLevel
        ('SetChannelVolumeLevel', HRESULT, [UINT, c_float, POINTER(GUID)]),
        # SetChannelVolumeLevelScalar
        ('SetChannelVolumeLevelScalar', HRESULT, [DWORD, c_float, POINTER(GUID)]),
        # GetChannelVolumeLevel
        ('GetChannelVolumeLevel', HRESULT, [UINT, POINTER(c_float)]),
        # GetChannelVolumeLevelScalar
        ('GetChannelVolumeLevelScalar', HRESULT, [DWORD, POINTER(c_float)]),
        # SetMute
        ('SetMute', HRESULT, [BOOL, POINTER(GUID)]),
        # GetMute
        ('GetMute', HRESULT, [POINTER(BOOL)]),
        # GetVolumeStepInfo
        ('GetVolumeStepInfo', HRESULT, [POINTER(DWORD), POINTER(DWORD)]),
        # VolumeStepUp
        ('VolumeStepUp', HRESULT, [POINTER(GUID)]),
        # VolumeStepDown
        ('VolumeStepDown', HRESULT, [POINTER(GUID)]),
        # QueryHardwareSupport
        ('QueryHardwareSupport', HRESULT, [POINTER(DWORD)]),
        # GetVolumeRange
        ('GetVolumeRange', HRESULT, [POINTER(c_float), POINTER(c_float), POINTER(c_float)]),
    )


class IMMDevice(IUnknown):
    _iid_ = IID_IMMDevice
    _methods_ = (
        # Activate
        ('Activate', HRESULT, [POINTER(GUID), DWORD, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p)]),
        # OpenPropertyStore
        ('OpenPropertyStore', HRESULT, [DWORD, ctypes.POINTER(ctypes.c_void_p)]),
        # GetId
        ('GetId', HRESULT, [POINTER(LPCWSTR)]),
        # GetState
        ('GetState', HRESULT, [POINTER(DWORD)]),
    )


class IMMDeviceEnumerator(IUnknown):
    _iid_ = IID_IMMDeviceEnumerator
    _methods_ = (
        # EnumAudioEndpoints
        ('EnumAudioEndpoints', HRESULT, [DWORD, DWORD, ctypes.POINTER(ctypes.c_void_p)]),
        # GetDefaultAudioEndpoint
        ('GetDefaultAudioEndpoint', HRESULT, [DWORD, DWORD, ctypes.POINTER(POINTER(IMMDevice))]),
        # GetDevice
        ('GetDevice', HRESULT, [LPCWSTR, ctypes.POINTER(ctypes.c_void_p)]),
        # RegisterEndpointNotificationCallback
        ('RegisterEndpointNotificationCallback', HRESULT, [ctypes.c_void_p]),
        # UnregisterEndpointNotificationCallback
        ('UnregisterEndpointNotificationCallback', HRESULT, [ctypes.c_void_p]),
    )


_mic_muted = False
_mic_lock = threading.Lock()
_com_initialized = False
_volume_endpoint = None


def _ensure_com_initialized():
    """確保 COM 已初始化"""
    global _com_initialized
    if not _com_initialized:
        hr = ole32.CoInitialize(None)
        if hr < 0 and hr != -2147417850:
            raise ctypes.WinError(hr)
        _com_initialized = True


def _get_volume_endpoint():
    """取得音量控制端點"""
    global _volume_endpoint

    if _volume_endpoint is None:
        _ensure_com_initialized()

        enumerator_ptr = ctypes.c_void_p()
        hr = ole32.CoCreateInstance(
            ctypes.byref(CLSID_MMDeviceEnumerator),
            None,
            CLSCTX_ALL,
            ctypes.byref(IMMDeviceEnumerator._iid_),
            ctypes.byref(enumerator_ptr),
        )

        if hr < 0:
            raise ctypes.WinError(hr)

        enumerator = ctypes.cast(enumerator_ptr, POINTER(IMMDeviceEnumerator))

        device = POINTER(IMMDevice)()
        hr = enumerator[0].GetDefaultAudioEndpoint(EDataFlow.eCapture.value, ERole.eConsole.value, ctypes.byref(device))

        if hr < 0:
            raise ctypes.WinError(hr)

        endpoint_ptr = ctypes.c_void_p()
        hr = device[0].Activate(ctypes.byref(IAudioEndpointVolume._iid_), CLSCTX_ALL, None, ctypes.byref(endpoint_ptr))

        if hr < 0:
            raise ctypes.WinError(hr)

        _volume_endpoint = ctypes.cast(endpoint_ptr, POINTER(IAudioEndpointVolume))

    return _volume_endpoint


def mic_block():
    """
    阻擋（靜音）麥克風
    """
    global _mic_muted

    with _mic_lock:
        try:
            endpoint = _get_volume_endpoint()
            hr = endpoint[0].SetMute(True, None)
            if hr < 0:
                raise ctypes.WinError(hr)
            _mic_muted = True
        except Exception as e:
            raise RuntimeError(f"無法靜音麥克風: {e}")


def mic_unblock():
    """
    取消阻擋（取消靜音）麥克風
    """
    global _mic_muted

    with _mic_lock:
        try:
            endpoint = _get_volume_endpoint()
            hr = endpoint[0].SetMute(False, None)
            if hr < 0:
                raise ctypes.WinError(hr)
            _mic_muted = False
        except Exception as e:
            raise RuntimeError(f"無法取消靜音麥克風: {e}")


def is_mic_blocked():
    """
    檢查麥克風是否被阻擋（靜音）
    返回 : True 表示被阻擋（靜音），False 表示未被阻擋
    """
    with _mic_lock:
        try:
            endpoint = _get_volume_endpoint()
            is_muted = BOOL()
            hr = endpoint[0].GetMute(ctypes.byref(is_muted))
            if hr < 0:
                raise ctypes.WinError(hr)
            return bool(is_muted.value)
        except Exception:
            return _mic_muted


def _cleanup():
    """清理資源"""
    global _volume_endpoint, _com_initialized, _mic_muted

    if _mic_muted:
        try:
            mic_unblock()
        except:
            pass

    _volume_endpoint = None

    if _com_initialized:
        ole32.CoUninitialize()
        _com_initialized = False


import atexit

atexit.register(_cleanup)
