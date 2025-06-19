# tests/test_kb.py
"""
鍵盤功能測試 - 以 WASD 為主
"""
import time

from stbz_lib import kb_block, kb_hold, kb_tap, kb_unblock
from stbz_lib._kb import get_blocked_keys, is_key_blocked

# 虛擬鍵碼定義
VK_W = 0x57
VK_A = 0x41
VK_S = 0x53
VK_D = 0x44
VK_SPACE = 0x20
VK_ESCAPE = 0x1B


def test_kb_tap_single():
    """測試單次點按"""
    print("測試單次點按 W...")
    kb_tap(VK_W)
    time.sleep(0.5)


def test_kb_tap_multiple():
    """測試多次點按"""
    print("測試連續點按 WASD 各3次...")
    for key in [VK_W, VK_A, VK_S, VK_D]:
        kb_tap(key, count=3, interval_ms=100)
        time.sleep(0.5)


def test_kb_hold():
    """測試按住按鍵"""
    print("測試按住 W 鍵 1 秒...")
    kb_hold(VK_W, duration_ms=1000)
    time.sleep(0.5)

    print("測試按住 Space 鍵 0.5 秒，重複 3 次...")
    kb_hold(VK_SPACE, duration_ms=500, count=3, interval_ms=200)


def test_kb_block_unblock():
    """測試阻擋和取消阻擋"""
    print("\n測試阻擋 WASD 按鍵...")
    wasd_keys = [VK_W, VK_A, VK_S, VK_D]

    # 阻擋 WASD
    kb_block(wasd_keys)

    # 檢查阻擋狀態
    assert all(is_key_blocked(key) for key in wasd_keys)
    blocked = get_blocked_keys()
    print(f"已阻擋的按鍵數量: {len(blocked)}")

    print("請嘗試按 WASD（應該無效）...")
    time.sleep(3)

    # 取消阻擋 W 和 A
    print("\n取消阻擋 W 和 A...")
    kb_unblock([VK_W, VK_A])
    assert not is_key_blocked(VK_W)
    assert not is_key_blocked(VK_A)
    assert is_key_blocked(VK_S)
    assert is_key_blocked(VK_D)

    print("請嘗試按 WASD（W和A應該有效，S和D無效）...")
    time.sleep(3)

    # 取消所有阻擋
    print("\n取消所有阻擋...")
    kb_unblock()
    assert len(get_blocked_keys()) == 0


def test_kb_block_all():
    """測試阻擋所有按鍵"""
    print("\n測試阻擋所有按鍵...")
    kb_block()  # 不傳參數 = 阻擋所有

    blocked_count = len(get_blocked_keys())
    print(f"已阻擋 {blocked_count} 個按鍵")

    print("請嘗試按任意鍵（應該都無效）...")
    time.sleep(3)

    kb_unblock()
    print("已取消所有阻擋")


def test_kb_game_simulation():
    """模擬遊戲操作"""
    print("\n模擬遊戲操作...")

    # 模擬前進
    print("模擬前進 (W)...")
    kb_hold(VK_W, duration_ms=1500)

    # 模擬左右移動
    print("模擬左右閃避 (A-D-A-D)...")
    for _ in range(2):
        kb_tap(VK_A)
        time.sleep(0.2)
        kb_tap(VK_D)
        time.sleep(0.2)

    # 模擬跳躍
    print("模擬跳躍 (Space)...")
    kb_tap(VK_SPACE, count=3, interval_ms=300)

    # 模擬蹲下
    print("模擬蹲下 (S)...")
    kb_hold(VK_S, duration_ms=1000)


def test_interactive():
    """互動式測試"""
    print("\n=== 互動式測試 ===")
    print("按 ESC 結束測試")
    print("1. 測試阻擋：將阻擋 WASD，請嘗試按這些鍵")

    kb_block([VK_W, VK_A, VK_S, VK_D])

    print("\n等待測試（按 ESC 繼續）...")
    # 這裡實際應用中可以加入檢測 ESC 的邏輯
    time.sleep(5)

    kb_unblock()
    print("測試結束，已取消所有阻擋")


def run_all_tests():
    """執行所有測試"""
    try:
        print("=== 開始鍵盤功能測試 ===\n")

        test_kb_tap_single()
        time.sleep(1)

        test_kb_tap_multiple()
        time.sleep(1)

        test_kb_hold()
        time.sleep(1)

        test_kb_block_unblock()
        time.sleep(1)

        test_kb_block_all()
        time.sleep(1)

        test_kb_game_simulation()
        time.sleep(1)

        # test_interactive()  # 可選的互動測試

        print("\n=== 所有測試完成 ===")

    except Exception as e:
        print(f"\n測試失敗: {e}")
        kb_unblock()  # 確保清理阻擋狀態
        raise


if __name__ == "__main__":
    # 提示
    print("請打開一個記事本或文字編輯器來查看按鍵輸出")
    print("3 秒後開始測試...")
    time.sleep(3)

    run_all_tests()
