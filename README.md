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
| `remotion-best-practices` | Remotion 影片製作最佳實踐（React 影片、動畫、字幕、音訊、3D） |
| `nhri-risk-plugin` | 國衛院 NHRI V4 健康風險評估（CHD、中風、高血壓、糖尿病、MACE） |
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

## 推薦的其他 Plugin Marketplaces

| Marketplace | 說明 | 安裝指令 |
|---|---|---|
| **Awesome Claude Skills** | 社群精選技能合集 | `/plugin marketplace add ComposioHQ/awesome-claude-skills` |
| **Claude Official Plugins** | Anthropic 官方插件 | `/plugin marketplace add anthropics/claude-plugins-official` |
| **Everything Claude Code** | 全方位開發技能套件（40+ skills） | `/plugin marketplace add affaan-m/everything-claude-code` |
| **Jeffallan Claude Skills** | 社群貢獻技能集 | `/plugin marketplace add Jeffallan/claude-skills` |

## License

MIT
