# src/stbz_lib/__init__.py
"""
stbz_lib 對外 API。
"""

from ._kb import get_blocked_keys, is_key_blocked, kb_block, kb_hold, kb_tap, kb_unblock
from ._mouse import (
    get_blocked_buttons,
    get_mouse_pos,
    is_button_blocked,
    mouse_block,
    mouse_hold,
    mouse_move,
    mouse_pos,
    mouse_tap,
    mouse_unblock,
)

__all__ = [
    # 鍵盤功能
    "kb_block",
    "kb_unblock",
    "kb_tap",
    "kb_hold",
    "get_blocked_keys",
    "is_key_blocked",
    # 滑鼠功能
    "mouse_block",
    "mouse_unblock",
    "mouse_tap",
    "mouse_hold",
    "mouse_pos",
    "mouse_move",
    "get_blocked_buttons",
    "is_button_blocked",
    "get_mouse_pos",
]

__version__ = "0.0.0"
