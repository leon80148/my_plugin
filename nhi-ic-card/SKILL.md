---
name: nhi-ic-card
description: 健保IC卡讀卡整合技能。涵蓋 BhpNhi.dll API 開發、回應碼解碼、成健/BC肝篩檢工作流程、IC卡欄位結構、資料上傳格式2.0。當涉及健保卡讀卡、篩檢資格查詢、IC卡欄位、或上傳XML時自動啟用。
version: 2.0.0
source: 健保署元件套用說明 + 測試說明 + IC卡存放內容規格 + 上傳格式2.0作業說明
tags: [healthcare, NHI, IC-card, BhpNhi, dotnet, screening, upload-format, Taiwan]
---

# Skill: 健保IC卡整合開發參考

本 Skill 整合台灣健保IC卡讀卡系統的完整知識，涵蓋 API 開發、篩檢工作流程、卡片欄位結構、資料上傳格式四大主題。

## 使用時機

當以下任一條件符合時，應自動啟用：

- 提到 **BhpNhi.dll**、**CsHis.dll**、**健保卡讀卡**、**IC卡讀卡機**
- 需要整合 **成人健檢**、**BC肝篩檢** API
- 開發或修改 **.NET 讀卡應用程式**
- 需要處理 **API 回應碼**、**錯誤碼**
- 診所人員詢問**篩檢資格代碼**的意思
- 查詢 **IC 卡欄位結構**、**RegisterPrevent** 解析
- 需要產生**健保卡上傳 XML** 或處理異常上傳情境
- 查詢**就醫類別 (M07)** 與欄位交叉檢核規則

---

## 系統架構

```
HIS 系統
  |
  +-- BhpNhi.dll（封裝層，本專案使用）
  |     +-- 內部呼叫 CsHis.dll（讀卡機控制軟體 6.0）
  |     +-- 內部呼叫 HpaBhp.dll（Token 驗證）
  |     +-- 呼叫國健署 API（成健/BC肝資格查詢）
  |
  +-- 讀卡機硬體 + SAM 卡
  +-- 健保卡控制軟體 6.0 主控台
```

---

## API 方法速查表

```csharp
var bhpNhi = new BhpNhi.Bhp();
```

| 方法 | 用途 | 回傳 | 前置條件 |
|------|------|------|----------|
| `GetPersonData()` | 讀卡 + 建立 Token | JSON → `Person` | 無（**必須最先呼叫**） |
| `ValidAdult()` | 成健資格查詢 | JSON → `ApiResponse` | 需先 GetPersonData |
| `ValidBcLiver()` | BC肝資格查詢 | JSON → `ApiResponse` | 需先 GetPersonData |
| `ValidAll()` | 成健+BC肝同時查詢 | JSON → `ApiResponse` | 需先 GetPersonData |
| `RegisterBcLiver()` | BC肝篩檢登記 | JSON → `ApiResponse` | 需先 GetPersonData |
| `CancelBcLiver()` | BC肝取消登記 | JSON → `ApiResponse` | 需先 GetPersonData |
| `GetVersion()` | DLL 版本 | string | 無 |
| `GetStatus()` | 主控台狀態 | string | 無 |

---

## 回應碼格式 XXYY-ZZ 速記

```
  XX    YY  -  ZZ
  BC肝  成健    身分別

  01 = 未做過（符合資格）    00 = 一般身分
  02 = 年齡不符              01 = 原住民
  03 = 已做過
  00 = 未查
```

快速範例：`0101-00` = 兩者都符合(一般) | `0303-01` = 都做過(原住民)

### 登記/取消碼

| 前綴 | 意義 |
|------|------|
| `1100` | 登記成功 |
| `1200` | 登記失敗（年齡不符） |
| `1300` | 登記失敗（已做過） |
| `2100` | 取消成功 |
| `2200` | 取消失敗（無登記紀錄） |
| `2300` | 取消失敗（逾期） |

### 錯誤碼

| Code | 說明 |
|------|------|
| `9999` | Token 驗證失敗（未先讀卡/網路不通） |
| `9998` | 主控台/SAM/卡片驗證失敗 |
| `9001` | 資料格式檢核不正確 |
| `9002` | 健保卡註記含空白或特殊字元 |

---

## 就醫類別 M07 常用代碼

| M07 | 說明 | 就醫序號 |
|-----|------|----------|
| `01` | 西醫門診 | 需取號 |
| `02` | 牙醫門診 | 需取號 |
| `03` | 中醫門診 | 需取號 |
| `04` | 急診 | 需取號 |
| `05` | 住院 | 需取號 |
| `AC` | 預防保健 | ICxx 格式 |
| `AD` | 職災門(急)診 | 不取號 |
| `AE` | 慢連箋領藥 | 不取號 |
| `AF` | 藥局調劑 | 不取號 |

---

## IC 卡四大區段概覽

| 區段 | 欄位數 | 主要內容 |
|------|--------|---------|
| 基本資料 | 8 | 卡號、姓名、身分證、生日、性別 |
| 健保資料段 | 67 | 投保、重大傷病、就醫紀錄(6次)、預防保健註記 |
| 醫療專區 | 26 | 處方紀錄、過敏藥物(3筆) |
| 衛生行政專區 | 17 | 疫苗接種紀錄(6筆) |

> BhpNhi.dll 的 `GetPersonData()` 只讀 6 個欄位（HospId, SamId, CardId, Pid, Birth, RegisterPrevent）。完整卡片資料需用 CsHis.dll。

---

## 篩檢資格規則

### 成人預防保健

| 對象 | 年齡 | 頻率 |
|------|------|------|
| 一般身分 | 40-64 歲 | 每 3 年 1 次 |
| 一般身分 | 65 歲以上 | 每年 1 次 |
| 原住民 | 55 歲以上 | 每年 1 次 |

### BC肝篩檢

| 對象 | 年齡 | 頻率 |
|------|------|------|
| 一般身分 | 45-79 歲 | **終身 1 次** |
| 原住民 | 40-79 歲 | **終身 1 次** |

---

## 詳細參考文件（按需載入）

以下 references 檔案包含完整細節，Claude 會依據問題自動讀取相關檔案：

| 檔案 | 內容 | 適用對象 |
|------|------|----------|
| [`references/api-development.md`](references/api-development.md) | BhpNhi.dll API 開發、資料模型、回應碼完整表、程式碼範本、疑難排解 Decision Tree | 開發者 |
| [`references/screening-workflow.md`](references/screening-workflow.md) | 成健/BC肝篩檢工作流程、白話代碼對照、登記取消流程、展望HIS整合、FAQ | 診所人員 + 開發者 |
| [`references/card-fields.md`](references/card-fields.md) | IC卡 822+ 欄位結構、四大區段定義、RegisterPrevent 解析、日期格式轉換 | 開發者 |
| [`references/upload-format.md`](references/upload-format.md) | 上傳格式 2.0 XML 結構、MSH/MB1/MB2 欄位規則、異常上傳、補卡、急診住院規則 | 開發者 + 診所人員 |

### 路由指引

- **「怎麼呼叫 API」「程式碼範例」「DLL 載入失敗」** → 讀取 `references/api-development.md`
- **「這個代碼什麼意思」「病人符不符合資格」「登記流程」** → 讀取 `references/screening-workflow.md`
- **「IC卡存了什麼」「欄位格式」「RegisterPrevent 怎麼解」** → 讀取 `references/card-fields.md`
- **「上傳 XML 怎麼寫」「異常上傳」「補卡」「就醫類別」** → 讀取 `references/upload-format.md`

---

## 共通注意事項

1. **GetPersonData() 必須最先呼叫** — 它建立 Token 通道，未先呼叫會得到 9999 錯誤。

2. **Status=true 不代表符合資格** — `ApiResponse.Status` 只表示 API 呼叫成功，實際資格看 `Code` 欄位解碼。

3. **BC肝篩檢終身一次** — 不同於成健可定期做，BC肝是終身只有一次。登記(Register)≠執行，確認執行後才登記。

4. **XML 編碼是 Big5** — 上傳 XML 宣告必須用 `encoding="Big5"`，否則退件。

5. **範例程式按鈕事件未綁定** — 官方範例 Designer.cs 中只有 `btn_getConsoleStatus` 有綁定，其餘 7 個按鈕需手動補上。

6. **DLL 參考路徑不一致** — .csproj 寫的路徑與實際不同，建置前需確認。下載的 DLL 可能被 Windows 封鎖，需右鍵解除。
