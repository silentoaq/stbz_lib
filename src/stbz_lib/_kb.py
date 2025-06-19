# src/stbz_lib/_kb.py
"""
鍵盤相關 API
- kb_block(keys)
- kb_unblock(keys)
- kb_tap(key)
- kb_hold(key)
"""


def kb_block(keys=None):
    """阻擋指定按鍵"""
    raise NotImplementedError


def kb_unblock(keys=None):
    """取消阻擋"""
    raise NotImplementedError


def kb_tap(key, count=1, interval_ms=50):
    """模擬點按按鍵"""
    raise NotImplementedError


def kb_hold(key, duration_ms=100, count=1, interval_ms=50):
    """模擬按住按鍵"""
    raise NotImplementedError
