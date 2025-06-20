# tests/test_capture.py
import time

from stbz_lib import capture


def test_capture_windows():
    """測試截取指定視窗"""
    windows = [("League of Legends", "League of Legends"), ("記事本", "記事本"), ("PUBG:", "PUBG")]

    for search_name, display_name in windows:
        print(f"\n測試截取 {display_name}...")
        try:
            img, info = capture(search_name)
            print(f"✓ 成功截取 {display_name}")
            print(f"  HWND: {info['hwnd']}")
            print(f"  位置: ({info['x']}, {info['y']})")
            print(f"  大小: {info['width']} x {info['height']}")
            print(f"  圖像: {img.shape} {img.dtype}")
        except RuntimeError as e:
            print(f"✗ {display_name} - {e}")

        time.sleep(0.5)


def run_all_tests():
    """執行所有測試"""
    try:
        print("=== 開始截圖測試 ===")
        test_capture_windows()
        print("\n=== 測試完成 ===")
    except Exception as e:
        print(f"\n測試失敗: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
