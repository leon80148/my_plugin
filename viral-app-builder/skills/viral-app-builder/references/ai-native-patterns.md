# AI-Native App 開發模式

本文件涵蓋 AI 原生應用程式的整合模式、架構決策與最佳實踐。

---

## LLM 整合模式決策樹

你的 App 需要什麼 AI 能力？

- 文字生成/對話 -> 用 LLM API
  - 需要專業知識？ -> RAG（檢索增強生成）
  - 不需要 -> Direct API Call
  - 需要大幅自訂行為 -> Fine-tuning
  - 小幅自訂 -> System Prompt + Few-shot
- 多步驟推理/工具使用 -> Agent 框架
  - 固定流程 -> LangGraph / CrewAI
  - 動態決策 -> ReAct / Reflexion
- 圖像生成/理解 -> 多模態模型
  - 生成 -> DALL-E / Stable Diffusion / Flux
  - 理解 -> GPT-4V / Claude Vision / Gemini
- 語音 -> Speech API
  - STT -> Whisper / Deepgram / Azure
  - TTS -> ElevenLabs / OpenAI TTS / Azure

## 模型選擇矩陣

| 場景 | 推薦模型 | 備選 | 考量 |
|------|---------|------|------|
| 一般對話/客服 | GPT-4o-mini / Claude Haiku | Gemini Flash | 低成本、低延遲 |
| 複雜推理/程式碼 | Claude Opus / GPT-4o | Gemini Pro | 高品質、較高成本 |
| RAG 問答 | Claude Sonnet / GPT-4o | Mistral Large | 平衡品質與成本 |
| 嵌入/向量化 | text-embedding-3-small | Cohere Embed v3 | 維度/效能比 |
| 圖片理解 | Claude Sonnet / GPT-4o | Gemini Pro Vision | 多模態能力 |
| 即時串流 | GPT-4o-mini / Claude Haiku | Groq (Llama) | TTFT（首 Token 時間） |

## RAG 架構模式

### 基本 RAG Pipeline

Documents -> Chunking -> Embedding -> Vector Store
User Query -> Query Embedding -> Similarity Search -> Context -> LLM -> Response

### Chunking 策略

| 策略 | 適用場景 | Chunk Size |
|------|---------|------------|
| 固定長度 | 結構化文件 | 512-1024 tokens |
| 語義分割 | 長篇文章 | 依段落自然斷點 |
| 遞迴分割 | 程式碼/技術文件 | 依函式/區塊邊界 |
| 句子視窗 | 需要上下文的場景 | 單句 + 前後各 2 句 |
| Parent-Child | 需精確又需全貌 | Child: 256, Parent: 1024 |

### 向量資料庫比較

| 資料庫 | 類型 | 適合場景 | 定價模式 |
|--------|------|---------|---------|
| Pinecone | 托管 | 快速上線、無運維 | 按用量 |
| Weaviate | 自建/托管 | 混合搜尋（向量+關鍵字） | 開源/托管 |
| Qdrant | 自建/托管 | 高效能、多租戶 | 開源/托管 |
| ChromaDB | 嵌入式 | 原型開發、本地測試 | 開源 |
| pgvector | 擴充套件 | 已用 PostgreSQL | 隨 DB |
| Supabase | 托管 | pgvector + Auth + Storage | 按用量 |

## Agent 框架選擇

| 框架 | 適合場景 | 學習曲線 | 可控性 |
|------|---------|---------|--------|
| LangGraph | 複雜狀態機、多 Agent | 中高 | 高 |
| CrewAI | 角色扮演、團隊協作 | 低 | 中 |
| AutoGen | 多 Agent 對話 | 中 | 中 |
| Claude Tool Use | 單 Agent + 工具 | 低 | 高 |
| OpenAI Assistants | 快速原型、託管 | 低 | 低 |
| Semantic Kernel | .NET/企業整合 | 中 | 高 |

## AI App UX 模式

### 延遲管理 UX 模式

| 延遲範圍 | 使用者感受 | UX 策略 |
|---------|----------|---------|
| < 300ms | 即時 | 無需處理 |
| 300ms-2s | 稍等 | 顯示 typing indicator |
| 2-10s | 等待 | 串流 + 進度提示 |
| 10-30s | 焦慮 | 分步進度條 + 預估時間 |
| > 30s | 不耐 | 背景處理 + 通知完成 |

### 幻覺防護策略

| 策略 | 實作方式 | 適用場景 |
|------|---------|---------|
| RAG 基礎事實 | 用檢索結果限制回答範圍 | 知識庫問答 |
| 引用標註 | 回答中標記資料來源 | 研究/報告類 |
| 信心分數 | 模型自評信心 + 閾值過濾 | 醫療/法律 |
| 人工審核環 | 低信心回答送人工覆核 | 高風險場景 |
| Fact-checking | 用第二個 LLM 驗證 | 重要事實 |

## 成本優化

### Token 預算管理

成本控制手段：
1. 模型路由：簡單問題用小模型，複雜問題用大模型
2. Prompt 壓縮：移除冗餘指令，用 few-shot 取代長描述
3. 快取：對相似問題快取回答（語意快取）
4. 限流：設定每用戶每日/每小時呼叫上限
5. 批次處理：非即時需求用 Batch API（成本減半）

### 模型路由策略

根據問題複雜度選擇模型：
- 複雜度 < 0.3 -> gpt-4o-mini（簡單問題）
- 複雜度 0.3-0.7 -> claude-sonnet（中等複雜度）
- 複雜度 > 0.7 -> claude-opus（複雜推理）

### 語意快取

流程：
1. 計算 query embedding
2. 搜尋相似的已快取 query（閾值 0.95）
3. 命中 -> 回傳快取結果
4. 未命中 -> 呼叫 LLM 生成 -> 存入快取

## 架構模式

### 多模型編排

User Request -> Router (Intent Classification) -> Dispatcher
- 簡單查詢 -> GPT-4o-mini
- 知識問答 -> RAG + Claude Sonnet
- 程式碼生成 -> Claude Opus
- 圖片分析 -> GPT-4V
- 翻譯 -> DeepL API
最後經 Post-processor 格式化和安全過濾後回傳。

### 記憶管理

| 記憶類型 | 儲存方式 | 生命週期 | 範例 |
|---------|---------|---------|------|
| 短期記憶 | Context Window | 單次對話 | 對話歷史 |
| 工作記憶 | 會話變數 | 跨輪次 | 使用者偏好 |
| 長期記憶 | 向量 DB / KV Store | 跨會話 | 過往互動摘要 |
| 外部記憶 | RAG 文件庫 | 持久 | 知識庫 |

## 安全與合規

### AI 應用安全檢查清單

- Prompt Injection 防護（輸入消毒、指令隔離）
- 輸出過濾（PII 偵測、有害內容過濾）
- Rate Limiting（防止濫用）
- API Key 管理（不暴露在前端）
- 日誌記錄（保留審計軌跡，但排除敏感資料）
- 模型輸出免責聲明（使用者知道是 AI 生成）
