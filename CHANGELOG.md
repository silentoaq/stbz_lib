# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-06-21

### Added
- 新增 MIT 授權檔 **LICENSE**
- 補上模組 metadata：

## [0.1.0](https://github.com/silentoaq/stbz_lib/releases/tag/v0.1.0) - 2025-06-21

### Added

* **鍵盤控制功能**

  * `kb_tap()` - 模擬按鍵點擊，支援連續多次點擊

  * `kb_hold()` - 模擬按住按鍵，支援自定義持續時間

  * `kb_block()` - 阻擋指定按鍵或所有按鍵輸入

  * `kb_unblock()` - 取消按鍵阻擋

* **滑鼠控制功能**

  * `mouse_tap()` - 模擬滑鼠點擊（左鍵、右鍵、中鍵、側鍵）

  * `mouse_hold()` - 模擬按住滑鼠按鍵

  * `mouse_pos()` - 移動滑鼠到指定座標

  * `mouse_move()` - 移動滑鼠到螢幕邊緣並持續移動

  * `mouse_block()` - 阻擋滑鼠按鍵或移動

  * `mouse_unblock()` - 取消滑鼠阻擋

* **截圖功能**

  * `capture()` - 截取指定視窗畫面，返回 numpy 陣列格式圖像

* **關閉進程功能**

  * `close()` - 強制關閉符合名稱的所有進程

* **核心架構**

  * 基於 Windows Hook 機制的低階鍵盤滑鼠控制

  * 執行緒安全的全域狀態管理

  * 自動清理機制（程式結束時釋放所有按鍵和取消阻擋）
