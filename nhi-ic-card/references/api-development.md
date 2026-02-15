# BhpNhi.dll API 開發參考

本文件提供台灣健保IC卡讀卡元件 BhpNhi.dll 的完整開發知識。包含 API 架構、資料模型、回應碼、程式碼範本、疑難排解。

## 系統需求

| 項目 | 需求 |
|------|------|
| 作業系統 | Windows 10 專業版 22H2 以上 |
| Runtime | .NET Desktop Runtime 6.0.36 |
| 硬體 | 健保卡讀卡機 + 驅動程式 |
| 軟體 | 健保卡控制軟體 6.0（主控台） |
| NuGet 套件 | Newtonsoft.Json 13.0.3 |
| 元件 | BhpNhi.dll（需加入專案參考） |

---

## API 架構流程

```
HIS 系統
  │
  ├─ 引入 CsHis.dll（讀卡機控制軟體）
  │   ├─ NHIcsOpenCom        → 開啟連線
  │   ├─ NHIcsGetHospID      → 取得院所代號
  │   ├─ NHIcsGetCardNo      → 取得卡號
  │   ├─ NHIhisGetBasicData  → 取得基本資料
  │   ├─ NHIhisGetRegisterPrevent → 取得預防保健註記
  │   └─ NHIcsCloseCom       → 關閉連線
  │
  ├─ 調用 HpaBhp.dll 取得 Token
  │   ├─ 檢查傳入 key 值
  │   ├─ 驗證 Token（驗證後即註記用過）
  │   │   ├─ 通過 → 可用功能
  │   │   └─ 失敗 → 不可使用
  │   ├─ 產生 Token 存入 db
  │   └─ 回傳 HpaBhp.dll
  │
  └─ 呼叫 API 進行資格檢查
      └─ 國健署成健及BC肝相關 API
          ├─ 成健及BC肝篩檢資格查詢（含健保卡6次就醫紀錄比對）
          └─ 民眾前次到院服務紀錄
```

**關鍵**: BhpNhi.dll 封裝了上述所有流程，開發者只需呼叫簡化的 API 方法即可。

---

## API 方法速查表

### 初始化

```csharp
using BhpNhi;
using Newtonsoft.Json;

BhpNhi.Bhp bhpNhi = new BhpNhi.Bhp();
```

### 方法一覽

| 方法 | 用途 | 回傳型別 | 說明 |
|------|------|----------|------|
| `GetPersonData()` | 讀取卡片基本資料 | JSON string → `BhpNhi.Person` | **必須最先呼叫**，取得 Token |
| `ValidAdult()` | 成人健檢資格查詢 | JSON string → `ApiResponse` | 需先呼叫 GetPersonData |
| `ValidBcLiver()` | BC肝篩檢資格查詢 | JSON string → `ApiResponse` | 需先呼叫 GetPersonData |
| `ValidAll()` | 成健 + BC肝同時查詢 | JSON string → `ApiResponse` | 需先呼叫 GetPersonData |
| `RegisterBcLiver()` | BC肝篩檢登記 | JSON string → `ApiResponse` | 需先呼叫 GetPersonData |
| `CancelBcLiver()` | BC肝篩檢取消登記 | JSON string → `ApiResponse` | 需先呼叫 GetPersonData |
| `GetVersion()` | 取得 DLL 版本 | string | 不需先讀卡 |
| `GetStatus()` | 讀取主控台狀態 | string | 不需先讀卡 |

### 對應 REST API 端點

| BhpNhi.dll 方法 | 對應 API 端點 |
|-----------------|-------------|
| ValidAll() | /api/All/Valid |
| ValidAdult() | /api/Adult/Valid |
| ValidBcLiver() | /api/BcLiver/Valid |
| RegisterBcLiver() | /api/BcLiver/Register |
| CancelBcLiver() | /api/BcLiver/Cancel |
| GetVersion() | /api/Version |

API Swagger 文件: `https://apcvpn.hpa.gov.tw/bhpapi/swagger/index.html`

---

## 資料模型

### BhpNhi.Person

`GetPersonData()` 回傳 JSON 字串，反序列化為此模型：

```csharp
public class Person
{
    public string HospId { get; set; }           // 醫療院所代號
    public string SamId { get; set; }            // 安全模組卡號 (SAM)
    public string CardId { get; set; }           // 民眾健保卡號
    public string Pid { get; set; }              // 民眾身分證號
    public string Birth { get; set; }            // 民眾出生日期（民國年 YYYMMDD）
    public string RegisterPrevent { get; set; }  // 預防保健註記（多筆紀錄串接）
}
```

### ApiResponse

`ValidAdult()`, `ValidBcLiver()`, `ValidAll()`, `RegisterBcLiver()`, `CancelBcLiver()` 回傳此模型：

```csharp
public class ApiResponse
{
    public bool Status { get; set; }        // 回傳狀態（true=API呼叫成功, false=失敗）
    public string Code { get; set; }        // 回傳代碼（見回應碼編碼原則）
    public string Description { get; set; } // 描述（中文說明）
}
```

---

## 回應碼編碼原則（核心）

### 資格查詢碼格式：`XXYY-ZZ`

```
  XX    YY  -  ZZ
  ││    ││     ││
  ││    ││     └┘─ 身分別
  ││    └┘──────── 成健資格查詢結果
  └┘────────────── BC肝資格查詢結果
```

| 位置 | 值 | 意義 |
|------|----|------|
| XX（第1-2碼）BC肝結果 | 00 | 未查 B、C 肝炎 |
| | 01 | 未做過（**符合資格**） |
| | 02 | 年齡不符 |
| | 03 | 已做過 |
| YY（第3-4碼）成健結果 | 00 | 未查成人預防保健 |
| | 01 | 未做過（**符合資格**） |
| | 02 | 年齡不符 |
| | 03 | 已做過 |
| ZZ（第5-6碼）身分別 | 00 | 一般身分 |
| | 01 | 原住民 |

### 快速判斷範例

```
"0101-00" → BC肝未做過 + 成健未做過 + 一般身分 → 兩者都符合資格
"0303-01" → BC肝已做過 + 成健已做過 + 原住民 → 都不符合
"0001-00" → BC肝未查 + 成健未做過 + 一般 → 只查成健，符合資格
"0200-01" → BC肝年齡不符 + 成健未查 + 原住民 → 只查BC肝，不符合
```

### C# 回應碼解析

```csharp
string code = response.Code;  // 例如 "0101-00"
string bcResult = code.Substring(0, 2);    // BC肝結果
string adultResult = code.Substring(2, 2); // 成健結果
string identity = code.Substring(5, 2);    // 身分別

bool bcEligible = bcResult == "01";
bool adultEligible = adultResult == "01";
bool isIndigenous = identity == "01";
```

### 登記回應碼

| Code | 說明 |
|------|------|
| 1100-0X | 登記成功 |
| 1200-0X | 登記失敗，年齡不符合 B、C 肝篩檢資格 |
| 1300-0X | 登記失敗，已做過 B、C 肝篩檢 |

### 取消回應碼

| Code | 說明 |
|------|------|
| 2100-0X | 取消成功 |
| 2200-0X | 取消失敗，未在院所登記過 B、C 肝篩檢 |
| 2300-0X | 取消失敗，作業已逾期 |

> **X = 0** 為一般身分，**X = 1** 為原住民身分

---

## 錯誤碼與排解

| Code | 說明 | 排解方法 |
|------|------|---------|
| 9999 | Token 驗證失敗 | 1. 檢查網路連線 2. 確認 HPA API 可存取 (apcvpn.hpa.gov.tw) 3. 確認已先呼叫 GetPersonData() |
| 9001 | 資料傳入格式檢核不正確 | 檢查以下格式：院所代碼、SAM 代碼、健保卡號碼、證號、健保卡就醫資料、出生日期 |
| 9002 | 個案健保卡註記含空白或特殊字元 | 請自行檢視完整服務紀錄，可能是卡片資料異常 |
| 9998 | 主控台/業務端/健保卡/SAM 驗證失敗 | 1. 確認主控台已啟動 2. 檢查讀卡機連線 3. 確認卡片正確插入 4. 檢查 SAM 卡 |

---

## 程式碼範本

### 基本讀卡

```csharp
using BhpNhi;
using Newtonsoft.Json;

var bhpNhi = new BhpNhi.Bhp();

// 1. 讀取卡片基本資料（必須最先呼叫）
var resp = bhpNhi.GetPersonData();
try
{
    var data = JsonConvert.DeserializeObject<BhpNhi.Person>(resp);
    Console.WriteLine($"院所代號: {data.HospId}");
    Console.WriteLine($"SAM卡號: {data.SamId}");
    Console.WriteLine($"健保卡號: {data.CardId}");
    Console.WriteLine($"身分證號: {data.Pid}");
    Console.WriteLine($"出生日期: {data.Birth}");
    Console.WriteLine($"預防保健註記: {data.RegisterPrevent}");
}
catch (Exception)
{
    // GetPersonData() 失敗時回傳的不是合法 JSON，而是錯誤訊息字串
    Console.WriteLine($"讀卡失敗: {resp}");
}
```

### 資格查詢與結果解析

```csharp
// 2. 查詢成健 + BC肝篩檢資格（需先完成 GetPersonData）
string result = bhpNhi.ValidAll();
var response = JsonConvert.DeserializeObject<ApiResponse>(result);

if (response.Status)
{
    string code = response.Code;
    string bcResult = code.Substring(0, 2);
    string adultResult = code.Substring(2, 2);
    string identity = code.Substring(5, 2);

    if (bcResult == "01") Console.WriteLine("符合 BC 肝篩檢資格");
    if (adultResult == "01") Console.WriteLine("符合成人健檢資格");
    if (identity == "01") Console.WriteLine("原住民身分");
}
else
{
    Console.WriteLine($"查詢失敗: {response.Code} - {response.Description}");
}
```

### BC肝篩檢登記與取消

```csharp
// 3. 登記（需先完成 GetPersonData）
string regResult = bhpNhi.RegisterBcLiver();
Console.WriteLine($"登記結果: {regResult}");

// 4. 取消登記
string cancelResult = bhpNhi.CancelBcLiver();
Console.WriteLine($"取消結果: {cancelResult}");
```

### Windows Forms 事件綁定（補齊範例程式缺少的）

```csharp
// 在 frmMain.Designer.cs 的 InitializeComponent() 中加入：
btn_getHcData.Click += btn_getHcData_Click;
btn_validAdult.Click += btn_validAdult_Click;
btn_validBc.Click += btn_validBc_Click;
btn_validAll.Click += btn_validAll_Click;
btn_BcRegister.Click += btn_BcRegister_Click;
btn_BcCancel.Click += btn_BcCancel_Click;
btn_getDllVersion.Click += btn_getDllVersion_Click;
// btn_getConsoleStatus 已有綁定
```

### .csproj 參考設定

```xml
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
</ItemGroup>
<ItemGroup>
  <Reference Include="BhpNhi">
    <HintPath>..\BhpNhi組件\BhpNhi.dll</HintPath>
  </Reference>
</ItemGroup>
```

---

## 疑難排解 Decision Tree

```
問題：讀卡或查詢失敗
│
├─ GetStatus() 回傳錯誤
│   ├─ "未偵測到讀卡機" → 檢查 USB 連線 / 讀卡機驅動
│   ├─ "無卡片" → 確認健保卡正確插入（晶片朝上）
│   └─ "主控台未啟動" → 啟動健保卡控制軟體 6.0 主控台
│
├─ GetPersonData() 回傳非 JSON
│   ├─ 含 "9998" → 主控台/SAM/卡片驗證失敗，檢查硬體
│   └─ 其他錯誤 → 記錄完整訊息，聯繫支援
│
├─ 資格查詢回傳 "9999"
│   └─ Token 驗證失敗
│       ├─ 未先呼叫 GetPersonData()? → 先讀卡
│       ├─ 網路不通? → 檢查網路連線
│       └─ HPA API 不可存取? → 檢查防火牆/VPN
│
├─ 資格查詢回傳 "9001"
│   └─ 資料格式錯誤 → 檢查卡片資料是否完整
│
├─ DLL 載入失敗 (FileNotFoundException)
│   ├─ BhpNhi.dll 路徑不對? → 檢查 .csproj HintPath
│   ├─ DLL 被 Windows 封鎖? → 右鍵屬性 → 解除封鎖
│   └─ .NET Runtime 版本不對? → 需 .NET Desktop Runtime 6.0
│
└─ 按鈕點擊無反應
    └─ Designer.cs 缺少 Click 事件綁定 → 補上事件綁定
```

---

## 第二次查詢機制

同一天、同一醫事機構、同一個案，**第二次**點選資格查詢時：

1. 系統判斷為重複查詢
2. 彈出「知情同意」提醒視窗，確認是否取得民眾知情同意
3. 確認後，回傳結果 Description 中會包含**前次服務機構名稱**
4. 用於讓院所確認個案之前在哪裡做過篩檢

---

## Gotchas

1. **GetPersonData() 必須最先呼叫** — 它不只讀卡，還會建立 Token 通道。未先呼叫就做資格查詢會得到 9999。

2. **回傳值是 JSON 字串** — 所有方法回傳 `string`，需 `JsonConvert.DeserializeObject<T>()` 反序列化。

3. **Status=true 不代表符合資格** — `Status` 只表示 API 呼叫成功，實際資格看 `Code` 欄位。

4. **範例程式按鈕事件未綁定** — 官方範例 Designer.cs 中只有 `btn_getConsoleStatus` 有綁定 Click，其餘 7 個按鈕需手動補上。

5. **DLL 參考路徑不一致** — .csproj 寫 `..\BhpNhi\bin\Debug\net6.0\BhpNhi.dll`，實際在 `BhpNhi組件\BhpNhi.dll`。

6. **下載 DLL 需解除封鎖** — Windows 可能封鎖網路下載的 DLL，右鍵 → 屬性 → 解除封鎖。

7. **僅適用控制軟體 6.0** — BhpNhi.dll 僅相容健保卡控制軟體 6.0 版。

8. **RegisterPrevent 是串接字串** — 多筆預防保健紀錄串接，需解析（見 card-fields.md）。
