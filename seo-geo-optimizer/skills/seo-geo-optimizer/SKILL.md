---
name: seo-geo-optimizer
description: >
  SEO 與 GEO（生成式引擎最佳化）整合策略工具。分析、撰寫、技術實作、策略規劃四大模式，幫助用戶優化網站內容，使其同時在傳統搜尋引擎和 AI 生成式引擎（ChatGPT、Perplexity、Gemini、Claude、Google AI Overviews）中獲得最大能見度。

  務必在以下任何情境使用此 skill — 即使用戶沒有明確提到 SEO 或 GEO：
  (1) 用戶要求分析、改善、檢查任何網頁或文章的搜尋表現、流量、或 AI 引用率
  (2) 用戶想讓品牌/產品/診所/公司被 ChatGPT、Perplexity 等 AI 搜尋引擎推薦或引用
  (3) 用戶需要撰寫或改寫文章，特別是想改善倒金字塔結構、去除「隨著...發展」等語言雜訊
  (4) 用戶要求建立 llms.txt、llms-full.txt、Schema JSON-LD 結構化資料、或 Markdown 鏡像檔案
  (5) 用戶詢問如何設定 robots.txt 來管理 AI 爬蟲（GPTBot、ClaudeBot、PerplexityBot 等）
  (6) 用戶想進行知識圖譜最佳化（KGO）、品牌實體建構、Wikidata 條目建立
  (7) 用戶詢問 AI 能見度指標追蹤（AIGVR、引用位置、情感分析）、提示詞矩陣建立、或 GEO 工具推薦
  (8) 用戶要進行 SEO/GEO 混合策略規劃、競爭者 AI 引用分析
  (9) 用戶要針對醫療、金融、法律等 YMYL 領域檢查或強化 E-E-A-T 信號
  (10) 用戶提到內容在 AI 搜尋中的表現、品牌在 AI 回答中的情感/準確度問題

  觸發詞：SEO、GEO、生成式引擎最佳化、AI搜尋優化、AI可見度、AI引用、AI推薦、
  llms.txt、llms-full.txt、Schema標記、Schema JSON-LD、結構化資料、FAQPage Schema、
  知識圖譜、E-E-A-T、YMYL、零點擊搜尋、引用佔有率、
  倒金字塔、段落精確度、語言雜訊、多模態搜尋、AI Overviews、Perplexity優化、
  ChatGPT搜尋、ChatGPT推薦、品牌實體、數位公關、內容工程、機器可讀性、AIGVR、
  搜尋引擎優化、網站優化、關鍵字優化、內容優化、排名優化、
  robots.txt AI爬蟲、GPTBot、ClaudeBot、PerplexityBot、提示詞矩陣、Prompt Matrix、
  AI能見度追蹤、品牌聲譽、內容衰退、Content Decay
---

# SEO & GEO 整合最佳化 Skill

基於普林斯頓大學 GEO-bench 研究成果及 2025-2026 年最新業界實踐，提供 SEO（搜尋引擎最佳化）與 GEO（生成式引擎最佳化）的整合策略框架。核心目標：讓用戶的內容同時在傳統 SERP 和 AI 合成回覆中獲得最大能見度。

## 工作模式

根據用戶需求，選擇對應模式執行：

| 模式 | 適用場景 | 輸出 |
|------|----------|------|
| **A：內容分析** | 分析現有文章/網頁的 SEO/GEO 表現 | 六維度評分報告 + 行動清單 |
| **B：內容撰寫** | 從零撰寫或改寫符合 GEO 原則的內容 | 結構化文章 |
| **C：技術實作** | 生成 llms.txt、Schema JSON-LD、Markdown 鏡像 | 技術檔案 |
| **D：策略規劃** | 制定 SEO/GEO 混合策略、KPI 體系、工具選型 | 策略文件 |

若用戶需求跨模式，依序執行（如先 A 分析再 B 改寫）。

---

## 模式 A：內容分析與優化建議

對用戶提供的內容進行六大維度評分（每項 0-10 分，滿分 60）：

### 1. GEO 三大驅動因子

根據普林斯頓 GEO-bench 研究，以下為提升 AI 引用率最有效的三項策略：

| 因子 | AI 引用率提升 | 檢核重點 |
|------|--------------|----------|
| 統計數據密度 | +33.9% | 具體數字、百分比、時間戳記，明確來源歸屬 |
| 專家語錄嵌入 | +32% | 具名專家直接觀點，含姓名/頭銜/機構 |
| 權威來源引用 | +30.3% | 附出處連結，權威層級：學術論文 > 權威媒體 > 產業報告 |

**判斷標準**：
- 8-10 分：三項因子齊全，每 200-300 字至少 1 個數據點
- 5-7 分：具備 2 項因子，但密度不足
- 0-4 分：缺乏數據、語錄或來源引用

### 2. 結構與機器可讀性

- **倒金字塔結構**：每段落前 50-75 字是否為直接宣告式解答
- **模組化架構**：每個觀念獨立成區塊，語意 HTML（H2/H3 層次清晰）
- **段落精確度 (Passage Precision)**：AI 能否從任一段落獨立提取完整答案

### 3. E-E-A-T 信號強度

- **經驗 (Experience)**：第一人稱案例、實驗數據、試用報告
- **專業 (Expertise)**：作者實體可追溯（LinkedIn、ORCID）、Person Schema
- **權威 (Authoritativeness)**：第三方背書、產業評測收錄
- **信任 (Trustworthiness)**：更新時間戳記、聯絡資訊、隱私政策

### 4. 傳統 SEO 基礎健康度

- Title Tag：含目標關鍵字、60 字元內
- Meta Description：精準摘要、155 字元內
- URL 結構乾淨、含關鍵字
- 圖片 Alt Text 描述性
- 內部連結架構合理
- Core Web Vitals（LCP < 2.5s、CLS < 0.1）

### 5. 對話意圖覆蓋度

- 能否回答長尾對話式查詢（10-23 字的複雜問題）
- 是否預測後續追問（子查詢拆解）
- 是否覆蓋四維度：分類查詢、問題解決、比較分析、品牌直接查詢

### 6. 多模態就緒度

- 圖像 Alt Text 和 EXIF/IPTC 中介資料
- 圖像文字字體高度 > 30px、灰階對比度 > 40
- 影片字幕檔 (.vtt)、時間軸章節、VideoObject Schema

### 分析報告輸出格式

輸出以下結構化報告：

總分：__/60

評估維度與分數表：
- GEO 三大驅動因子：__/10
- 結構與機器可讀性：__/10
- E-E-A-T 信號強度：__/10
- 傳統 SEO 基礎：__/10
- 對話意圖覆蓋度：__/10
- 多模態就緒度：__/10

分級輸出：
- [紅] 急需改善（優先處理）
- [黃] 可強化項目
- [綠] 表現良好
- 具體優化行動清單（勾選框格式）

完整評分細則見 [references/geo-writing-guide.md](references/geo-writing-guide.md)。

---

## 模式 B：內容撰寫或改寫

### GEO 寫作八原則（嚴格遵守）

1. **倒金字塔開頭**：每段落前 50-75 字是直接解答，無修飾鋪陳
2. **統計數據錨定**：每 200-300 字至少 1 個帶來源的數據點
3. **專家語錄穿插**：每篇至少 1-2 則具名專家語錄（「據[機構][姓名][頭銜]指出：『...』」）
4. **權威引用標註**：關鍵事實附來源，優先學術論文/權威媒體/政府資料
5. **模組化問答結構**：精確的使用者提問作為 H2/H3 子標題
6. **去除語言雜訊**：禁止「眾所周知」「隨著科技發展」等空泛語句
7. **對話意圖預測**：結尾預設 3-5 個常見追問並提供解答
8. **資訊增益優先**：至少 1 項原創數據/獨家觀點/第一手經驗

### 輸出結構模板

```markdown
# [精準回答使用者核心問題的標題]

[50-75 字的直接宣告式解答，含 1 個關鍵數據點]

## [使用者可能的提問 1]？

[直接解答 + 統計數據 + 來源]

> 據 [機構] [姓名]（[頭銜]）指出：「...」

[補充細節，項目符號條列]

## [使用者可能的提問 2]？

...

## 常見追問

### Q1: ...
A1: ...

### Q2: ...
A2: ...
```

### YMYL 領域特殊規範

若內容屬於醫療、金融、法律、政府等 YMYL 領域，額外強制要求：
- 所有主張附同行審查或官方來源
- 專業資格聲明（學歷、證照、執業年資）
- 免責聲明
- 引用時間戳記 12 個月以內
- 附結構化作者資訊（Person Schema）

詳細寫作範例與案例對照見 [references/geo-writing-guide.md](references/geo-writing-guide.md)。

---

## 模式 C：技術實作

三大技術產出物，完整模板見 [references/schema-templates.md](references/schema-templates.md)。

### C1: llms.txt 生成器

放置於網站根目錄 ，純 Markdown 格式。核心結構：
- 品牌名稱 + 一句話核心定位
- 結果導向描述（非功能列表）
- 5-10 個最具商業價值的核心頁面
- 常見問題簡答
- 聯絡資訊

注意：描述聚焦結果導向、複雜頁面同步生成 Markdown 鏡像、與 CMS 綁定確保自動更新。

### C2: Schema JSON-LD 生成器

四大 GEO 必備 Schema 類型：
- **Organization** — 品牌實體 + sameAs 跨平台連結
- **Person** — 作者標記 + 專業資格證明
- **FAQPage** — 結構化問答
- **Article** — 文章後設資料 + 發佈/修改時間

### C3: Markdown 鏡像策略

對複雜頁面（定價表、產品規格、對比表）生成純文字 Markdown 鏡像，消除 AI 解析 HTML 表格的誤判風險。

### C4: llms-full.txt 進階版

`llms.txt` 為精簡摘要版；`llms-full.txt` 為完整版，包含所有頁面的詳盡 Markdown 內容。兩者搭配使用：

| 檔案 | 用途 | 長度 | 放置位置 |
|------|------|------|----------|
| `llms.txt` | AI 引擎快速理解品牌概覽 | 500-2000 字 | `/llms.txt` |
| `llms-full.txt` | AI 引擎深度檢索完整內容 | 不限 | `/llms-full.txt` |

`llms-full.txt` 建議包含：完整產品文件、API 參考、定價詳情、所有部落格文章摘要。適合內容量大且希望 AI 引擎全面索引的網站。

### C5: AI 爬蟲管理（robots.txt）

主要 AI 爬蟲及其對應 User-Agent：

| AI 引擎 | User-Agent | 用途 |
|---------|------------|------|
| OpenAI (ChatGPT) | `GPTBot` | 訓練 + 搜尋 |
| OpenAI (搜尋) | `ChatGPT-User` | 即時搜尋瀏覽 |
| Google AI | `Google-Extended` | Gemini 訓練 |
| Anthropic | `ClaudeBot` | Claude 訓練 |
| Meta | `FacebookBot` | Meta AI 訓練 |
| Perplexity | `PerplexityBot` | 即時搜尋 |
| Common Crawl | `CCBot` | 開源訓練資料 |

**建議策略**：允許搜尋型爬蟲（ChatGPT-User、PerplexityBot）以獲得 AI 引用，選擇性封鎖訓練型爬蟲以保護內容IP。完整 robots.txt 模板見 [references/schema-templates.md](references/schema-templates.md)。

---

## 模式 D：策略規劃

### D1: SEO/GEO 混合策略框架

六大策略模塊，詳見 [references/strategy-framework.md](references/strategy-framework.md)：

1. **現狀診斷** — SEO 健康度 + AI 能見度基準線 + 競爭者分析
2. **內容工程改造** — 核心頁面 GEO 改造優先序 + 系統性嵌入計畫
3. **技術架構升級** — llms.txt / llms-full.txt + Schema + Markdown 鏡像 + AI 爬蟲管理 + 渲染障礙排除
4. **知識圖譜建構 (KGO)** — NAP 一致性 + Wikidata + 數位公關 + 品牌共現
5. **多模態搜尋布局** — 圖像 AI 可讀性 + 影片 AI 解析規範
6. **內容衰退偵測** — 衰退信號偵測 + 更新優先序 + 季度稽核流程 + 常青內容策略
7. **KPI 與追蹤體系** — AIGVR + SOV + 情感監控 + 轉換追蹤

### D2: 提示詞矩陣（Prompt Matrix）

協助用戶建立 20-30 個追蹤提示詞，涵蓋四大維度：

| 維度 | 範例格式 |
|------|----------|
| 分類查詢 | 「最佳 [產品類別] 推薦 [年份]」 |
| 問題解決 | 「如何解決 [特定問題]」 |
| 比較分析 | 「[品牌A] vs [品牌B] 比較」 |
| 品牌直接查詢 | 「[品牌名稱] 評價/優缺點」 |

### D3: GEO 工具選型建議

| 企業規模 | 推薦工具 | 特色 |
|----------|----------|------|
| 大型（隱私優先） | Atomic AGI | AI 優先歸因，GDPR 合規 |
| 大型（數據深度） | Profound AI | 對話探索器，SOC 2 Type II |
| 中小品牌 | Peec AI | 多引擎追蹤，每四小時更新 |
| SEO 團隊延伸 | Ahrefs Brand Radar | 整合 Ahrefs 生態系 |
| 行銷主管 | SE Visible | 直觀圖表，品牌聲譽預警 |

---

## 關鍵數據速查表

撰寫或分析時可直接引用的核心研究數據：

| 數據點 | 數值 | 來源 |
|--------|------|------|
| 美國 Google 零點擊搜尋比例 | 58.5% | SparkToro / Datos, 2024 |
| 被 AI 引用但不在 Google 首頁的來源 | 80% | Authoritas AI Search Study, 2024 |
| 統計數據嵌入提升 AI 引用率 | +33.9% | Aggarwal et al., GEO-bench, Princeton, 2023 |
| 專家語錄嵌入提升 AI 引用率 | +32% | Aggarwal et al., GEO-bench, Princeton, 2023 |
| 權威引用提升 AI 引用率 | +30.3% | Aggarwal et al., GEO-bench, Princeton, 2023 |
| AI 平台平均查詢長度 | 10-23 字 | Authoritas AI Query Analysis, 2024 |
| AI 搜尋工作階段平均時長 | 6 分鐘 | SparkToro AI Search Behavior Report, 2024 |
| 品牌提及與 AI 可見度相關性 | 0.664 | Profound AI Brand Visibility Study, 2024 |
| 反向連結與 AI 可見度相關性 | 0.218 | Profound AI Brand Visibility Study, 2024 |
| AI 流量轉換率 vs 傳統自然搜尋 | 4.4 倍 | Ahrefs AI Traffic Conversion Report, 2024 |
| Wikipedia 頁面對 AI 引用率提升 | 180% | Profound AI Knowledge Graph Study, 2024 |
| B2B 採購受 AI 答案影響比例 | 82% | Gartner B2B Buying Survey, 2024 |
| Google Lens 月視覺查詢量 | 200 億次 | Google I/O 2024 Keynote |
| 傳統搜尋引擎查詢預估衰退（至 2026） | -25% | Gartner Search Forecast, 2024 |

---

## 回應語言

- 預設使用繁體中文回應
- 若用戶使用英文提問，以英文回應
- 技術術語保留英文原文並附中文翻譯

## 參考文件

- [GEO 寫作指南與分析細則](references/geo-writing-guide.md) — 完整寫作規範、評分細則、案例對照
- [Schema JSON-LD 完整模板](references/schema-templates.md) — 六大 Schema 類型完整模板 + llms.txt 進階範例 + AI 爬蟲 robots.txt 模板
- [策略規劃框架與 KPI 體系](references/strategy-framework.md) — 六大策略模塊展開 + KGO + 內容衰退偵測 + 追蹤工具選型

## 相關插件

- **health-education-writer** — 醫療教育內容撰寫時，搭配本 skill 的模式 B（YMYL 寫作規範）可強化 E-E-A-T
- **quickstart-doc-writer** — 技術文件產出後，可用本 skill 的模式 A 分析 GEO 友善度
- **medical-content-team** — 醫療內容團隊審查流程中，可整合本 skill 的六維度評分作為品質檢查點
