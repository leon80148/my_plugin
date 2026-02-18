---
name: instinct-export
description: 匯出 instincts 供分享給隊友或其他專案
command: true
---

# Instinct Export 指令

匯出 instincts 為可分享格式。適用於：
- 分享給隊友
- 轉移至新機器
- 貢獻至專案慣例

## 實作方式

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" export [--output file] [--domain name] [--min-confidence n]
```

Windows 環境下若 python3 不可用，改用 python：

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" export [--output file]
```

## 使用方式

```
/instinct-export                           # 匯出所有個人 instincts
/instinct-export --domain testing          # 僅匯出 testing 領域
/instinct-export --min-confidence 0.7      # 僅匯出高信心度 instincts
/instinct-export --output team-instincts.yaml
```

## 執行步驟

1. 讀取 `~/.claude/homunculus/instincts/personal/` 中的 instincts
2. 依旗標篩選
3. 移除敏感資訊：
   - 移除 session ID
   - 移除檔案路徑（僅保留模式）
   - 移除超過一週的時戳
4. 產生匯出檔案

## 輸出格式

產生 YAML 檔案：

```yaml
# Instincts Export
# Generated: 2025-01-22
# Source: personal
# Count: 12 instincts

---
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.8
domain: code-style
source: session-observation
---

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 8 instances of functional pattern preference
```

## 隱私考量

匯出包含：
- 觸發模式 (triggers)
- 動作描述 (actions)
- 信心度評分 (confidence scores)
- 領域標籤 (domains)
- 觀察次數 (observation counts)

匯出不包含：
- 實際程式碼片段
- 檔案路徑
- Session 對話記錄
- 個人識別資訊

## 可用旗標

- `--domain <name>`: 僅匯出指定領域
- `--min-confidence <n>`: 最低信心度閾值（預設：0.3）
- `--output <file>`: 輸出檔案路徑（預設：instincts-export-YYYYMMDD.yaml）
- `--format <yaml|json|md>`: 輸出格式（預設：yaml）
- `--include-evidence`: 包含證據文字（預設：排除）
