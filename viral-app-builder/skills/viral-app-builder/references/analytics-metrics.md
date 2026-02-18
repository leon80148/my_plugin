# 分析指標與數據驅動框架

本文件提供 App 分析的方法論、指標框架、工具比較及實作指南。

---

## AARRR 海盜指標框架

### 五大階段

Acquisition -> Activation -> Retention -> Revenue -> Referral

### 各階段關鍵指標

| 階段 | 關鍵指標 | 計算方式 | 基準值 |
|------|---------|---------|--------|
| Acquisition | CAC | 行銷支出 / 新用戶數 | 依管道差異大 |
| Acquisition | 管道轉換率 | 註冊數 / 管道訪客數 | 2-5% organic |
| Activation | 啟動率 | 完成關鍵動作 / 註冊 | 20-40% |
| Activation | Time to Value | 註冊到首個價值行動 | < 5 分鐘 |
| Retention | D1/D7/D30 | 第N天回訪 / 新用戶 | D1:25-40% D7:15-25% D30:8-15% |
| Retention | DAU/MAU | 日活/月活 | 20-25% 好 50%+ 優 |
| Revenue | ARPU | 總營收 / 活躍用戶 | 依模式 |
| Revenue | LTV | 用戶終身價值 | LTV > 3x CAC |
| Revenue | 付費轉換率 | 付費 / 活躍 | 2-5% freemium |
| Referral | K-factor | 邀請數 x 轉換率 | K>1 病毒成長 |
| Referral | NPS | 淨推薦分數 | 30+ 好 50+ 優 |

---

## North Star Metric

### 選擇條件

1. 反映用戶價值
2. 領先指標（比營收更早反映健康度）
3. 可拆解為團隊可操作的子指標

### 各類 App 的 NSM

| App 類型 | NSM | 原因 |
|---------|-----|------|
| 社群媒體 | 每日發布內容的用戶數 | 反映參與度 |
| 電商 | 每週購買的用戶數 | 核心價值 |
| SaaS | 每週活躍團隊數 | 黏著度 |
| 內容平台 | 每日消費時間 | 內容品質 |
| 健康 App | 每週完成目標用戶數 | 用戶受益 |
| 通訊 | 每日訊息數 | 使用頻率 |
| 遊戲 | 每日遊戲時長 | 趣味性 |
| 教育 | 每週完成課程學員數 | 學習成效 |

---

## 分析工具比較

| 工具 | 免費方案 | 適合階段 | 強項 | 弱項 |
|------|---------|---------|------|------|
| Mixpanel | 20M events/月 | 成長期 | 漏斗、Cohort | 定價高 |
| Amplitude | 50M events/月 | 成長期 | 路徑分析 | 學習曲線 |
| PostHog | 1M events/月 | 早期-成長 | 開源、Feature Flag | 維護成本 |
| GA4 | 免費 | 所有階段 | 流量、Google 整合 | 行為分析弱 |
| Plausible | 付費 | 早期 | 隱私友好 | 功能簡單 |
| June.so | 1000 MAU | 早期 B2B | B2B 專用 | 只適 B2B |

### 選擇建議

- MVP 低預算: GA4 + 自建事件
- MVP 有預算: PostHog Cloud
- 成長 B2C: Mixpanel 或 Amplitude
- 成長 B2B: June.so 或 Amplitude
- 重視隱私: PostHog 自建
- 規模化: Amplitude + 資料倉儲

---

## A/B 測試框架

### 流程

假設 -> 設計 -> 實驗 -> 分析 -> 決策

### 最小樣本數估算

| 轉換率 | 最小改善 | 每組樣本 |
|-------|---------|--------|
| 2% | 0.5% | ~6,000 |
| 5% | 1% | ~1,825 |
| 10% | 2% | ~865 |
| 20% | 3% | ~683 |
| 50% | 5% | ~384 |

### 工具

| 工具 | 類型 | 適合 | 定價 |
|------|------|------|------|
| PostHog | 開源/托管 | 全端 | 免費-付費 |
| LaunchDarkly | Feature Flag | 企業 | 付費 |
| Firebase Remote Config | 行動端 | App | 免費 |
| Statsig | 全端 | 成長團隊 | Free-付費 |
| GrowthBook | 開源 | 自建 | 免費-付費 |

### 常見陷阱

| 陷阱 | 問題 | 解決 |
|------|------|------|
| 偷看 | 假陽性 | 預設結束條件 |
| 多重比較 | alpha 膨脹 | Bonferroni 校正 |
| 辛普森悖論 | 子群不同 | 分層分析 |
| 新奇效應 | 改動吸引注意 | 延長至 2+ 週 |
| 倖存者偏差 | 只看完成者 | Intent-to-Treat |

---

## Dashboard 設計

### 執行摘要 Dashboard

上方：4 個 KPI 卡片（DAU、新用戶、營收、NPS）含週變化
中左：Retention Curve（D1/D7/D30）
中右：Conversion Funnel
下方：Top Events 排行

### 事件命名規範

| 類型 | 規範 | 範例 |
|------|------|------|
| 頁面瀏覽 | page_view | page_view {page:home} |
| 點擊 | {object}_{action} | signup_button_clicked |
| 功能 | feature_{name}_{action} | feature_search_used |
| 交易 | {action}_{object} | purchase_completed |
| 錯誤 | error_{category} | error_payment_failed |

### 追蹤計劃模板

每個追蹤計劃包含：
1. 核心事件表（名稱、觸發時機、屬性、AARRR 階段）
2. 用戶屬性表（屬性、類型、更新時機、用途）
3. Dashboard 列表（名稱、受眾、頻率、指標）
