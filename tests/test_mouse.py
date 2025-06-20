# tests/test_mouse.py
import time

from stbz_lib import mouse_block, mouse_hold, mouse_move, mouse_pos, mouse_tap, mouse_unblock
from stbz_lib._mouse import (
    MOUSE_LEFT,
    MOUSE_MIDDLE,
    MOUSE_MOVE,
    MOUSE_RIGHT,
    MOVE_DOWN,
    MOVE_LEFT,
    MOVE_RIGHT,
    MOVE_UP,
    get_blocked_buttons,
    get_mouse_pos,
    is_button_blocked,
)


def test_mouse_tap_single():
    """測試單次點擊"""
    print("測試單次點擊左鍵...")
    mouse_tap(MOUSE_LEFT)
    time.sleep(0.5)

    print("測試單次點擊右鍵...")
    mouse_tap(MOUSE_RIGHT)
    time.sleep(0.5)


def test_mouse_tap_multiple():
    """測試多次點擊"""
    print("測試連續點擊左鍵 3 次...")
    mouse_tap(MOUSE_LEFT, count=3, interval_ms=200)
    time.sleep(0.5)

    print("測試雙擊（快速點擊 2 次）...")
    mouse_tap(MOUSE_LEFT, count=2, interval_ms=50)
    time.sleep(0.5)


def test_mouse_hold():
    """測試按住滑鼠按鍵"""
    print("測試按住左鍵 1 秒...")
    mouse_hold(MOUSE_LEFT, duration_ms=1000)
    time.sleep(0.5)

    print("測試按住右鍵 0.5 秒，重複 3 次...")
    mouse_hold(MOUSE_RIGHT, duration_ms=500, count=3, interval_ms=200)


def test_mouse_pos():
    """測試滑鼠移動到指定位置"""
    print("\n測試滑鼠定位...")

    original_pos = get_mouse_pos()
    print(f"原始位置: {original_pos}")

    positions = [
        (100, 100),
        (300, 300),
        (500, 500),
        (300, 300),
    ]

    for x, y in positions:
        print(f"移動到 ({x}, {y})...")
        mouse_pos(x, y)
        time.sleep(0.5)

    print(f"返回原始位置 {original_pos}...")
    mouse_pos(*original_pos)


def test_mouse_move():
    """測試滑鼠移動到邊緣"""
    print("\n測試滑鼠邊緣移動...")

    original_pos = get_mouse_pos()

    directions = [
        (MOVE_UP, "上"),
        (MOVE_RIGHT, "右"),
        (MOVE_DOWN, "下"),
        (MOVE_LEFT, "左"),
    ]

    for direction, name in directions:
        print(f"移動到{name}邊緣並持續移動 0.5 秒...")
        mouse_move(direction, duration_ms=500, speed=10)
        time.sleep(0.5)

    mouse_pos(*original_pos)


def test_mouse_block_unblock():
    """測試阻擋和取消阻擋"""
    print("\n測試阻擋滑鼠按鍵...")

    mouse_block([MOUSE_LEFT, MOUSE_RIGHT])

    assert is_button_blocked(MOUSE_LEFT)
    assert is_button_blocked(MOUSE_RIGHT)
    assert not is_button_blocked(MOUSE_MIDDLE)

    blocked = get_blocked_buttons()
    print(f"已阻擋的按鍵數量: {len(blocked)}")

    print("請嘗試點擊左右鍵（應該無效）...")
    time.sleep(3)

    print("\n取消阻擋左鍵...")
    mouse_unblock([MOUSE_LEFT])
    assert not is_button_blocked(MOUSE_LEFT)
    assert is_button_blocked(MOUSE_RIGHT)

    print("請嘗試點擊左右鍵（左鍵應該有效，右鍵無效）...")
    time.sleep(3)

    print("\n取消所有阻擋...")
    mouse_unblock()
    assert len(get_blocked_buttons()) == 0


def test_mouse_block_all():
    """測試阻擋所有滑鼠操作"""
    print("\n測試阻擋所有滑鼠操作...")
    mouse_block()

    blocked_count = len(get_blocked_buttons())
    print(f"已阻擋 {blocked_count} 個滑鼠功能")

    print("請嘗試移動和點擊滑鼠（應該都無效）...")
    time.sleep(3)

    mouse_unblock()
    print("已取消所有阻擋")


def test_mouse_block_move():
    """測試單獨阻擋滑鼠移動"""
    print("\n測試阻擋滑鼠移動...")
    mouse_block([MOUSE_MOVE])

    print("請嘗試移動滑鼠（應該無法移動，但可以點擊）...")
    time.sleep(3)

    mouse_unblock()
    print("已取消移動阻擋")


def test_mouse_game_simulation():
    """模擬遊戲操作"""
    print("\n模擬遊戲操作...")

    original_pos = get_mouse_pos()

    print("模擬射擊（連續點擊左鍵）...")
    mouse_tap(MOUSE_LEFT, count=5, interval_ms=100)

    print("模擬瞄準（按住右鍵）...")
    mouse_hold(MOUSE_RIGHT, duration_ms=2000)

    print("模擬快速轉身...")
    mouse_pos(original_pos[0] + 200, original_pos[1])
    time.sleep(0.2)
    mouse_pos(original_pos[0] - 200, original_pos[1])
    time.sleep(0.2)
    mouse_pos(*original_pos)

    print("模擬滾輪點擊（如果有中鍵）...")
    mouse_tap(MOUSE_MIDDLE, count=2)


def run_all_tests():
    """執行所有測試"""
    try:
        print("=== 開始滑鼠功能測試 ===\n")

        test_mouse_tap_single()
        time.sleep(1)

        test_mouse_tap_multiple()
        time.sleep(1)

        test_mouse_hold()
        time.sleep(1)

        test_mouse_pos()
        time.sleep(1)

        test_mouse_move()
        time.sleep(1)

        test_mouse_block_unblock()
        time.sleep(1)

        test_mouse_block_all()
        time.sleep(1)

        test_mouse_block_move()
        time.sleep(1)

        test_mouse_game_simulation()
        time.sleep(1)

        print("\n=== 所有測試完成 ===")

    except Exception as e:
        print(f"\n測試失敗: {e}")
        mouse_unblock()
        raise


if __name__ == "__main__":
    print("滑鼠測試將會移動和點擊您的滑鼠")
    print("請確保螢幕上沒有重要的操作")
    print("3 秒後開始測試...")
    time.sleep(3)

    run_all_tests()
