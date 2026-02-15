# 醫學內容創作團隊討論啟動

啟動 Agent Teams 協作式醫學內容創作流程。

**題目**：$ARGUMENTS

---

## 執行指引

你是「主持人（Facilitator）」，擔任本次討論的 **Team Lead**。請嚴格按照以下步驟執行。

### Phase 1：準備工作

1. **解析題目**：從 `$ARGUMENTS` 取得討論題目。如果為空，請使用 AskUserQuestion 詢問題目。
2. **建立輸出目錄**：
   ```
   mkdir -p record/$ARGUMENTS/作品
   mkdir -p record/$ARGUMENTS/作品/assets
   mkdir -p record/$ARGUMENTS/會議記錄
   ```
3. **建立團隊**：使用 TeamCreate 建立團隊，團隊名稱使用題目的簡短英文代稱（例如「糖尿病預防」→ `med-diabetes-prevention`）
4. **建立 PRD**：在 `record/$ARGUMENTS/會議記錄/PRD.md` 寫入內容需求文件，包含：
   - 題目名稱
   - 目標讀者：醫療同業（醫師/藥師/護理師）及關注健康的高知識份子
   - 內容基調：專業 KOL 分析文風格（參照 prompt.md）
   - 字數目標（800-1600字）
   - 寫作風格規範：遵循 prompt.md 的硬性規則和輸出結構（A-F）
   - 格式要求：Facebook 貼文友善，不使用 markdown 語法
   - 多媒體轉換考量

### Phase 2：建立任務清單

使用 TaskCreate 建立以下 15 個任務，並用 TaskUpdate 設定依賴關係（addBlockedBy）：

| # | 任務 | 負責人 | blockedBy |
|---|------|--------|-----------|
| 1 | [Round 0] 初稿撰寫：研究主題並撰寫 800-1200 字散文敘事初稿 | medical-journalist | — |
| 2 | [Round 1] 科學審查：審查初稿的醫學準確性、證據來源、統計數據 | science-gatekeeper | 1 |
| 3 | [Round 1] 易讀性審查：評估初稿的親民度、朗讀友善度、術語易懂度 | patient-advocate | 1 |
| 4 | [Round 1] 批判審查：質疑初稿的假設、偏見、邏輯漏洞、平衡性 | devil-advocate | 1 |
| 5 | [Round 1] 傳播力審查：評估標題吸引力、開頭鉤子、分享動機、視覺潛力 | traffic-hunter | 1 |
| 6 | [Round 1] 綜合裁決：整合所有審查結果，撰寫 round1.md，確定改善方向 | facilitator (lead) | 2,3,4,5 |
| 7 | [Round 2] 深度改寫：根據 Round 1 反饋進行實質性改寫 | medical-journalist | 6 |
| 8 | [Round 2] 科學複審：審查修改後的醫學準確性 | science-gatekeeper | 7 |
| 9 | [Round 2] 易讀性複審：審查修改後的易讀性和朗讀友善度 | patient-advocate | 7 |
| 10 | [Round 2] 批判複審：審查修改後的客觀平衡性 | devil-advocate | 7 |
| 11 | [Round 2] 傳播力複審：審查修改後的傳播潛力 | traffic-hunter | 7 |
| 12 | [Round 2] 綜合裁決：整合所有複審結果，撰寫 round2.md | facilitator (lead) | 8,9,10,11 |
| 13 | [Round 3] 最終優化與平衡：流量獵人主導包裝優化 + 醫學記者配合調整 | medical-journalist + traffic-hunter | 12 |
| 14 | [Round 4] 最終審定：全員最終審查，產出 final.md | all | 13 |
| 15 | [Post-R4] 圖表擷取：從參考論文系統性擷取文章引用的關鍵圖表，建立 asset_manifest.md | medical-journalist | 14 |

### Phase 3：Spawn Teammates

使用 Task tool 啟動 5 個 teammate，全部使用 `model: opus`。每個 teammate 的 prompt 必須包含：

#### Teammate 1：醫學記者 (medical-journalist)
```
spawn 參數：
- name: "medical-journalist"
- subagent_type: "medical_journalist_agent"
- team_name: [團隊名稱]
- model: opus

prompt 要點：
- 你是醫學記者，負責撰寫和修改文章
- 題目：$ARGUMENTS
- 輸出目錄：record/$ARGUMENTS/作品/
- 會議記錄目錄：record/$ARGUMENTS/會議記錄/
- **寫作風格**：必須先讀取 prompt.md，嚴格遵循其中的風格規範和輸出結構（A標題→B開場→C舊觀念拆解→D臨床衝擊→E受惠族群→F收尾）
- **格式要求**：不使用 markdown 語法，使用 Facebook 貼文友善的編排格式
- **圖表擷取**：研究時順帶擷取重要圖表到 record/$ARGUMENTS/作品/assets/
- 讀取 medical_journalist_agent.md 中的「圖表擷取指引」了解詳細方法
- 請先查看 TaskList 認領你的任務
- 完成任務後用 TaskUpdate 標記完成，然後查看 TaskList 找下一個任務
- 與其他 teammate 溝通使用 SendMessage
- 讀取 .claude/agents/medical_journalist_agent.md 了解你的完整角色定義
```

#### Teammate 2：科學守門人 (science-gatekeeper)
```
spawn 參數：
- name: "science-gatekeeper"
- subagent_type: "science_gatekeeper_agent"
- team_name: [團隊名稱]
- model: opus

prompt 要點：
- 你是科學守門人，負責審查醫學準確性
- 題目：$ARGUMENTS
- 請先查看 TaskList 認領你的任務
- 審查初稿時，閱讀 record/$ARGUMENTS/作品/draft_v0.md
- 完成審查後 message 主持人（facilitator）和醫學記者（medical-journalist）
- 讀取 .claude/agents/science_gatekeeper_agent.md 了解你的完整角色定義
```

#### Teammate 3：病患代言人 (patient-advocate)
```
spawn 參數：
- name: "patient-advocate"
- subagent_type: "patient_advocate_agent"
- team_name: [團隊名稱]
- model: opus

prompt 要點：
- 你是病患代言人，負責確保內容親民易懂
- 題目：$ARGUMENTS
- 請先查看 TaskList 認領你的任務
- 審查初稿時，閱讀 record/$ARGUMENTS/作品/draft_v0.md
- 完成審查後 message 主持人（facilitator）和醫學記者（medical-journalist）
- 主動與流量獵人（traffic-hunter）討論易讀性 vs 傳播力的平衡
- 讀取 .claude/agents/patient_advocate_agent.md 了解你的完整角色定義
```

#### Teammate 4：魔鬼代言人 (devil-advocate)
```
spawn 參數：
- name: "devil-advocate"
- subagent_type: "devil_advocate_agent"
- team_name: [團隊名稱]
- model: opus

prompt 要點：
- 你是魔鬼代言人，負責質疑和挑戰內容
- 題目：$ARGUMENTS
- 請先查看 TaskList 認領你的任務
- 審查初稿時，閱讀 record/$ARGUMENTS/作品/draft_v0.md
- 完成審查後 message 主持人（facilitator）和醫學記者（medical-journalist）
- 主動 message 科學守門人（science-gatekeeper）質疑其審查結論
- 讀取 .claude/agents/devil_advocate_agent.md 了解你的完整角色定義
```

#### Teammate 5：流量獵人 (traffic-hunter)
```
spawn 參數：
- name: "traffic-hunter"
- subagent_type: "traffic_hunter_agent"
- team_name: [團隊名稱]
- model: opus

prompt 要點：
- 你是流量獵人，負責優化內容傳播力
- 題目：$ARGUMENTS
- 請先查看 TaskList 認領你的任務
- 審查初稿時，閱讀 record/$ARGUMENTS/作品/draft_v0.md
- 完成審查後 message 主持人（facilitator）和醫學記者（medical-journalist）
- 主動與病患代言人（patient-advocate）討論傳播力 vs 易讀性的平衡
- 讀取 .claude/agents/traffic_hunter_agent.md 了解你的完整角色定義
```

### Phase 4：啟動 Delegate Mode

所有 teammate spawn 後，你（主持人/Team Lead）進入協調模式：

1. **監控任務進度**：定期查看 TaskList
2. **等待 Round 0 完成**：醫學記者完成初稿後，Round 1 的審查任務會自動解除阻塞
3. **Round 1 審查期間**：
   - 4 個審查 teammate 平行工作，互相可見彼此的審查結果
   - 鼓勵 teammate 之間互相溝通（科學守門人 vs 魔鬼代言人辯論）
   - 等待所有審查完成
4. **綜合裁決**：
   - 讀取所有 teammate 的審查結果
   - 撰寫 `會議記錄/round1.md`
   - 更新 `會議記錄/decision_log.md`
   - 使用 TaskUpdate 完成 Task 6，解除 Task 7 的阻塞
5. **重複 Round 2-4**：按相同模式推進

### 通訊規則

**Round 1 審查期間的互動規則**：
- 科學守門人完成審查後，message 主持人和醫學記者報告關鍵發現
- 魔鬼代言人可以直接 message 科學守門人，質疑其審查結論
- 病患代言人可以 message 流量獵人，討論易讀性 vs 傳播力的平衡
- 所有審查結果由主持人整合到 round1.md
- 主持人等待所有審查完成後，綜合出會議記錄

**Round 2 改寫期間的互動規則**：
- 醫學記者根據 round1.md 的綜合裁決進行改寫
- 改寫完成後通知所有 teammate 進行複審
- 複審期間同樣允許 teammate 之間互相溝通

**Round 3-4 的互動規則**：
- Round 3 由流量獵人和醫學記者共同主導最終優化
- Round 4 全員參與最終審定，每人確認自己負責的品質面向

### 完成條件

當 Task 15（圖表擷取）完成後：
1. 確認 `record/$ARGUMENTS/作品/final.md` 已產出
2. 確認所有會議記錄已完整
3. 確認 `record/$ARGUMENTS/作品/assets/asset_manifest.md` 已建立
4. **歸檔原始素材**：將使用者提供的原始素材（論文 PDF、參考資料等）移動到 `record/$ARGUMENTS/作品/sources/` 目錄（先 mkdir -p 建立目錄，再 mv 移動檔案）
5. 向所有 teammate 發送 shutdown_request
6. 使用 TeamDelete 清理團隊
7. 向使用者報告完成狀態，提供 final.md 的位置

---

## 重要提醒

- **全部使用 Opus 模型**：確保最高品質
- **檔案衝突預防**：每個 teammate 只操作自己負責的檔案
- **散文敘事風格**：所有內容必須採用 4.0 版散文敘事風格
- **避免虛構案例**：使用情境描述取代具體人物故事
- **參考 workflow.md**：詳細流程規範請參閱 workflow.md 5.0 版
