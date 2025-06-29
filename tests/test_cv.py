# tests/test_cv.py
import time

from stbz_lib import *

print("=== Hook 交叉測試 ===")
print("3秒後開始...")
time.sleep(5)

print("\n測試1：鍵盤 → 滑鼠")
print("- 按住 W 鍵 1 秒")
kb_hold(0x57, 1000)
print("- 點擊滑鼠左鍵 3 次")
mouse_tap(0x01, 3, 200)
print("✓ 完成")

print("\n測試2：滑鼠 → 鍵盤")
print("- 按住滑鼠右鍵 1 秒")
mouse_hold(0x02, 2000)
print("- 按 Space 鍵 3 次")
kb_tap(0x20, 3, 200)
print("✓ 完成")

print("\n測試3：Hold 後 Block（關鍵測試）")
print("- 按住 W 鍵 1 秒")
kb_hold(0x57, 1000)
print("- 阻擋 WASD 按鍵")
kb_block([0x57, 0x41, 0x53, 0x44])
print("- 請嘗試按 WASD（應該無效）...")
time.sleep(5)
print("- 取消阻擋")
kb_unblock()
print("✓ 完成")

print("\n測試4：鍵盤後滑鼠 Block")
print("- 按 W 鍵 2 次")
kb_tap(0x57, 2)
print("- 阻擋滑鼠左右鍵")
mouse_block([0x01, 0x02])
print("- 請嘗試點擊滑鼠（應該無效）...")
time.sleep(5)
print("- 取消阻擋")
mouse_unblock()
print("✓ 完成")

print("\n=== 所有測試完成！ ===")
