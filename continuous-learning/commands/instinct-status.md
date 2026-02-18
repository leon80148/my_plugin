---
name: instinct-status
description: 顯示所有已學習的 instincts 及其信心度
command: true
---

# Instinct Status 指令

顯示所有已學習的 instincts，依領域分組並附信心度評分。

## 實作方式

使用插件根路徑執行 instinct CLI：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" status
```

若 `CLAUDE_PLUGIN_ROOT` 未設定（手動安裝），使用：

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py status
```

Windows 環境下若 python3 不可用，改用 python：

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" status
```

## 使用方式

```
/instinct-status
/instinct-status --domain code-style
/instinct-status --low-confidence
```

## 執行步驟

1. 讀取 `~/.claude/homunculus/instincts/personal/` 中所有 instinct 檔案
2. 讀取 `~/.claude/homunculus/instincts/inherited/` 中繼承的 instincts
3. 依領域分組，顯示信心度長條圖

## 輸出格式

```
INSTINCT STATUS - 9 total
==================

  Personal:  4
  Inherited: 5

## CODE-STYLE (4)

  [########..] 80%  prefer-functional-style
            trigger: when writing new functions
            action: Use functional patterns over classes

  [######....] 60%  use-path-aliases
            trigger: when importing modules
            action: Use @/ path aliases instead of relative imports

## TESTING (2)

  [#########.] 90%  test-first-workflow
            trigger: when adding new functionality
            action: Write test first, then implementation

## WORKFLOW (3)

  [#######...] 70%  grep-before-edit
            trigger: when modifying code
            action: Search with Grep, confirm with Read, then Edit

---
Total: 9 instincts (4 personal, 5 inherited)
Observer: Running (last analysis: 5 min ago)
```

## 可用旗標

- `--domain <name>`: 依領域篩選（code-style, testing, git 等）
- `--low-confidence`: 僅顯示信心度 < 0.5 的 instincts
- `--high-confidence`: 僅顯示信心度 >= 0.7 的 instincts
- `--source <type>`: 依來源篩選（session-observation, repo-analysis, inherited）
- `--json`: 輸出 JSON 格式供程式化使用
