# Schema JSON-LD 完整模板與 llms.txt 進階範例

本文件提供 seo-geo-optimizer skill 模式 C（技術實作）的完整模板。

## 一、Organization Schema

品牌實體標記，建立品牌在知識圖譜中的存在感。`sameAs` 欄位對 AI 引擎建立品牌實體至關重要。

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[品牌正式名稱]",
  "alternateName": "[品牌簡稱或別名]",
  "url": "[官方網站 URL]",
  "logo": "[Logo 圖片 URL（建議 112x112px 以上）]",
  "description": "[2-3 句結果導向描述]",
  "foundingDate": "[YYYY-MM-DD]",
  "sameAs": [
    "[Wikipedia URL — 最優先，AI 引用率提升 180%]",
    "[Wikidata URL — 知識圖譜核心]",
    "[LinkedIn 公司頁面 URL]",
    "[Crunchbase URL]",
    "[Twitter/X URL]",
    "[Facebook URL]",
    "[YouTube 頻道 URL]",
    "[GitHub URL（如適用）]"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[+886-X-XXXX-XXXX]",
    "contactType": "customer service",
    "availableLanguage": ["zh-TW", "en"]
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[街道地址]",
    "addressLocality": "[城市]",
    "addressRegion": "[縣市]",
    "postalCode": "[郵遞區號]",
    "addressCountry": "TW"
  }
}
```

**重點注意事項**：
- `sameAs` 至少填入 3 個以上跨平台連結
- Wikipedia/Wikidata 條目對 AI 能見度影響最大（相關性 0.664）
- `description` 使用結果導向語句，而非功能列表
- 若有多個品牌，使用 `parentOrganization` / `subOrganization` 建立關聯

---

## 二、Person Schema（作者標記）

為每篇內容的作者建立可追溯的專業身份。這是 E-E-A-T 中「Expertise」的技術實現。

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "[作者全名]",
  "jobTitle": "[現任職稱]",
  "worksFor": {
    "@type": "Organization",
    "name": "[所屬機構名稱]",
    "url": "[機構官網 URL]"
  },
  "alumniOf": {
    "@type": "EducationalOrganization",
    "name": "[畢業學校]"
  },
  "description": "[1-2 句專業背景描述，含執業年資]",
  "sameAs": [
    "[LinkedIn 個人檔案 URL]",
    "[ORCID URL（學術作者）]",
    "[Google Scholar URL]",
    "[個人網站/部落格 URL]",
    "[Twitter/X URL]"
  ],
  "hasCredential": [
    {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "degree",
      "name": "[學位名稱，如 醫學博士]",
      "educationalLevel": "[PhD / Master / Bachelor]"
    },
    {
      "@type": "EducationalOccupationalCredential",
      "credentialCategory": "certification",
      "name": "[專業證照名稱]",
      "recognizedBy": {
        "@type": "Organization",
        "name": "[發照機構]"
      }
    }
  ],
  "knowsAbout": [
    "[專業領域 1]",
    "[專業領域 2]",
    "[專業領域 3]"
  ]
}
```

**YMYL 領域必填欄位**：
- `hasCredential`：醫療/金融/法律內容必須包含相關證照
- `alumniOf`：標示學歷背景
- `knowsAbout`：明確標示專業領域範圍

---

## 三、FAQPage Schema

將常見問答結構化，使 AI 引擎能直接提取問答對。

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[問題 1 — 使用自然語言提問形式]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[精簡直接的解答，50-100 字為佳。含關鍵數據點和來源。]"
      }
    },
    {
      "@type": "Question",
      "name": "[問題 2]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[解答 2]"
      }
    },
    {
      "@type": "Question",
      "name": "[問題 3]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[解答 3]"
      }
    }
  ]
}
```

**FAQ 寫作原則**：
- 問題使用真實用戶會搜尋的自然語言（10-23 字）
- 答案首句即為直接解答（倒金字塔）
- 答案含至少 1 個數據點
- 建議 5-10 個 FAQ 項目
- 問題涵蓋四大意圖維度（分類、問題解決、比較、品牌）

---

## 四、Article Schema

文章後設資料標記，幫助 AI 引擎理解內容的時效性和權威性。

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[文章標題 — 60 字元以內]",
  "description": "[文章摘要 — 155 字元以內，倒金字塔式]",
  "author": {
    "@type": "Person",
    "name": "[作者姓名]",
    "url": "[作者個人頁面 URL]",
    "jobTitle": "[職稱]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[發佈機構名稱]",
    "logo": {
      "@type": "ImageObject",
      "url": "[Logo URL]",
      "width": 600,
      "height": 60
    }
  },
  "datePublished": "[ISO 8601 格式，如 2024-03-15T08:00:00+08:00]",
  "dateModified": "[ISO 8601 格式 — 必須隨內容更新而更新]",
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "[文章正式 URL]"
  },
  "image": {
    "@type": "ImageObject",
    "url": "[主圖 URL]",
    "width": 1200,
    "height": 630
  },
  "articleSection": "[分類/主題]",
  "keywords": ["關鍵字1", "關鍵字2", "關鍵字3"],
  "wordCount": 2500,
  "inLanguage": "zh-TW"
}
```

**時效性管理**：
- `dateModified` 必須在每次內容更新時同步更新
- YMYL 領域內容的 `dateModified` 與當前日期差距不應超過 12 個月
- 建議在頁面可見處也顯示「最後更新日期」

---

## 五、HowTo Schema

適用於步驟式教學內容，幫助 AI 引擎精確提取操作步驟。

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[如何完成某項任務的標題]",
  "description": "[1-2 句摘要說明此教學的目標成果]",
  "totalTime": "PT30M",
  "estimatedCost": {
    "@type": "MonetaryAmount",
    "currency": "TWD",
    "value": "0"
  },
  "supply": [
    {
      "@type": "HowToSupply",
      "name": "[所需材料/工具 1]"
    }
  ],
  "tool": [
    {
      "@type": "HowToTool",
      "name": "[所需工具 1]"
    }
  ],
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "[步驟 1 標題]",
      "text": "[步驟 1 詳細說明，50-100 字]",
      "image": "[步驟示意圖 URL（選填）]"
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "[步驟 2 標題]",
      "text": "[步驟 2 詳細說明]"
    },
    {
      "@type": "HowToStep",
      "position": 3,
      "name": "[步驟 3 標題]",
      "text": "[步驟 3 詳細說明]"
    }
  ]
}
```

**HowTo Schema 最佳實踐**：
- 每個步驟的 `text` 以動詞開頭（「打開」「點選」「輸入」）
- `totalTime` 使用 ISO 8601 Duration 格式（PT30M = 30 分鐘）
- 步驟數量建議 3-10 步，過多則拆分為多個 HowTo
- 搭配影片時可在步驟中加入 `video` 欄位指向對應時間軸

---

## 六、BreadcrumbList Schema

幫助 AI 引擎理解頁面在網站架構中的層級位置，提升段落定位精準度。

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "首頁",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[分類名稱]",
      "item": "https://example.com/category/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[當前頁面標題]",
      "item": "https://example.com/category/current-page/"
    }
  ]
}
```

**BreadcrumbList 最佳實踐**：
- 層級深度建議 2-4 層，與網站實際導覽結構一致
- `name` 使用簡潔標題（非完整頁面標題），利於 AI 理解層級
- 最後一個 `ListItem` 為當前頁面，`item` 為該頁面的正式 URL
- 每頁只放一組 BreadcrumbList，與頁面上可見的麵包屑一致

---

## 七、AI 爬蟲 robots.txt 管理模板

### 建議策略：允許搜尋、選擇性封鎖訓練

```
# ===== AI 搜尋爬蟲（建議允許 — 獲得 AI 引用的前提）=====
User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

# ===== AI 訓練爬蟲（依需求決定是否封鎖）=====
# 若希望被 ChatGPT/Gemini/Claude 引用，建議允許
# 若擔心內容被用於訓練，可選擇封鎖

# OpenAI 訓練爬蟲
User-agent: GPTBot
Allow: /
# Disallow: /  # 取消註解以封鎖訓練用途

# Google Gemini 訓練
User-agent: Google-Extended
Allow: /
# Disallow: /

# Anthropic Claude 訓練
User-agent: ClaudeBot
Allow: /
# Disallow: /

# Meta AI 訓練
User-agent: FacebookBot
Allow: /
# Disallow: /

# Common Crawl（開源訓練資料集）
User-agent: CCBot
Disallow: /

# ===== 傳統搜尋引擎（保持允許）=====
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# ===== 指向 llms.txt =====
# 在 robots.txt 末尾加入，幫助 AI 爬蟲發現品牌摘要
# Llms-Txt: https://example.com/llms.txt
```

### 決策矩陣

| 品牌目標 | GPTBot | Google-Extended | ClaudeBot | PerplexityBot | ChatGPT-User |
|---------|--------|-----------------|-----------|---------------|--------------|
| 最大 AI 能見度 | Allow | Allow | Allow | Allow | Allow |
| 保護內容 IP + 保留搜尋引用 | Disallow | Disallow | Disallow | Allow | Allow |
| 完全封鎖 AI | Disallow | Disallow | Disallow | Disallow | Disallow |

**重要提醒**：封鎖 AI 訓練爬蟲不等於封鎖 AI 搜尋引用。AI 引擎可能透過第三方引用（Wikipedia、產業報告）間接引用你的內容。最有效的 AI 能見度策略是允許爬取 + 優化內容結構。

---

## 八、llms.txt 進階範例

### 範例：SaaS 公司

```markdown
# CloudOps Pro

> 幫助中大型企業將雲端基礎設施成本降低 30-50% 的智慧成本管理平台

## 關於我們
CloudOps Pro 是台灣領先的雲端成本優化平台，已協助超過 200 家企業
節省累計 NT$15 億的雲端支出。支援 AWS、Azure、GCP 三大雲端平台，
提供即時成本異常偵測與自動化節費建議。

## 核心資源
- [定價方案](https://cloudopspro.tw/pricing): 三種方案，從新創到企業級
- [客戶案例](https://cloudopspro.tw/cases): 12 個產業的成功案例與 ROI 數據
- [雲端成本計算器](https://cloudopspro.tw/calculator): 免費估算潛在節費空間
- [API 文件](https://docs.cloudopspro.tw): RESTful API 完整技術文件
- [部落格](https://cloudopspro.tw/blog): 雲端成本管理最佳實踐與產業趨勢

## 常見問題
- 支援哪些雲端平台？: AWS、Azure、GCP，含多雲混合環境
- 整合需要多久？: 平均 15 分鐘完成 API 串接，即時開始分析
- 資料安全如何保障？: SOC 2 Type II 認證，資料不離開客戶環境
- 免費試用期多長？: 14 天全功能免費試用，無需信用卡

## 聯絡資訊
- 網站: https://cloudopspro.tw
- Email: hello@cloudopspro.tw
- 客服電話: +886-2-2345-6789
```

### llms.txt 最佳實踐

1. **檔案位置**：網站根目錄 `/llms.txt`
2. **格式**：純 Markdown，不含 HTML
3. **長度**：500-2000 字為佳
4. **更新頻率**：與 CMS 綁定，內容更新時自動重構
5. **核心頁面篩選**：僅列 5-10 個最具商業價值的頁面
6. **描述原則**：結果導向（「幫助企業降低 30% 成本」而非「提供成本管理功能」）
7. **鏡像策略**：對定價頁、規格表等複雜頁面，額外建立 `.md` 鏡像檔案（如 `pricing.md`）

### llms-full.txt 範例（完整版）

```markdown
# CloudOps Pro — 完整資訊

> 幫助中大型企業將雲端基礎設施成本降低 30-50% 的智慧成本管理平台

## 產品概覽
CloudOps Pro 是台灣領先的雲端成本優化平台，已協助超過 200 家企業
節省累計 NT$15 億的雲端支出。支援 AWS、Azure、GCP 三大雲端平台。

## 功能詳述

### 成本總覽儀表板
即時視覺化所有雲端帳號的支出分佈，支援多維度切片（服務、區域、
標籤、團隊）。儀表板每 5 分鐘自動刷新，異常支出自動標紅警示。

### 自動化節費引擎
基於 ML 模型分析歷史用量，自動產出三類節費建議：
1. 閒置資源回收（平均節省 15-20%）
2. 預留實例優化（平均節省 25-35%）
3. 資源規格調整（平均節省 10-15%）

### API 整合
RESTful API 支援所有平台功能，完整 OpenAPI 3.0 規格文件。
認證方式：Bearer Token（API Key）或 OAuth 2.0。
速率限制：每分鐘 1000 次請求（Enterprise 方案可調整）。

## 定價方案
| 方案 | 月費 | 管理上限 | 功能 |
|------|------|---------|------|
| Starter | NT$9,900 | NT$500萬/月 | 基礎監控 + 警報 |
| Professional | NT$29,900 | NT$5,000萬/月 | 全功能 + API |
| Enterprise | 客製報價 | 無上限 | 全功能 + SLA + SSO |

## 客戶案例摘要
- 台灣大型電商：年省 NT$2,400 萬（32% 降幅）
- 金融科技新創：3 個月回本，年省 NT$800 萬
- 製造業 ERP 遷雲：雲端支出降低 41%

## 技術規格
- 部署模式：SaaS（公有雲）或 On-Premise
- 資料加密：AES-256 + TLS 1.3
- 合規認證：SOC 2 Type II、ISO 27001
- SLA：99.9% 可用性（Enterprise）
```

### llms-full.txt 與 llms.txt 的差異

| 面向 | llms.txt | llms-full.txt |
|------|----------|---------------|
| 目的 | 品牌概覽，快速定位 | 深度內容，完整索引 |
| 長度 | 500-2000 字 | 不限（通常 5000-20000 字） |
| 更新頻率 | 品牌定位變動時 | 隨產品/內容更新 |
| 結構 | 精簡摘要 + 核心連結 | 完整功能說明 + 技術規格 + 案例 |

---

### Markdown 鏡像檔案範例（定價頁）

```markdown
# CloudOps Pro 定價方案

最後更新：2024-12-01

| 方案 | 月費 | 管理雲端支出上限 | 主要功能 |
|------|------|------------------|----------|
| Starter | NT$9,900/月 | NT$500萬/月 | 成本總覽、異常警報、基礎報表 |
| Professional | NT$29,900/月 | NT$5,000萬/月 | 全部 Starter + 自動化節費、API 存取、Slack 整合 |
| Enterprise | 客製報價 | 無上限 | 全部 Pro + 專屬客戶經理、SLA 保證、SSO |

## 所有方案皆包含
- 14 天免費試用
- AWS / Azure / GCP 支援
- 即時成本儀表板
- Email 技術支援

## 常見定價問題
- 可以按年付費嗎？: 年付享 8 折優惠
- 超過管理上限怎麼辦？: 自動升級建議，不中斷服務
- 有教育/非營利優惠嗎？: 提供 50% 折扣，請聯繫業務團隊
```
