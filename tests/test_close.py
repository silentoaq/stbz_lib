# tests/test_close.py
from stbz_lib import close

terminated = close("PUBG:")
print(f"關閉了 {terminated} 個 LOL 進程")
