"""
滑鼠相關 API
- mouse_block
- mouse_unblock
- mouse_tap
- mouse_hold
- mouse_move
"""


def mouse_block(button_list=None):
    """阻擋滑鼠按鍵"""
    raise NotImplementedError


def mouse_unblock(button_list=None):
    """取消阻擋"""
    raise NotImplementedError


def mouse_tap(button, count=1, interval_ms=50):
    """點擊滑鼠按鍵"""
    raise NotImplementedError


def mouse_hold(button, duration_ms=100, count=1, interval_ms=50):
    """按住滑鼠按鍵"""
    raise NotImplementedError


def mouse_pos(x, y):
    """滑鼠移動到指定位置"""
    raise NotImplementedError


def mouse_move(direction, duration_ms=1000, speed=5):
    """滑鼠移動到邊緣並持續移動"""
    raise NotImplementedError
