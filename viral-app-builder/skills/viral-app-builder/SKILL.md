---
name: viral-app-builder
description: |
  跨平台爆款 App 全生命週期開發助手。涵蓋從創意發想、市場驗證、MVP規劃、UI/UX設計、
  程式開發、測試迭代、成長黑客策略、營利模式到規模擴展的完整產品開發流程。
  新增 AI 原生應用開發、隱私合規、技術選型比較、數據分析框架等現代開發模式。

  觸發時機：
  (1) 用戶想要開發新的 App 或數位產品
  (2) 需要腦暴創業點子或驗證商業概念
  (3) 規劃 MVP 功能清單或產品路線圖
  (4) 設計用戶體驗、遊戲化機制或留存策略
  (5) 制定成長黑客策略或病毒式傳播機制
  (6) 選擇營利模式（訂閱、廣告、內購、Freemium）
  (7) 規劃技術架構擴展或團隊協作流程
  (8) 開發 AI 原生應用（LLM 整合、RAG 系統、AI Agent）
  (9) 處理隱私合規（GDPR、個資法、App Store 規範）
  (10) 技術選型比較（跨平台框架、後端服務、AI 服務）
  (11) 建立數據分析與指標追蹤框架

  觸發詞：App開發、創業點子、MVP、產品規劃、成長黑客、營利模式、用戶成長、
  病毒傳播、留存策略、訂閱制、跨平台開發、React Native、Flutter、
  AI 應用、LLM 整合、RAG 系統、ChatGPT、Claude API、AI Agent、
  隱私合規、GDPR、個資法、資料保護、技術選型、框架比較、
  數據分析、Analytics、A/B Testing、AARRR、留存指標
---

# 爆款 App 全生命週期開發助手

## 核心原則

1. **AI 輔助，人類主導**：Claude 提供創意和技術支援，但最終判斷由你做出
2. **快速驗證，迭代改進**：先用最小可行產品測試假設，再根據數據優化
3. **用戶為中心**：所有決策都應回歸用戶痛點和體驗

## 產品開發八階段

根據任務類型選擇對應階段的詳細指引：

| 階段 | 任務類型 | 參考文件 |
|------|----------|----------|
| 1. 創意發想 | 腦暴點子、市場驗證、競品分析 | [ideation.md](references/ideation.md) |
| 2. MVP 規劃 | 功能優先級、原型設計、驗證方法 | [mvp-planning.md](references/mvp-planning.md) |
| 3. UI/UX 設計 | Onboarding、遊戲化、習慣養成 | [ux-design.md](references/ux-design.md) |
| 4. 程式開發 | 跨平台開發、代碼審查、除錯 | [development.md](references/development.md) |
| 5. 測試迭代 | 自動化測試、用戶反饋分析 | [testing.md](references/testing.md) |
| 6. 成長黑客 | 病毒傳播、A/B測試、留存優化 | [growth.md](references/growth.md) |
| 7. 營利模式 | 訂閱、廣告、內購、定價策略 | [monetization.md](references/monetization.md) |
| 8. 規模擴展 | 架構擴容、DevOps、團隊協作 | [scaling.md](references/scaling.md) |
| 9. AI 整合 | LLM 選型、RAG 架構、成本優化 | [ai-native-patterns.md](references/ai-native-patterns.md) |
| 10. 隱私合規 | GDPR、App Store 規範、資料保護 | [privacy-compliance.md](references/privacy-compliance.md) |
| 11. 數據分析 | 指標框架、Analytics 工具、A/B Testing | [analytics-metrics.md](references/analytics-metrics.md) |
| 12. 技術選型 | 跨平台框架、後端服務、AI 服務比較 | [tech-stack-comparison.md](references/tech-stack-comparison.md) |

## 快速提示範本

### 創意發想
```
請列出10個 {領域} 中新近冒出的問題與解決方案，
格式：問題 : 解決方案 : 目標用戶
```

### MVP 功能規劃
```
我想開發一款 {產品描述} 的 App，
請用 MoSCoW 方法列出 MVP 功能：Must-have / Should-have / Could-have / Won't-have
```

### 成長策略
```
針對這款 {產品類型} App，請設計：
1. 病毒式傳播機制（用戶如何自然推薦）
2. 推薦獎勵計畫（雙邊激勵）
3. 提升留存的遊戲化元素
```

### 營利模式評估
```
對於 {產品類型}，請比較以下營利模式的優劣：
- 訂閱制 vs 一次性買斷
- 免費+廣告 vs Freemium
並給出推薦方案
```

### AI 原生應用開發
```
我要開發一款 {AI應用類型}，請分析：
1. LLM 選擇建議（GPT-4/Claude/Gemini/開源模型）
2. 架構設計（RAG vs Fine-tuning vs Prompt Engineering）
3. 成本估算（API 費用 + 基礎設施）
4. 用戶體驗設計（延遲處理、串流回應、錯誤處理）
```

### 隱私合規檢查
```
我的 App 會收集 {資料類型}，目標市場包含 {地區}，
請檢查：
1. 需要符合哪些隱私法規（GDPR/個資法/CCPA）
2. App Store 上架需要揭露哪些隱私標籤
3. 需要實作哪些使用者權利功能（刪除/匯出/同意管理）
```

### 技術選型決策
```
我要開發 {產品類型}，團隊背景是 {技術背景}，
請比較適合的技術棧：
1. 前端框架選擇與理由
2. 後端服務選擇與理由
3. 預估開發時間與成本
4. 長期維護考量
```

### 數據分析規劃
```
我的 {產品類型} 已上線，目前有 {用戶規模} 用戶，
請幫我規劃：
1. 應追蹤的核心指標（北極星指標 + 輔助指標）
2. Analytics 工具推薦
3. Dashboard 設計建議
4. 數據驅動的迭代流程
```

## 應用類別範例

本 Skill 適用於各類 App 開發，包括但不限於：
- **生產力工具**：專注計時器、待辦事項、筆記應用
- **AI 工具**：聊天機器人、AI 助手、智能分析
- **健康應用**：健身追蹤、習慣養成、心理健康
- **娛樂應用**：迷因生成器、社交遊戲、內容創作
- **社交應用**：交友配對、社群平台、即時通訊
- **AI 原生應用**：LLM 聊天機器人、RAG 知識庫、AI Agent 系統、AI 繪圖工具
- **Web3/區塊鏈**：DeFi 應用、NFT 平台、DAO 治理工具
- **No-code/Low-code**：自動化工具、表單建構器、網站建構器
- **IoT 伴侶應用**：智慧家居控制、穿戴裝置、健康監測

詳細案例請參考 [examples.md](references/examples.md)

## 快速導覽：新增模組

| 主題 | 適用情境 | 參考文件 |
|------|----------|----------|
| AI 原生開發 | 想整合 LLM/RAG/Agent 到產品中 | [ai-native-patterns.md](references/ai-native-patterns.md) |
| 隱私合規 | 上架前合規檢查、跨國資料處理 | [privacy-compliance.md](references/privacy-compliance.md) |
| 數據分析 | 建立指標體系、選擇 Analytics 工具 | [analytics-metrics.md](references/analytics-metrics.md) |
| 技術選型 | 跨平台框架比較、後端與 AI 服務選擇 | [tech-stack-comparison.md](references/tech-stack-comparison.md) |

---

## 故障排除

| 問題 | 可能原因 | 解決 |
|------|---------|------|
| 產出的 MVP 範圍太大 | 未嚴格遵循 MVF 原則 | 回到 ideation，重新定義核心功能環 |
| 技術選型分析過於發散 | 未設定預算 Tier | 先確認 Tier 1-4 再進行選型 |
| 成長策略缺乏可操作性 | 缺少具體指標 | 先定義 North Star Metric 再制定策略 |
| AI 整合架構不明確 | 未走完決策樹 | 從 ai-native-patterns.md 的決策樹開始 |
