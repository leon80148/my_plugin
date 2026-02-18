---
name: evolve
description: 將相關 instincts 叢集化為 skills、commands 或 agents
command: true
---

# Evolve 指令

## 實作方式

使用插件根路徑執行 instinct CLI：

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" evolve [--generate]
```

Windows 環境下若 python3 不可用，改用 python：

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/instinct-cli.py" evolve [--generate]
```

分析 instincts 並將相關者叢集化為更高階結構：
- **Commands**: 描述使用者主動觸發的動作
- **Skills**: 描述自動觸發的行為模式
- **Agents**: 描述複雜的多步驟流程

## 使用方式

```
/evolve                    # 分析所有 instincts 並建議進化方向
/evolve --domain testing   # 僅進化 testing 領域的 instincts
/evolve --dry-run          # 預覽而不實際建立
/evolve --threshold 5      # 需要 5+ 相關 instincts 才叢集化
```

## 進化規則

### -> Command（使用者觸發）
當 instincts 描述使用者會明確請求的動作：
- 多個關於「當使用者要求...」的 instincts
- 觸發條件如「建立新 X 時」
- 遵循可重複序列的 instincts

範例：
- `new-table-step1`: 新增資料庫表格時，建立 migration
- `new-table-step2`: 新增資料庫表格時，更新 schema
- `new-table-step3`: 新增資料庫表格時，重新產生型別

-> 建立: **new-table** command

### -> Skill（自動觸發）
當 instincts 描述應自動發生的行為：
- 模式匹配觸發條件
- 錯誤處理回應
- 程式碼風格規範

範例：
- `prefer-functional`: 撰寫函式時，偏好函式式風格
- `use-immutable`: 修改狀態時，使用不可變模式
- `avoid-classes`: 設計模組時，避免 class-based 設計

-> 建立: `functional-patterns` skill

### -> Agent（需要深度/隔離）
當 instincts 描述受益於隔離的複雜多步驟流程：
- 除錯工作流
- 重構序列
- 研究任務

範例：
- `debug-step1`: 除錯時，先檢查 log
- `debug-step2`: 除錯時，隔離失敗元件
- `debug-step3`: 除錯時，建立最小重現
- `debug-step4`: 除錯時，用測試驗證修復

-> 建立: **debugger** agent

## 執行步驟

1. 讀取 `~/.claude/homunculus/instincts/` 中所有 instincts
2. 依以下條件分組：
   - 領域相似度
   - 觸發模式重疊
   - 動作序列關聯
3. 對每個 3+ 相關 instincts 的叢集：
   - 判定進化類型（command/skill/agent）
   - 產生對應檔案
   - 儲存至 `~/.claude/homunculus/evolved/{commands,skills,agents}/`
4. 將進化結構連結回原始 instincts

## 輸出格式

```
EVOLVE ANALYSIS - 15 instincts
==================

High confidence instincts (>=80%): 6

## SKILL CANDIDATES

1. Cluster: "database operations"
   Instincts: 4
   Avg confidence: 85%
   Domains: database, workflow

## COMMAND CANDIDATES (2)

  /new-table
    From: new-table-workflow
    Confidence: 90%

## AGENT CANDIDATES (1)

  debugger-agent
    Covers 4 instincts
    Avg confidence: 82%
```

## 可用旗標

- `--generate`: 實際建立進化結構（預設僅預覽）
- `--dry-run`: 預覽而不建立
- `--domain <name>`: 僅進化指定領域的 instincts
- `--threshold <n>`: 形成叢集所需最少 instincts 數（預設：3）
- `--type <command|skill|agent>`: 僅建立指定類型

## 產生的檔案存放位置

```
~/.claude/homunculus/evolved/
  commands/   # 產生的 command 檔案
  skills/     # 產生的 skill 檔案
  agents/     # 產生的 agent 檔案
```
