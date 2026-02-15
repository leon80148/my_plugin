---
name: nhs-pportal-screening
description: "國健署預防保健篩檢資格查詢系統（pportal.hpa.gov.tw）的完整領域知識。包含登入流程、VoidAPI2 篩檢資格、GetBasicData 健保卡紀錄、agreeResult 代碼、以及健保IC卡 BhpNhi 整合方式。"
argument-hint: "[query-context]"
---

# 國健署預防保健篩檢資格查詢系統

## 系統概述

國健署（國民健康署，HPA）提供「預防保健服務資訊查詢」系統，供醫療院所查詢病患的各項篩檢資格。

### 三種資料來源

| 來源 | 方式 | 查詢範圍 | 需求 | 資料性質 |
|------|------|----------|------|----------|
| **Pportal VoidAPI2** | 瀏覽器登入 pportal.hpa.gov.tw | 全項目（10+ 項） | 帳號密碼 + 驗證碼 + 健保卡 | 即時篩檢資格判定 |
| **Pportal GetBasicData** | 同上（伴隨 VoidAPI2 自動觸發） | 健保卡歷史紀錄 | 同上 | 跨院歷史執行記錄 |
| **BhpNhi（健保IC卡）** | 本機 CLI 呼叫 BhpNetNhiEx.exe | 成健 + BC肝（2 項） | 健保IC卡讀卡機 + 控制軟體 | 即時資格判定 |

---

## 核心設計原則

以下原則適用於所有需要「嵌入外部 Web 系統並自動化操作」的場景，不限於國健署。

### 原則 1：Session 重用 — 認證成本最小化

**問題**：外部系統的登入流程通常包含驗證碼、MFA 等人工介入步驟，每次查詢都重新登入會嚴重影響效率。

**策略**：將「已認證的瀏覽器環境」視為可重用資源，查詢入口依存活狀態分層處理：

```
查詢請求進入
  │
  ├── 層級 1（最快）：操作頁面仍在 → 直接在頁面上觸發動作
  ├── 層級 2（次快）：主視窗仍在 → 從主視窗導航到操作頁面
  └── 層級 3（最慢）：都不在    → 重建視窗 → 偵測 Cookie 是否有效
      ├── Cookie 有效 → 跳過登入，直接導航
      └── Cookie 過期 → 完整登入流程
```

**關鍵規則**：
- 每一層都要做 `isDestroyed()` 檢查，視窗可能被使用者手動關閉
- Cookie 持久化（Electron `persist:xxx` / Puppeteer userDataDir）是層級 3 的基礎
- 查詢前要重置暫態資料（如換卡查詢要清除上一張卡的快取），避免資料錯配

### 原則 2：多視窗生命週期管理

**問題**：外部系統常用 `window.open` 開子視窗，若不追蹤引用，無法重用也無法正確清理。

**策略**：
- **建立時保存引用**：`did-create-window` / `window.open` handler 中立即保存
- **關閉時清空引用**：監聽 `closed` 事件，設為 null
- **銷毀時清理資源**：detach debugger、取消計時器、釋放攔截器
- **統一清理入口**：提供 `close()` 方法，由外到內（子視窗 → 主視窗）依序清理

**防禦性檢查模式**：
```javascript
if (this._window && !this._window.isDestroyed()) {
  // 安全操作
}
```

### 原則 3：DOM 偵測用 Polling，不用導航事件

**問題**：SPA / 同頁 Modal / ASP.NET Partial PostBack 不會觸發頁面導航事件（`did-navigate`），無法用傳統方式偵測 UI 狀態變化。

**策略**：
- 使用 `setInterval` + `executeJavaScript` 定期掃描 DOM
- 每個 polling 都要設 **maxAttempts 上限**，避免永久輪詢
- 偵測成功後立即 `clearInterval`
- 用 **flag 變數**（如 `_autoFillDone`）防止重複執行

**適用場景**：
- 登入 Modal 出現偵測
- 登入後頁面狀態變化偵測
- 使用者手動輸入完成偵測（如驗證碼）

### 原則 4：表單填入 — 模擬真實使用者輸入

**問題**：ASP.NET WebForms 的 `__doPostBack` 和各種 JS 框架依賴 DOM 事件鏈（focus → input → change），直接設定 `.value` 不會觸發這些事件。

**策略**（按可靠度排序）：
1. **Electron `insertText()`**：最可靠，模擬 OS 層鍵盤輸入
2. **Puppeteer/Playwright `page.type()`**：逐字輸入，觸發完整事件鏈
3. **手動 dispatch 事件**：設 `.value` 後 dispatch `input` + `change` 事件
4. **直接設 `.value`**：最不可靠，許多框架不會接受

**填入前必做**：focus → select（清除舊值）→ 再輸入

### 原則 5：按鈕/元素匹配 — 精確優先

**問題**：同一頁面可能有多個文字相似的按鈕（如「登入」、「服務登入」、「一般登入」），模糊匹配會點錯。

**策略**（按優先度）：
1. **ID 精確匹配**：`document.querySelector('#ctl00_lbtnLogin')`
2. **Placeholder 精確匹配**：`input.placeholder === '請輸入帳號'`
3. **文字精確匹配**：`text === '實體卡查詢'`（用 `===` 不用 `includes`）
4. **文字包含匹配**：`text.includes('篩檢資格查詢')`（僅限無歧義時）
5. **DOM 順序遍歷**：`querySelectorAll` 逐一比對，找到第一個符合的

**避免**：
- `input[type="password"]`（可能匹配到變更密碼欄位）
- `text.includes('登入')`（會匹配到多個 tab 和按鈕）

### 原則 6：XHR 攔截 — 攔截 Response Body

**問題**：瀏覽器 `webRequest` API 只能取得 headers，無法取得 response body。自動化場景需要讀取 API 回傳的完整 JSON。

**策略**：
- **Electron**：attach Chrome DevTools Protocol → `Network.enable` → 監聯 `Network.responseReceived` → `Network.getResponseBody`
- **Puppeteer/Playwright**：`page.on('response', r => r.json())`
- **子視窗也要攔截**：`did-create-window` 事件中對新視窗重複設定

**過濾原則**：只攔截目標 XHR（用 URL pattern + type 過濾），忽略靜態資源，避免效能影響。

### 原則 7：登入狀態偵測 — 頁面語義推斷

**問題**：外部系統通常沒有公開的「是否已登入」API，需從頁面 DOM 推斷。

**策略**：偵測「僅登入後才會出現的 UI 元素」，常見指標：
- **登出按鈕/連結**：出現「登出」文字 → 已登入
- **功能入口連結**：出現「篩檢資格查詢」等需登入才可見的連結 → 已登入
- **使用者名稱顯示**：頁面顯示帳號或姓名 → 已登入

**注意**：偵測需延遲執行（如 500ms），等待動態內容渲染完成。

---

## Pportal 系統（Web Portal）

### URL 與頁面結構

- **首頁**: `https://pportal.hpa.gov.tw/Web/Notice.aspx`
- **技術框架**: ASP.NET WebForms
- **登入方式**: 首頁的「服務登入」按鈕 → 同頁 Modal（非新頁面）
- **所有 AJAX 回傳**: 包裹在 ASP.NET `{"d": ...}` 格式中

### 登入 Modal DOM 結構

登入 modal 是 ASP.NET 的同頁面彈出框，有以下關鍵元素：

#### Tab 切換
- **「一般登入」tab** → 切換到 `#tab1`
- **「服務登入」tab** → 切換到 `#tab2`（帳號密碼登入在此）
- **「憑證登入」tab** → 切換到 `#tab3`

#### 表單欄位

| 用途 | ID | Placeholder | type |
|------|-----|------------|------|
| 帳號 | `ctl00_txtAccount` | `請輸入帳號` | text |
| 密碼 | `ctl00_txtPassword` | `請輸入密碼` | password |
| 驗證碼 | `ctl00_txtCaptcha` (推測) | 含「驗證碼」 | text |
| 登入按鈕 | `ctl00_lbtnLogin` | — | submit/anchor |

#### 危險的相似欄位（必須避免匹配到）

| 欄位 | ID | Placeholder | 說明 |
|------|-----|------------|------|
| 變更密碼-舊密碼 | `ctl00_txt_OldPswd` | `請輸入您目前密碼` | `input[type="password"]` 會先匹配到此欄位 |
| 變更密碼-新帳號 | `ctl00_txt_NewPAccount` | `請輸入帳號` | 在 DOM 中可能比 `txtAccount` 更早出現 |
| 顯示密碼核取框 | `ctl00_chkShowPassword` | — | `input[name*="Password"]` 會匹配到 |

### 登入後流程

1. 登入成功 → 頁面導向篩檢查詢頁
2. 查詢操作在**子視窗**中開啟（`window.open`）
3. 子視窗中使用者點擊「實體卡查詢」或「虛擬卡查詢」
4. 系統讀取健保卡後，依序觸發多個 XHR

---

## Screening.aspx XHR 端點總覽

查詢觸發後，子視窗會依序發出以下 XHR 請求：

### 呼叫時序

```
使用者點擊「查詢」（實體卡/虛擬卡）
  │
  ├── 1. GetHospData        → 取得醫院名稱
  ├── 2. CheckAccount        → 驗證登入帳號
  ├── 3. GetNoticeToSync     → 同步公告資訊
  │
  ├── 4. GetBasicData ★      → 健保卡基本資料 + 歷史紀錄（PreventDatas）
  ├── 5. WriteInputLog       → 寫入查詢紀錄
  │
  └── 6. VoidAPI2 ★          → 篩檢資格判定結果（agreeResult）
```

**重點**: GetBasicData **先於** VoidAPI2 回傳。攔截時需先暫存 GetBasicData，待 VoidAPI2 回傳時合併送出。

### 端點明細

| 端點 | 用途 | 回傳範例 | 是否需攔截 |
|------|------|----------|-----------|
| `GetHospData` | 醫院名稱 | `{"d": "安家診所"}` | 否 |
| `CheckAccount` | 驗證帳號 | `{"d": {"PersonSNO": "168195", "PAccount": "anchia"}}` | 否 |
| `GetNoticeToSync` | 公告同步 | `{"d": [{...}]}` | 否 |
| **`GetBasicData`** | **健保卡紀錄** | **見下方** | **是** |
| `WriteInputLog` | 寫入查詢紀錄 | `{"d": "前台資料存檔成功"}` | 否 |
| **`VoidAPI2`** | **篩檢資格判定** | **見下方** | **是** |

---

## GetBasicData — 健保卡歷史紀錄 API

### 端點

```
POST https://pportal.hpa.gov.tw/Screening/Screening.aspx/GetBasicData
```

### 用途

讀取健保卡內儲存的**預防保健服務歷史紀錄**。這些是病患在**所有醫療院所**的執行記錄（跨院），不限於本院。

### 回傳格式

```json
{
  "d": {
    "__type": "UB.Screening.Screening+CardBasicData",
    "CardID": "000013375450",
    "Name": "楊伊雅              ",
    "PId": "I2******76",
    "EPId": "I200XXX976",
    "Birthday": "0861227",
    "Gender": "F",
    "CardIssueDate": "0920307",
    "Note": "1",
    "Age": "29歲",
    "PreventDatas": [
      {
        "Item": "04",
        "ServiceDate": "1141001",
        "HospCode": "3522013684",
        "ServiceCode": "  "
      },
      {
        "Item": "03",
        "ServiceDate": "1140807",
        "HospCode": "3522023662",
        "ServiceCode": "31"
      },
      {
        "Item": "12",
        "ServiceDate": "1140527",
        "HospCode": "3522013684",
        "ServiceCode": "  "
      }
    ]
  }
}
```

### CardBasicData 欄位說明

| 欄位 | 說明 | 格式 |
|------|------|------|
| `CardID` | 健保卡卡號 | 12 位數字 |
| `Name` | 姓名（可能含尾隨空白） | 字串，需 trim |
| `PId` | 身分證字號（遮罩） | `X0******00` |
| `EPId` | 加密身分證字號 | `X000XXX000` |
| `Birthday` | 生日 | 7 位民國年 `YYYMMDD` |
| `Gender` | 性別 | `"M"` 男 / `"F"` 女 |
| `CardIssueDate` | 發卡日 | 7 位民國年 `YYYMMDD` |
| `Note` | 卡片註記 | 字串 |
| `Age` | 年齡（含「歲」字） | 如 `"29歲"` |
| **`PreventDatas`** | **預防保健歷史紀錄陣列** | 見下方 |

### PreventDatas 陣列格式

每筆記錄代表一次預防保健服務執行：

| 欄位 | 說明 | 格式 |
|------|------|------|
| `Item` | 服務代碼（2 碼） | 見「服務代碼對應表」 |
| `ServiceDate` | 執行日期 | 7 位民國年 `YYYMMDD` |
| `HospCode` | 執行院所代碼 | 10 位數字 |
| `ServiceCode` | 項目代碼 | 2 字元（可能為空白） |

**注意**: 同一 Item 可能有多筆記錄（不同日期、不同院所）。通常取最新一筆顯示。

### 與 VoidAPI2 的關係

| 面向 | GetBasicData | VoidAPI2 |
|------|-------------|----------|
| 資料性質 | 歷史紀錄（已做過什麼） | 資格判定（現在能做什麼） |
| 資料範圍 | 跨院（所有醫療院所） | 跨院（國健署整體判定） |
| 呼叫時序 | 先回傳 | 後回傳 |
| 資料粒度 | 逐筆（日期、院所） | 逐項（符合/不符合） |
| 典型用途 | 顯示「健保卡最近記錄」 | 顯示「是否符合資格」 |

### 整合策略

1. 攔截 GetBasicData → 暫存 `PreventDatas`，建立以 `Item` 代碼為 key 的 map（保留每個 Item 最新一筆）
2. 攔截 VoidAPI2 → 解析 `agreeResult`，同時附帶已暫存的健保卡紀錄一起送出
3. 前端透過 Item 代碼對應表，將健保卡紀錄匹配到對應的篩檢項目行

---

## VoidAPI2 — 篩檢資格判定 API

### 端點

```
POST https://pportal.hpa.gov.tw/Screening/Screening.aspx/VoidAPI2
```

### 回傳格式

```json
{
  "d": {
    "__type": "UB.Models.QueryResult",
    "ReturnCode": "0000",
    "Sex": "F",
    "Age": "29",
    "VerifyResult": true,
    "QueryStatus": true,
    "Native": "0",
    "agreeResult": {
      "Adult": "0",
      "BcLiver": "0",
      "Stool": "0",
      "Breast": "?",
      "Oral": "0",
      "Pss": "?",
      "Hpv": "?",
      "Ldct": "?",
      "Gf": "0",
      "Child1": "0", "Child2": "0", "Child3": "0",
      "Child4": "0", "Child5": "0", "Child6": "0", "Child7": "0",
      "SmokingH": "1",
      "SmokingM": "1",
      "Prenatal": "1"
    },
    "ErrorMsg": "0000",
    "ResultMsg": "0000000?0?00000000111??0",
    "BcLiverNeedInformedConsent": false,
    "AdultNeedInformedConsent": false
  }
}
```

### VoidAPI2 頂層欄位

| 欄位 | 說明 |
|------|------|
| `ReturnCode` | `"0000"` 表示成功 |
| `Sex` | 性別：`"M"` 男 / `"F"` 女（來自健保卡） |
| `Age` | 年齡（數字字串） |
| `Native` | 原住民身分：`"0"` 一般、`"1"` 原住民 |
| `agreeResult` | 各項篩檢資格判定（主要資料） |
| `BcLiverNeedInformedConsent` | BC 肝是否需知情同意 |
| `AdultNeedInformedConsent` | 成健是否需知情同意 |

### agreeResult 代碼

VoidAPI2 原始值與標準化後的對應：

| 原始值 | 意義 | 標準化值 | 前端顯示 |
|--------|------|----------|----------|
| `"1"` | 符合資格 | `"1"` | ○ 符合 |
| `"0"` | 不符合資格 | `"2"` | ✗ 不符合 |
| `"?"` | 不適用/無法判定 | `"3"` | △ 待確認 |

### agreeResult 欄位對應

| API Key | 中文名稱 | 說明 | 性別限制 |
|---------|---------|------|----------|
| `Adult` | 成人預防保健 | 成人健康檢查 | 無 |
| `BcLiver` | BC肝篩檢 | BC 型肝炎篩檢 | 無 |
| `Stool` | 定量免疫法糞便潛血檢查 | 腸癌篩檢 | 無 |
| `Breast` | 婦女乳房檢查 | 乳癌篩檢（乳攝影） | 女性 |
| `Oral` | 口腔黏膜檢查 | 口腔篩檢 | 無 |
| `Pss` | 婦女子宮頸抹片檢查 | 子宮頸抹片 | 女性 |
| `Hpv` | 婦女人類乳突病毒檢測服務 | HPV 檢測 | 女性 |
| `Ldct` | 胸部低劑量電腦斷層檢查 | 低劑量肺部 CT | 無 |
| `Gf` | 糞便抗原檢測胃幽門螺旋桿菌 | 胃幽門螺旋桿菌 | 無 |

---

## 服務代碼對應表（通用）

此對應表適用於 GetBasicData 的 `PreventDatas[].Item` 以及健保卡 RegisterPrevent 記錄：

| 代碼 | 服務名稱 | 常用簡稱 | VoidAPI2 對應 Key |
|------|----------|----------|-------------------|
| `01` | 兒童預防保健 | 兒保 | Child1~7 |
| `02` | 成人預防保健 | 成健 | Adult |
| `03` | 婦女子宮頸抹片檢查 | 子宮頸抹片 | Pss |
| `04` | 流行性感冒疫苗 | 流感 | — |
| `05` | 兒童牙齒預防保健 | 兒牙 | — |
| `06` | 婦女乳房檢查 | 乳攝影 | Breast |
| `07` | 定量免疫法糞便潛血檢查 | 腸篩 | Stool |
| `08` | 口腔黏膜檢查 | 口篩 | Oral |
| `09` | 兒童常規疫苗 | 兒疫 | — |
| `10` | 肺炎鏈球菌疫苗 | 肺鏈 | — |
| `11` | 戒菸服務 | 戒菸 | — |
| `12` | COVID-19 疫苗 | 新冠 | — |
| `13` | 婦女人類乳突病毒檢測 | HPV | Hpv |
| `14` | 低劑量電腦斷層 | LDCT | Ldct |
| `15` | 胃幽門螺旋桿菌 | 幽桿 | Gf |

**注意**: 流感(04)、肺鏈(10)、新冠(12) 等疫苗項目在 GetBasicData 有紀錄，但 VoidAPI2 的 agreeResult 中沒有對應欄位（疫苗資格不由 pportal 判定）。

---

## BhpNhi 代碼格式（健保IC卡本機查詢）

### ValidAll 回傳格式：`XXYY-ZZ`

```
XX: BC肝資格
  00 = 未查
  01 = 符合資格
  02 = 年齡不符
  03 = 已做過

YY: 成健資格
  00 = 未查
  01 = 符合資格
  02 = 年齡不符
  03 = 已做過

ZZ: 身分別
  00 = 一般
  01 = 原住民
```

**範例**: `0101-00` = BC肝符合 + 成健符合 + 一般身分

### 錯誤代碼

| 代碼 | 意義 |
|------|------|
| `9999` | Token 驗證失敗 |
| `9998` | 讀取健保控制軟體/健保卡/SAM 驗證失敗 |
| `9001` | 資料傳入格式檢核不正確 |
| `9002` | 個案健保卡註記含空白或特殊字元 |
| `0000` | Token 驗證成功（但無查詢結果） |

### BC肝登記/取消代碼

| 動作 | 代碼 | 意義 |
|------|------|------|
| 登記成功 | `1100-ZZ` | BC肝篩檢登記成功 |
| 年齡不符 | `1200-ZZ` | 登記失敗：年齡不符合 |
| 已做過 | `1300-ZZ` | 登記失敗：已做過 |
| 取消成功 | `2100-ZZ` | BC肝篩檢登記取消成功 |
| 未登記 | `2200-ZZ` | 取消失敗：未在本院所登記 |
| 逾期 | `2300-ZZ` | 取消失敗：作業已逾期 |

---

## 健保卡預防保健服務記錄（RegisterPrevent）

健保卡內記錄的保健服務記錄，每組 21 bytes，最多 6 組：

```
位置 0-1   (2 bytes): 服務代碼（對應「服務代碼對應表」）
位置 2-8   (7 bytes): 檢查日期（民國年 YYYMMDD）
位置 9-18  (10 bytes): 醫院代碼
位置 19-20 (2 bytes): 項目代碼
```

---

## 自動化登入技術要點

### 1. 登入表單是同頁 Modal

登入表單不會產生頁面導航（no navigation），是 JavaScript 動態顯示的 modal。因此：
- 不能用頁面載入事件偵測 modal 出現
- 需要用 **polling（定時查詢 DOM）** 偵測 modal 是否出現
- 按鈕文字匹配需精確：只匹配「服務登入」，避免匹配到「一般登入」tab

### 2. 表單欄位匹配策略

用 `placeholder` 精確匹配最可靠：
- 帳號：`placeholder === '請輸入帳號'`
- 密碼：`placeholder === '請輸入密碼'`

**不要用** `input[type="password"]`（會匹配到變更密碼的 `ctl00_txt_OldPswd`）。

### 3. ASP.NET WebForms 填入注意

ASP.NET 的 `__doPostBack` 機制依賴 JavaScript 事件。直接設定 `input.value` 可能不會觸發 ASP.NET 的 change 事件。建議：
- 使用模擬鍵盤輸入（如 Electron 的 `insertText`、Puppeteer 的 `page.type`）
- 或在設值後手動觸發 `input`/`change` 事件

### 4. 驗證碼

- 為 4 碼數字的圖形驗證碼，無法自動辨識
- 需等使用者手動輸入
- 可用 polling 偵測驗證碼欄位的值長度 ≥ 4 後自動點擊「登入」按鈕

### 5. Cookie 持久化

登入成功後的 session cookie 應保留，避免每次都需重新登入：
- Electron：使用 `session.fromPartition('persist:xxx')`
- Puppeteer/Playwright：儲存 cookies 到檔案
- 一般瀏覽器自動化：使用 user data directory

### 6. XHR 攔截策略

需攔截 response body（不只 headers），常用方法：
- **Electron**: Chrome DevTools Protocol（CDP）的 `Network.getResponseBody`
- **Puppeteer/Playwright**: `page.on('response')` + `response.json()`
- **瀏覽器擴充**: `chrome.devtools.network` 或 `fetch` monkey-patching

### 7. 子視窗攔截

國健署的篩檢頁面在新視窗中開啟（`window.open`），對子視窗也需要設定 XHR 攔截。
（參照原則 2「多視窗生命週期管理」和原則 6「XHR 攔截」）

---

## 性別判斷

判斷病患性別以決定是否顯示女性專屬篩檢項目時，應綜合多個來源：

| 來源 | 欄位 | 值 |
|------|------|-----|
| 本院資料庫 | `msex` | `'1'` 男 / `'2'` 女 |
| VoidAPI2 回傳 | `Sex` | `"M"` 男 / `"F"` 女 |
| GetBasicData 回傳 | `Gender` | `"M"` 男 / `"F"` 女 |

建議：任一來源判定為女性即顯示女性專屬項目（子宮頸抹片、乳攝影、HPV）。

---

## 注意事項

1. **VoidAPI2 / GetBasicData 回傳格式可能隨國健署改版而變化**，需定期確認
2. **agreeResult 值為字串型別**（`"1"` 不是 `1`）
3. **篩檢項目名稱必須與 VoidAPI2 回傳完全一致**（如「定量免疫法糞便潛血檢查」不能簡寫）
4. **BhpNhi 需要健保IC卡讀卡機和控制軟體**，Pportal 只需帳號密碼
5. **驗證碼為 4 碼數字**，是圖形驗證碼，無法自動辨識
6. **登入頁面使用 ASP.NET WebForms 的 `__doPostBack` 機制**，表單提交非標準 HTML form submit
7. **GetBasicData 先於 VoidAPI2 回傳**，攔截時需注意時序：先暫存健保卡紀錄，待 VoidAPI2 到達時合併
8. **PreventDatas 同一 Item 可能有多筆記錄**（如多次流感施打），取最新一筆即可
9. **`hisGetBasicData` ≠ `GetBasicData`**：前者是 pportal 網頁呼叫本機讀卡軟體的 client-side API，後者是 pportal 伺服器回傳的 server-side XHR。讀卡失敗時會出現「等待 hisGetBasicData 回應超時」錯誤
