"""
stbz_lib 對外 API。
"""

from ._capture import capture
from ._kb import kb_block, kb_hold, kb_tap, kb_unblock
from ._mouse import mouse_block, mouse_hold, mouse_move, mouse_pos, mouse_tap, mouse_unblock

__all__ = [
    # 鍵盤
    "kb_block",
    "kb_unblock",
    "kb_tap",
    "kb_hold",
    # 滑鼠
    "mouse_block",
    "mouse_unblock",
    "mouse_tap",
    "mouse_hold",
    "mouse_pos",
    "mouse_move",
    # 截圖
    "capture",
]
