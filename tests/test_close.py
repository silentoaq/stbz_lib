# tests/test_close.py
import time

from stbz_lib import close


def test_close_windows():
    """測試關閉視窗"""
    windows = [("League of Legends", "League of Legends"), ("記事本", "記事本"), ("PUBG:", "PUBG")]

    for search_name, display_name in windows:
        print(f"\n測試關閉 {display_name}...")
        closed = close(search_name, delay_ms=100)
        if closed > 0:
            print(f"✓ 成功關閉 {closed} 個視窗")
        else:
            print(f"✗ 沒有找到視窗")

        time.sleep(0.5)


def run_all_tests():
    """執行所有測試"""
    try:
        print("=== 開始關閉視窗測試 ===")
        test_close_windows()
        print("\n=== 測試完成 ===")
    except Exception as e:
        print(f"\n測試失敗: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
