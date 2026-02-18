# 技術棧比較與選型指南

本文件提供 App 開發各層面的技術選型比較。

---

## 跨平台框架比較

| 框架 | 語言 | 效能 | 生態系 | 學習曲線 | 適合場景 |
|------|------|------|--------|---------|--------|
| React Native | JS/TS | 好 | 最大 | 低 | 一般 App、快速開發 |
| Flutter | Dart | 優秀 | 大 | 中 | 自訂 UI、多平台 |
| .NET MAUI | C# | 好 | 中 | 中 | 企業 App |
| KMP | Kotlin | 優秀 | 中 | 中高 | 共享邏輯、原生 UI |
| Capacitor | Web | 一般 | 大 | 低 | Web 轉行動 |

### 選擇建議

- Web 團隊 + 效能要求高: React Native (New Architecture)
- Web 團隊 + 效能一般: Capacitor
- 高度自訂 UI: Flutter
- Native 團隊 + 共享邏輯: KMP
- .NET 團隊: MAUI
- 快速上線: React Native
- 長期投資: Flutter

---

## BaaS 比較

| 服務 | 資料庫 | Auth | Storage | Functions | 開源 |
|------|--------|------|---------|-----------|------|
| Firebase | Firestore | 完整 | 有 | Cloud Functions | 否 |
| Supabase | PostgreSQL | 完整 | 有 | Edge Functions | 是 |
| Amplify | DynamoDB | Cognito | S3 | Lambda | 部分 |
| Pocketbase | SQLite | 基本 | 有 | Go hooks | 是 |
| Appwrite | MariaDB | 完整 | 有 | Functions | 是 |

### 免費方案

| 服務 | DB | Auth | 儲存 | Functions |
|------|-----|------|------|----------|
| Firebase | 1 GiB | 無限 | 5 GB | 2M/月 |
| Supabase | 500 MB | 50K MAU | 1 GB | 500K/月 |
| Amplify | 25 GB | 50K MAU | 5 GB | 1M/月 |
| Pocketbase | 無限 | 無限 | 無限 | 無限 |
| Appwrite | 2 GB | 75K MAU | 2 GB | 750K/月 |

### 選擇建議

- 快速原型 + Google: Firebase
- 快速原型 + SQL: Supabase
- 超低預算: Pocketbase
- 即時同步 + 文件: Firebase
- 即時同步 + 表格: Supabase Realtime
- AWS 綁定: Amplify
- 需自建: Pocketbase / Appwrite

---

## AI 服務比較

| 提供商 | 主力模型 | 價格(1M tokens) | 強項 |
|--------|---------|----------------|------|
| OpenAI | GPT-4o, o1 | .50 input | 生態最大 |
| Anthropic | Claude | .00 input | 長上下文 |
| Google | Gemini | .25 input | 多模態 |
| Mistral | Large | .00 input | 歐洲隱私 |
| Groq | Llama 3 | 免費有限 | 極速推理 |
| Together | 多模型 | /usr/bin/bash.20 (8B) | 開源託管 |

### 選型依據

| 考量 | 推薦 |
|------|------|
| 最佳品質 | Claude Opus / GPT-4o |
| 性價比 | Claude Sonnet / Gemini Pro |
| 最低延遲 | Groq / GPT-4o-mini |
| 隱私(歐洲) | Mistral / 自建 |
| 長文件 | Claude (200K) / Gemini (1M) |
| 最低成本 | Gemini Flash / GPT-4o-mini |

---

## 資料庫選擇

| 資料庫 | 類型 | 適合場景 | 擴展性 |
|--------|------|---------|--------|
| PostgreSQL | 關聯式 | 通用、複雜查詢 | 垂直+讀寫分離 |
| MySQL | 關聯式 | 傳統 Web | 主從複製 |
| MongoDB | 文件 | 彈性 Schema | 水平 Sharding |
| Redis | KV/快取 | 快取、Session | Cluster |
| DynamoDB | KV/文件 | AWS、高吞吐 | 自動 |
| SQLite | 嵌入式 | 本地 App | 單機 |
| ClickHouse | 列式 | 分析、日誌 | 水平 |
| Turso | 邊緣 SQLite | 全球低延遲 | 分散式 |

---

## 預算分級

### Tier 1: /usr/bin/bash/月

| 層面 | 選擇 |
|------|------|
| 前端 | React Native + Expo |
| 後端 | Supabase Free / Pocketbase |
| AI | GPT-4o-mini / Gemini Free |
| 部署 | Vercel Free / Railway Free |
| 分析 | PostHog Free / GA4 |
| 適合 | Side Project |

### Tier 2: 0-100/月

| 層面 | 選擇 | 月費 |
|------|------|-----|
| 後端 | Supabase Pro | 5 |
| AI | OpenAI / Anthropic | 0-50 |
| 部署 | Vercel Pro | 0 |
| 合計 | | 5-95 |
| 適合 | MVP | |

### Tier 3: 00-500/月

| 層面 | 選擇 | 月費 |
|------|------|-----|
| 後端 | Supabase Pro+ | 0 |
| AI | Multi-model | 0-200 |
| 部署 | Vercel Pro+CDN | 0 |
| 監控 | Sentry | 6 |
| 合計 | | 66-366 |
| 適合 | PMF 後擴張 | |

### Tier 4: 00+/月

| 層面 | 選擇 |
|------|------|
| 後端 | AWS/GCP 自建 |
| AI | 專用方案 + Fine-tune |
| 部署 | Kubernetes |
| 分析 | Amplitude + 倉儲 |
| 監控 | Datadog / Grafana |
| 適合 | 規模化 |

---

## 開發工具

| 類別 | 工具 | 用途 |
|------|------|------|
| 版本控制 | Git + GitHub | 程式碼 |
| CI/CD | GitHub Actions | 自動化 |
| 專案管理 | Linear | 任務 |
| 設計 | Figma | UI/UX |
| API 測試 | Bruno / Insomnia | API |
| 錯誤追蹤 | Sentry | 錯誤通知 |
| LLM 監控 | LangSmith / Helicone | AI 觀測 |
| Prompt 評測 | Promptfoo | 開源 |
| 多 LLM API | LiteLLM | 統一 API |
