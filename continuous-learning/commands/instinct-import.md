---
name: instinct-import
description: 從隊友、Skill Creator 或其他來源匯入 instincts
command: true
---

# Instinct Import 指令

## 實作方式

使用插件根路徑執行 instinct CLI：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [--force] [--min-confidence 0.7]
```

Windows 環境下若 python3 不可用，改用 python：

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" import <file-or-url>
```

匯入來源：
- 隊友的匯出檔
- Skill Creator（repo 分析）
- 社群 instinct 集合
- 先前機器的備份
- 本插件的 seeds 目錄

## 使用方式

```
/instinct-import team-instincts.yaml
/instinct-import https://github.com/org/repo/instincts.yaml
/instinct-import ./seeds/plugin-marketplace.yaml
```

## 執行步驟

1. 取得 instinct 檔案（本地路徑或 URL）
2. 解析並驗證格式
3. 與現有 instincts 檢查重複
4. 合併或新增 instincts
5. 儲存至 `~/.claude/homunculus/instincts/inherited/`

## 匯入流程

```
Importing instincts from: team-instincts.yaml
================================================

Found 12 instincts to import.

NEW (8):
  + use-zod-validation (confidence: 0.70)
  + prefer-named-exports (confidence: 0.65)
  + test-async-functions (confidence: 0.80)

UPDATE (1):
  ~ test-first-workflow (confidence: 0.90)

SKIP (3 - already exists with equal/higher confidence):
  - prefer-functional-style

Import 8 new, update 1? [y/N]
```

## 合併策略

### 重複處理
匯入與既有相符的 instinct 時：
- **高信心度優先**: 保留信心度較高者
- **合併證據**: 結合觀察次數
- **更新時戳**: 標記為最近驗證

### 衝突處理
匯入與既有矛盾的 instinct 時：
- **預設跳過**: 不匯入衝突的 instincts
- **標記審查**: 標記兩者需要注意
- **手動解決**: 由使用者決定保留哪個

## 來源追蹤

匯入的 instincts 會標記：
```yaml
source: "inherited"
imported_from: "team-instincts.yaml"
imported_at: "2025-01-22T10:30:00Z"
original_source: "session-observation"
```

## 可用旗標

- `--dry-run`: 預覽而不實際匯入
- `--force`: 跳過確認直接匯入
- `--merge-strategy <higher|local|import>`: 重複時的處理策略
- `--min-confidence <n>`: 僅匯入信心度高於閾值的 instincts

## 匯入完成輸出

```
Import complete!

   Added: 8 instincts
   Updated: 1 instinct
   Skipped: 3 instincts (2 duplicates, 1 conflict)

   Saved to: ~/.claude/homunculus/instincts/inherited/

Run /instinct-status to see all instincts.
```
