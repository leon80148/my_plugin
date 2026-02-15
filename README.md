# Leon's Claude Code Plugins

Claude Code plugin marketplace - 包含醫療內容創作、AI 訓練、文件撰寫、App 開發等工具集。

## Plugins

| Plugin | 說明 |
|---|---|
| `health-education-writer` | 生成有溫度且專業可信的醫療衛教文章 |
| `lora-training-prompts` | 生成一致性 AI 圖像提示詞用於 LoRA 訓練資料集 |
| `quickstart-doc-writer` | 產出快速上手說明文件 |
| `viral-app-builder` | 跨平台爆款 App 全生命週期開發助手 |
| `nhs-pportal-screening` | 國健署預防保健篩檢資格查詢系統 |
| `ui-ux-pro-max` | UI/UX 設計智能系統（67 風格、96 調色盤、56 字體配對） |
| `vision-database` | 展望醫療系統 HIS 資料庫查詢 |
| `medical-content-team` | 醫療內容創作 Agent 團隊（6 Agents + 2 Commands） |

## 安裝方式

```bash
# 1. 加入 marketplace
/plugin marketplace add <username>/my_plugin

# 2. 安裝想要的 plugin
/plugin install health-education-writer@leon-claude-plugins
/plugin install medical-content-team@leon-claude-plugins
# ... 或安裝其他 plugin
```

## 本地測試

```bash
# 測試單一 plugin
claude --plugin-dir ./health-education-writer
claude --plugin-dir ./medical-content-team
```

## medical-content-team 使用方式

安裝後可使用以下指令：

- `/medical-content-team:discuss [主題]` - 啟動 6 人 Agent 團隊協作創作醫療衛教文章
- `/medical-content-team:extract-figures [PDF路徑]` - 從學術 PDF 提取圖表

### Agent 團隊成員

| Agent | 角色 |
|---|---|
| Facilitator | 會議主持人、團隊協調者 |
| Medical Journalist | 醫學記者、散文敘事撰稿人 |
| Science Gatekeeper | 醫學事實審查員 |
| Patient Advocate | 病人可讀性代言人 |
| Devil's Advocate | 批判思考、偏見檢測 |
| Traffic Hunter | 社群媒體優化、流量策略 |

## License

MIT
