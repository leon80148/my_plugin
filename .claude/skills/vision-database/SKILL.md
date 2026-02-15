---
name: vision-database
description: 展望醫療系統 HIS 資料庫查詢技能。當使用者提到展望資料庫、vision_clinic.db、診所資料、DBF 檔案、或需要查詢病患/處方/檢驗/掛號/庫存等醫療資料時自動啟用。根據需求定位正確的資料表、欄位與代碼，產出 SQLite 或 PostgreSQL 查詢語句。
---

# Skill: 展望醫療系統資料庫

本 Skill 提供展望診所 HIS 系統的完整資料庫知識。啟用後，Claude 能根據需求找到正確的資料表、欄位和代碼，產出可執行的查詢。

## 使用時機

當以下任一條件符合時，應自動啟用此 Skill：

- 使用者提到**展望資料庫**、**vision_clinic.db**、**HIS 系統**、**診所資料**
- 需要查詢**病患**、**處方**、**檢驗**、**掛號**、**庫存**相關醫療資料
- 使用者提到 **DBF 檔案**或相關資料表名稱（CO01M, CO02M, CO02F, CO02H, CO03L, CO03M, CO05B, CO05O, CO09D, CO09S, CO10A, CO18H, VISHFAM）
- 使用者詢問**藥品庫存**、**預防保健**、**疾病管理**（糖尿病照護、CKD 等）
- 使用者提到**病歷號** (KCSTMR)、**ICD 診斷碼**、**檢驗項目代碼** (HITEM)
- 使用者詢問**病歷紀錄**、**SOAP Notes**、**醫師記錄**、**看診紀錄內容**

## 使用說明

收到此 Skill 後，依以下流程處理：

1. **確認資料來源** — 判斷目前專案使用的是 SQLite (`vision_clinic.db`) 還是 PostgreSQL（Anchia Clinic Monitor）
2. **從 Decision Tree 定位資料表** — 根據使用者需求，找到該用哪些資料表和欄位
3. **產出查詢語句** — 根據資料來源產出正確語法的查詢（注意 SQLite vs PostgreSQL 差異）
4. **提醒查詢陷阱** — 如遇到 HVAL 數值比較、CO02F 分段合併、DNO 多義性等已知陷阱，主動提醒

---

## 資料來源設定

根據你的專案，資料來源可能不同。使用前請確認：

| 項目 | SQLite（原始查詢） | PostgreSQL（Anchia Clinic Monitor） |
|------|-------------------|-------------------------------------|
| 資料表名 | 大寫 `CO01M` | 小寫 `co01m` |
| 資料庫路徑 | `vision_clinic.db`（需設定） | 由專案連線設定決定 |
| 保留字欄位 | 不需引號 | `"date"`, `"time"`, `"case"` 需雙引號 |
| 額外欄位 | 無 | `record_hash`, `created_at`, `updated_at` |
| 最近 N 筆語法 | `GROUP BY` + `MAX()` | `DISTINCT ON (col)` |

**SQLite 連線範例**：
```bash
sqlite3 "<專案中 vision_clinic.db 的路徑>" "SELECT ..."
```

---

## 需求 → 資料表速查（Decision Tree）

根據你要做的事，找到該用哪些資料表：

### 病患相關

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 查病患基本資料（姓名、性別、生日、電話、地址） | **CO01M** | `KCSTMR`(病歷號), `MNAME`, `MSEX`, `MBIRTHDT`, `MPERSONID`(身分證), `MTELH`, `MTELO`, `MADDR` | 主鍵 `KCSTMR` 為 7 位數字字串 |
| 用身分證找病歷號 | **CO01M** | `MPERSONID` → `KCSTMR` | |
| 從家醫計畫找病患 | **VISHFAM** → **CO01M** | `VISHFAM.PAT_PID` = `CO01M.MPERSONID` | VISHFAM 用身分證，非病歷號 |

### 就診與掛號

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 就診歷史（含診斷） | **CO03L** | `KCSTMR`, `DATE`, `TIME`, `LABNO`(ICD主診斷), `LABDT`(診斷中文), `LTIME`(完診時間) | `LTIME='000000'` 表示未完診 |
| 掛號記錄（完整） | **CO05O** | `KCSTMR`, `TBKDT`, `TSTS`(狀態), `TNAME`, `TARTIME`(看診順序) | 含費用欄位 |
| 預約記錄 | **CO05B** | `KCSTMR`, `TBKDATE`, `TBKTIME`, `TSTS` | CO05O 的子集 |
| 今日門診狀態 | **CO05O** | `TBKDT`=今日 + `TSTS IN ('0','1')` | 候診中=0, 看診中=1, 完診=F |
| 看診費用與診斷碼 | **CO03M** | `KCSTMR`, `IDATE`, `LABNO`(主ICD), `LACD01`~`LACD05`(次ICD), `TOT`(總額), `A98`(部分負擔) | |

### 處方與用藥

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 處方記錄 | **CO02M** | `KCSTMR`, `IDATE`, `DNO`(醫令碼), `PFQ`(頻率), `PTDAY`(天數), `PTQTY`(數量) | |
| 藥品名稱與資訊 | **CO09D** | `KDRUG`(醫令碼), `DNO`(健保碼), `DDESC`(英文名), `DDESC2`(中文名), `DP2`(健保價) | |
| 處方→藥品 JOIN | **CO02M** + **CO09D** | `CO02M.DNO = CO09D.KDRUG OR CO02M.DNO = CO09D.DNO` | 兩欄都要比對 |

### 檢驗與生理量測

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 檢驗數值（抽血等） | **CO18H** | `KCSTMR`, `HDATE`, `HITEM`(項目代碼), `HVAL`(數值), `HDSCP`(說明), `HRESULT`(判定) | `HVAL` 為文字，數值比較需 CAST |
| 生理量測（血壓等） | **CO18H** | 同上，`HITEM` 無 `Z0S` 前綴 | BP 格式為 `收縮壓/舒張壓` |
| 某項檢驗的趨勢 | **CO18H** | `WHERE KCSTMR=? AND HITEM=? ORDER BY HDATE DESC` | |
| 最近一次各項結果 | **CO18H** | 需子查詢取每個 HITEM 的 MAX(HDATE) | 見查詢範例 |

### 病歷紀錄（SOAP Notes）

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 醫師看診病歷（SOAP） | **CO02H** | `KCSTMR`, `SDATE`, `STIME`, `STEXT`(內容), `SATB`(段落序號) | 超過 250 字分段，需按 SATB 排序合併 |
| 特定日期的完整病歷 | **CO02H** | `GROUP_CONCAT(STEXT, '' ORDER BY SATB)` 合併 | 同一次看診以 KCSTMR+SDATE+STIME 識別 |
| 主診斷 ICD 碼 | **CO02H** | `SLABNO` | 直接存於病歷記錄中 |

### 檢查報告

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 超音波/心電圖/肺功能報告 | **CO02F** | `KCSTMR`, `FDATE`, `FNO`(報告類型), `FTEXT`(內容), `FSQ`(序號) | 超過 250 字分段，需合併 |
| 哪些就診有做檢查 | **CO02M** | `DNO` 為檢查代碼（如 `19009C` 腹超） | |

### 藥品庫存

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 藥品庫存量 | **CO09D** | `KDRUG`, `DQTY2`(庫存), `DORDPOINT`(安全量), `DLVENDOR`(廠商) | 低庫存: `DQTY2 <= DORDPOINT` |
| 庫存異動歷程 | **CO09S** | `KDRUG`, `DDATE`, `DIO`(類型), `DQTY`(數量) | DIO: 5=消耗, B=期初, 2=進貨, 8=調整 |
| 進貨記錄 | **CO10A** | `KDRUG`, `ADATE`, `AQTY`, `APRICE`, `AREMARK`(效期) | ATYPE: 2=進貨, 8=調整 |
| 月消耗量統計 | **CO09S** | `DIO='5'` + `DDATE LIKE 'YYYMM%'` + `SUM(DQTY)` | |

### 預防保健與疾病管理

| 我需要... | 主資料表 | 關鍵欄位 | 備註 |
|-----------|---------|----------|------|
| 成人健檢記錄 | **CO03L** | `LISRS IN ('3D','21','22','3E','23','24')` | 一階/二階 |
| 癌症篩檢記錄 | **CO03L** | `LISRS='85'`(大腸癌), `LISRS='95'`(口腔癌) | |
| 疫苗接種記錄 | **CO03L** | `LISRS='AU'`(流感), `LISRS='VU'`(新冠), `LISRS='DU'`(肺炎鏈球菌) | |
| 糖尿病照護追蹤 | **CO02M** | `DNO IN ('P1406C'~'P1410C','P7001C','P7002C')` | 見代碼表 |
| CKD 照護追蹤 | **CO02M** | `DNO IN ('P4301C','P4302C')` | |
| 代謝症候群追蹤 | **CO02M** | `DNO IN ('P7501C','P7502C','P7503C')` | |
| 家醫計畫成員 | **VISHFAM** | `CASE_TYPE`(A=健保收案, B=一般), 健康風險: `HBP`(高血壓), `ASCVD` 等 | |

---

## 資料表 Schema 精簡參考

### CO01M - 病患主檔（主鍵: KCSTMR）

| 欄位 | 說明 | 範例 |
|------|------|------|
| KCSTMR | 病歷號 (7位) | `0000001` |
| MNAME | 姓名 | `王小明` |
| MSEX | 性別 (1=男, 2=女) | `1` |
| MBIRTHDT | 生日 (民國年) | `0761015` |
| MPERSONID | 身分證字號 | `A123456789` |
| MTELH / MTELO | 電話 | |
| MADDR | 地址 | |
| MREMARK | 備註 | |

### CO02M - 處方記錄（複合鍵: KCSTMR+IDATE+ITIME+DNO）

| 欄位 | 說明 | 範例 |
|------|------|------|
| KCSTMR | 病歷號 | |
| IDATE | 就診日期 (民國年) | `1141127` |
| ITIME | 就診時間 | `140530` |
| DNO | 藥品/醫令代碼 | `P1407C` |
| WICTM | 處方內容說明 | |
| PFQ | 頻率 (QD/BID/TID/QID/PRN) | `TID` |
| PTDAY | 天數 | `7` |
| PTQTY | 總數量 | `2100` |

### CO02H - 醫師病歷紀錄 SOAP Notes（複合鍵: KCSTMR+SDATE+STIME+SATB）

| 欄位 | 說明 | 範例 |
|------|------|------|
| KCSTMR | 病歷號 | `0000001` |
| SDATE | 看診日期 (民國年) | `1120801` |
| STIME | 看診時間 | `103819` |
| SIDS | 診間代碼 (01=主診間) | `01` |
| SID | 醫師代碼 (1 或 2) | `2` |
| SATB | 段落序號 (1,2,...9,A,B,C,D,E) | `1` |
| STYP | 段落類型 (O=首段, 空=接續段) | `O` |
| SLM | 身分別 (A=健保, 9=其他, 1=重大傷病, 3=福保, 4=榮民) | `A` |
| SDAY | 給藥天數 | `28` |
| SLABNO | 主診斷 ICD-10 碼 | `E1165` |
| SAMT | 自費金額 | `100` |
| SAMT0 | 部分負擔 | `50` |
| SLAMT | 用途待確認（僅 31 筆，值 300/350） | |
| SAMT98 | 用途待確認（僅 130 筆，值 20/40/60/80/100） | |
| SISRS | 序號 | `001` |
| SSUB | 固定值 01 | `01` |
| SRM4 | 參考編號 | |
| STEXT | 病歷內容 (max 250 字/段) | SOAP 文字 |

**分段儲存機制**：STEXT 每段上限 250 字元，長病歷拆成多筆記錄。
- `SATB='1'` + `STYP='O'`：首段（每次看診必有）
- `SATB='2','3'...` + `STYP=''`：接續段
- 同一次看診以 `KCSTMR + SDATE + STIME` 識別
- 最多可達 14 段（3,500 字元）

**統計**：152,510 筆記錄，72,024 次看診，10,091 位病患。約 48.5% 為單段，51.5% 需串接。

### CO02F - 檢查報告（複合鍵: KCSTMR+FDATE+FTIME+FNO+FSQ）

| 欄位 | 說明 | 範例 |
|------|------|------|
| KCSTMR | 病歷號 | |
| FDATE / FTIME | 日期/時間 | |
| FNO | 報告類型 (P1=心電圖, P2=腹超, P3=甲超, P5/P6=肺功能) | `P2` |
| FTEXT | 報告內容 (max 250 字) | |
| FSQ | 分段序號 | `01` |

### CO03L - 就診記錄（複合鍵: KCSTMR+DATE+TIME）

| 欄位 | 說明 | 範例 |
|------|------|------|
| KCSTMR | 病歷號 | |
| DATE / TIME | 就診日期/時間 | |
| LABNO | 主診斷 ICD | `E11` |
| LABDT | 主診斷中文 | |
| LISRS | 預防保健卡序代碼 | `3D` |
| LPID | 身分別 (A=健保, 9=其他, 空=自費) | `A` |
| LTIME | 完診時間 (000000=未完診) | `150230` |
| DAYQTY | 處方天數 | |

### CO03M - 看診費用（複合鍵: KCSTMR+IDATE+ITIME）

| 欄位 | 說明 |
|------|------|
| LABNO | 主診斷 ICD |
| LACD01~LACD05 | 次要診斷 ICD (最多 5 組) |
| TOT | 總金額 |
| A98 | 部分負擔 |
| RTOT | 申報總額 |

### CO05O - 門診掛號（複合鍵: KCSTMR+TBKDT+TBKTIME）

| 欄位 | 說明 | 範例 |
|------|------|------|
| TBKDT | 掛號日期 | |
| TBKTIME | 掛號時間 | |
| TSTS | 狀態 (0=候診, 1=看診中, E=預約, F=完診, H=取消) | `F` |
| LM | 身分別 | `A` |
| TARTIME | 看診順序號 | `00015` |
| TENDTIME | 完診時間 | |
| TNAME | 姓名 | |

### CO18H - 檢驗報告與生理量測（複合鍵: KCSTMR+HDATE+HITEM）

| 欄位 | 說明 | 範例 |
|------|------|------|
| KCSTMR | 病歷號 | |
| HDATE | 檢驗日期 | `1141127` |
| HITEM | 項目代碼 | `Z0SHbA1c` |
| HDSCP | 項目說明 | `HbA1C,醣化血色素` |
| HVAL | 數值（文字型態） | `6.5` |
| HRESULT | 結果判定 | `偏高` |

### CO09D - 藥品庫存（主鍵: KDRUG）

| 欄位 | 說明 |
|------|------|
| KDRUG | 醫令碼（主鍵） |
| DNO | 健保碼 |
| DDESC / DDESC2 | 英文名 / 中文名 |
| DUM1 | 單位 (錠/顆/瓶) |
| DTYPE | 類別 (02=內服, 03=外用, 04=注射, 12=其他) |
| DP2 | 健保給付價 |
| DQTY2 | 目前庫存量 |
| DORDPOINT | 安全庫存量 |
| DLVENDOR | 供應商 |

### CO09S - 庫存異動

| 欄位 | 說明 |
|------|------|
| KDRUG | 醫令碼 |
| DDATE | 異動日期 |
| DIO | 類型 (5=消耗, B=期初, 2=進貨, 8=調整) |
| DQTY | 異動數量 |
| DAMT | 異動金額 |

### CO10A - 進貨/調整

| 欄位 | 說明 |
|------|------|
| ATYPE | 類型 (2=進貨, 8=調整) |
| KDRUG | 醫令碼 |
| ADATE | 日期 |
| AQTY | 數量 |
| APRICE | 單價 |
| ATOTAL | 總價 |
| AREMARK | 進貨時為有效期限 (西元 YYYYMMDD) |

### VISHFAM - 家醫計畫（主鍵: PAT_PID）

| 欄位 | 說明 |
|------|------|
| PAT_PID | 身分證字號 |
| PAT_NAMEC | 姓名 |
| CASE_TYPE | A=健保收案, B=一般, C=特殊, D=結案 |
| MEMB_TYPE | 會員類型 |
| HBP, ASCVD, BEF, DIS | 健康風險標記 |

---

## 跨表關聯圖

```
CO01M (病患主檔, 主鍵: KCSTMR)
  │
  ├── KCSTMR ──→ CO02M (處方), CO02F (報告), CO02H (病歷SOAP),
  │                CO03L (就診), CO03M (費用), CO05B (預約),
  │                CO05O (掛號), CO18H (檢驗)
  │
  └── MPERSONID ←→ VISHFAM.PAT_PID (身分證關聯)

CO02H ←→ CO02M   以 (KCSTMR + SDATE/IDATE + STIME/ITIME) 關聯病歷與處方
CO02M ←→ CO02F   以 (KCSTMR + DATE + TIME) 關聯處方與檢查報告
CO03L ←→ CO03M   以 (KCSTMR + DATE + TIME) 關聯就診與費用
CO05O ⊃ CO05B    CO05O 為完整掛號，CO05B 為預約子集

CO02M.DNO ──→ CO09D.KDRUG 或 CO09D.DNO (處方→藥品)
CO09D.KDRUG ←── CO09S.KDRUG (庫存異動)
CO09D.KDRUG ←── CO10A.KDRUG (進貨調整)
```

---

## 核心資料慣例

### 日期格式

所有日期欄位為民國年 7 位字串 `YYYMMDD`：
- `西元年 = 民國年 + 1911`
- `1150212` → 民國 115 年 2 月 12 日 → `2026-02-12`
- 因格式固定，**可直接字串比較大小** (`>`, `<`, `BETWEEN`)

### 時間格式

`HHMMSS` 6 位字串，如 `140530` = 14:05:30

### 計算今日民國年日期

```
西元年份 - 1911 → 補零到 3 位 → 接月(2位)日(2位)
2026-02-12 → 115 → '1150212'
```

---

## 檢驗項目代碼速查（CO18H.HITEM）

### 生理量測（無前綴）

| HITEM | 說明 | 格式/單位 |
|-------|------|-----------|
| BP | 血壓 | `收縮壓/舒張壓` 如 `177/97` (mmHg) |
| BT | 體溫 | °C |
| BW | 體重 | kg |
| BH | 身高 | cm |
| BMI | BMI | 數值 |
| HR | 心率 | bpm |
| WC | 腰圍 | cm |
| AC | 飯前血糖(即時) | mg/dL |
| PC | 飯後血糖(即時) | mg/dL |

### 檢驗項目（Z0S 前綴）

| 分類 | HITEM | 說明 |
|------|-------|------|
| **糖尿病** | Z0SHbA1c | 醣化血色素 |
| | Z0SAC | 空腹血糖 |
| | Z0SINS | Insulin |
| | Z0SHOMA | HOMA-IR |
| **腎功能** | Z0SCRE | Creatinine 肌酸酐 |
| | Z0SEGFR | eGFR |
| | Z0SBUN | BUN |
| | Z0SMIA | 微小白蛋白 |
| | Z0SUPCR | 尿蛋白/肌酸酐比值 |
| | Z0SK / Z0SNA | 鉀/鈉離子 |
| **血脂** | Z0SCHO | 總膽固醇 |
| | Z0STG | 三酸甘油脂 |
| | Z0SLDL | LDL-C |
| | Z0SHDL | HDL-C |
| **肝功能** | Z0SGOT | AST |
| | Z0SGPT | ALT |
| | Z0SGGT | r-GT |
| | Z0SALKP | 鹼性磷酸酶 |
| | Z0STBIL / Z0SDBIL | 總/直接膽紅素 |
| | Z0SALB | 白蛋白 |
| **甲狀腺** | Z0STSH | TSH |
| | Z0SFT4 / Z0SFT3 | Free T4 / Free T3 |
| | Z0ST4 / Z0ST3 | T4 / T3 |
| **血液** | Z0SHB | 血色素 |
| | Z0SWBC | 白血球 |
| | Z0SRBC | 紅血球 |
| | Z0SPLT | 血小板 |
| | Z0SMCV / Z0SMCH | MCV / MCH |
| **發炎** | Z0SCRP | CRP |
| | Z0SHSCRP | hs-CRP |
| | Z0SESR | ESR |
| **尿酸** | Z0SUA | Uric Acid |
| **腫瘤標記** | Z0SPSA / Z0SFPSA | PSA / Free PSA |
| | Z0SCEA | CEA |
| | Z0SAFP | AFP |
| **尿液** | Z0SUPRO | 尿蛋白 |
| | Z0SUGLU | 尿糖 |
| | Z0SURBC / Z0SUWBC | 尿紅/白血球 |
| **B/C肝** | Z0SHBEP0~07 | B肝系列 |
| | Z0SHCV / Z0SHCVR | C肝抗體/病毒量 |
| **維生素** | Z0SVITD | Vitamin D |
| | Z0SB12 | Vitamin B12 |
| | Z0SFOL | 葉酸 |
| | Z0SFe / Z0SFER | 鐵/鐵蛋白 |

---

## 代碼對照表

### 疾病管理醫令代碼（CO02M.DNO）

| 分類 | 代碼 | 名稱 |
|------|------|------|
| 糖尿病 | P1406C | 初診 |
| | P1407C | 照護方案 |
| | P1408C | 定期追蹤 |
| | P1409C | 持續追蹤管理 |
| | P1410C | 出院追蹤 |
| | P7001C | DKD-複診 |
| | P7002C | DKD-年度 |
| 腎臟病 | P4301C | CKD 照護 |
| | P4302C | CKD 追蹤 |
| 代謝症候群 | P7501C | 照護 |
| | P7502C | 追蹤 |
| | P7503C | 定期追蹤 |

### 檢查項目代碼（CO02M.DNO ↔ CO02F.FNO）

| 檢查 | DNO 代碼 | FNO 報告代碼 |
|------|---------|-------------|
| 腹部超音波 | 19001C, 19009C | P2 |
| 甲狀腺超音波 | 19012C | P3 |
| 肺功能 | 17003C, 17006C | P5, P6 |
| 細針穿刺 | 15021C | (無) |
| 尿流速 | 21004C | (無) |

### 預防保健代碼（CO03L.LISRS）

| 代碼 | 項目 |
|------|------|
| 3D, 21, 22 | 成人健檢一階 |
| 3E, 23, 24 | 成人健檢二階 |
| 85 | 大腸癌篩檢 |
| 95 | 口腔癌篩檢 |
| AU | 流感疫苗 |
| VU | 新冠疫苗 |
| DU | 肺炎鏈球菌疫苗 |

### 處方頻率（CO02M.PFQ）

QD=日1次, BID=日2次, TID=日3次, QID=日4次, PRN=需要時

### 其他代碼

| 代碼系統 | 欄位 | 值 |
|---------|------|-----|
| 性別 | CO01M.MSEX | 1=男, 2=女 |
| 身分別 | CO03L.LPID / CO05O.LM / CO02H.SLM | A=健保, 9=其他, 1=重大傷病, 3=福保, 4=榮民, 空=自費 |
| 看診狀態 | CO05O.TSTS | 0=候診, 1=看診中, E=預約, F=完診, H=取消 |
| 藥品類別 | CO09D.DTYPE | 02=內服, 03=外用, 04=注射, 12=其他 |
| 庫存異動 | CO09S.DIO | 5=消耗, B=期初, 2=進貨, 8=調整 |
| 進貨類型 | CO10A.ATYPE | 2=進貨, 8=調整 |

---

## 查詢範例模板

以下為 **SQLite 語法**。PostgreSQL 需將表名改小寫、保留字欄位加雙引號、`GROUP_CONCAT` 改 `STRING_AGG`、可用 `DISTINCT ON`。

### 病患搜尋

```sql
-- 依姓名
SELECT KCSTMR, MNAME, MSEX, MBIRTHDT, MPERSONID FROM CO01M WHERE MNAME LIKE '%王%';
-- 依身分證
SELECT KCSTMR, MNAME FROM CO01M WHERE MPERSONID = 'A123456789';
-- 依病歷號
SELECT * FROM CO01M WHERE KCSTMR = '0000024';
```

### 就診歷史

```sql
SELECT DATE, TIME, LABNO, LABDT, LISRS, LTIME, DAYQTY
FROM CO03L WHERE KCSTMR = ? ORDER BY DATE DESC, TIME DESC LIMIT 10;
```

### 特定 ICD 診斷的病患

```sql
SELECT DISTINCT c.KCSTMR, m.MNAME, c.DATE, c.LABNO
FROM CO03L c JOIN CO01M m ON c.KCSTMR = m.KCSTMR
WHERE c.LABNO LIKE 'E11%'  -- 第二型糖尿病
ORDER BY c.DATE DESC;
```

### 處方（含藥品名稱）

```sql
SELECT m.KCSTMR, p.MNAME, m.IDATE, m.DNO, d.DDESC, d.DDESC2, m.PTDAY, m.PTQTY
FROM CO02M m
JOIN CO01M p ON m.KCSTMR = p.KCSTMR
JOIN CO09D d ON m.DNO = d.KDRUG OR m.DNO = d.DNO
WHERE d.DDESC LIKE '%METFORMIN%'
ORDER BY m.IDATE DESC;
```

### 檢驗趨勢

```sql
SELECT HDATE, HITEM, HDSCP, HVAL, HRESULT
FROM CO18H WHERE KCSTMR = ? AND HITEM = 'Z0SHbA1c'
ORDER BY HDATE DESC;
```

### 最近一次各項檢驗結果（SQLite）

```sql
SELECT h.HITEM, h.HDSCP, h.HVAL, h.HRESULT, h.HDATE
FROM CO18H h
WHERE h.KCSTMR = ?
  AND h.HITEM LIKE 'Z0S%'
  AND h.HDATE = (
    SELECT MAX(h2.HDATE) FROM CO18H h2
    WHERE h2.KCSTMR = h.KCSTMR AND h2.HITEM = h.HITEM
  )
ORDER BY h.HITEM;
```

### 檢驗異常篩選

```sql
SELECT h.KCSTMR, m.MNAME, h.HDATE, h.HVAL, h.HRESULT
FROM CO18H h JOIN CO01M m ON h.KCSTMR = m.KCSTMR
WHERE h.HITEM = 'Z0SHbA1c' AND CAST(h.HVAL AS REAL) >= 7.0
ORDER BY CAST(h.HVAL AS REAL) DESC;
```

### 病歷紀錄查詢（CO02H SOAP Notes 合併）

```sql
-- 查詢某病患某次看診的完整 SOAP 病歷（合併分段）
SELECT GROUP_CONCAT(STEXT, '') AS SOAP_NOTE
FROM (
  SELECT STEXT FROM CO02H
  WHERE KCSTMR = ? AND SDATE = ? AND STIME = ?
  ORDER BY SATB ASC
);

-- 查詢某病患所有看診的完整病歷列表
SELECT
    KCSTMR,
    SDATE,
    STIME,
    MAX(CASE WHEN SATB = '1' THEN SID END) AS DOCTOR,
    MAX(CASE WHEN SATB = '1' THEN SLM END) AS IDENTITY,
    MAX(CASE WHEN SATB = '1' THEN SLABNO END) AS ICD10,
    MAX(CASE WHEN SATB = '1' THEN SDAY END) AS DAYS,
    GROUP_CONCAT(STEXT, '') AS SOAP_NOTE
FROM (
    SELECT * FROM CO02H WHERE KCSTMR = ?
    ORDER BY SDATE DESC, STIME DESC, SATB ASC
)
GROUP BY KCSTMR, SDATE, STIME
ORDER BY SDATE DESC, STIME DESC;

-- 搜尋病歷內容含特定關鍵字的記錄
SELECT DISTINCT KCSTMR, SDATE, STIME
FROM CO02H
WHERE STEXT LIKE '%diabetes%' OR STEXT LIKE '%DM%'
ORDER BY SDATE DESC;

-- 病歷 + 處方聯合查詢（同一次看診的 SOAP + 用藥）
SELECT
    h.KCSTMR,
    h.SDATE,
    h.SOAP_NOTE,
    GROUP_CONCAT(d.DDESC || ' ' || m.PFQ || ' x' || m.PTDAY || 'd', ', ') AS MEDICATIONS
FROM (
    SELECT KCSTMR, SDATE, STIME,
           GROUP_CONCAT(STEXT, '') AS SOAP_NOTE
    FROM (SELECT * FROM CO02H ORDER BY SATB ASC)
    GROUP BY KCSTMR, SDATE, STIME
) h
LEFT JOIN CO02M m ON h.KCSTMR = m.KCSTMR AND h.SDATE = m.IDATE AND h.STIME = m.ITIME
LEFT JOIN CO09D d ON m.DNO = d.KDRUG OR m.DNO = d.DNO
WHERE h.KCSTMR = ?
GROUP BY h.KCSTMR, h.SDATE, h.STIME
ORDER BY h.SDATE DESC;
```

**PostgreSQL 版本差異**：
```sql
-- PostgreSQL 中 GROUP_CONCAT → STRING_AGG，且需明確 ORDER BY
SELECT
    "kcstmr", "sdate", "stime",
    STRING_AGG("stext", '' ORDER BY "satb" ASC) AS soap_note
FROM co02h
WHERE "kcstmr" = $1
GROUP BY "kcstmr", "sdate", "stime"
ORDER BY "sdate" DESC, "stime" DESC;
```

### 檢查報告（合併多段）

```sql
SELECT GROUP_CONCAT(FTEXT, '') as FULL_REPORT
FROM (
  SELECT FTEXT FROM CO02F
  WHERE KCSTMR = ? AND FDATE = ? AND FNO = 'P2'
  ORDER BY FSQ ASC
);
```

### 血壓異常

```sql
SELECT h.KCSTMR, m.MNAME, h.HDATE, h.HVAL
FROM CO18H h JOIN CO01M m ON h.KCSTMR = m.KCSTMR
WHERE h.HITEM = 'BP'
  AND (CAST(SUBSTR(h.HVAL, 1, INSTR(h.HVAL, '/') - 1) AS INTEGER) >= 140
    OR CAST(SUBSTR(h.HVAL, INSTR(h.HVAL, '/') + 1) AS INTEGER) >= 90)
ORDER BY h.HDATE DESC;
```

### 預防保健未做追蹤

```sql
-- 超過一年未做成人健檢的家醫計畫病患
SELECT v.PAT_PID, v.PAT_NAMEC, m.KCSTMR, MAX(l.DATE) as LAST_CHECKUP
FROM VISHFAM v
JOIN CO01M m ON v.PAT_PID = m.MPERSONID
LEFT JOIN CO03L l ON m.KCSTMR = l.KCSTMR AND l.LISRS IN ('3D','21','22','3E','23','24')
WHERE v.CASE_TYPE IN ('A', 'B')
GROUP BY v.PAT_PID
HAVING LAST_CHECKUP IS NULL OR LAST_CHECKUP < '1140212';
```

### 低庫存藥品

```sql
SELECT KDRUG, DDESC, DDESC2, DQTY2, DORDPOINT, DLVENDOR
FROM CO09D WHERE DQTY2 <= DORDPOINT AND DQTY2 > 0
ORDER BY (DQTY2 / NULLIF(DORDPOINT, 0)) ASC;
```

### 藥品月消耗量

```sql
SELECT KDRUG, SUM(DQTY) as MONTHLY_CONSUMPTION
FROM CO09S WHERE DIO = '5' AND DDATE LIKE '11501%'  -- 115年01月
GROUP BY KDRUG ORDER BY MONTHLY_CONSUMPTION ASC;
```

---

## 查詢陷阱 (Gotchas)

1. **HVAL 是文字** — 數值比較必須 `CAST(HVAL AS REAL)`；血壓 (BP) 格式為 `收縮壓/舒張壓`，需用 `SUBSTR`+`INSTR` 拆分
2. **CO02F 報告分段** — 超過 250 字元拆成多筆 (FSQ 序號)，查詢必須合併
3. **CO02H 病歷分段** — STEXT 每段上限 250 字元，按 SATB 序號排序合併。同一次看診以 `KCSTMR+SDATE+STIME` 識別。SLM/SDAY/SLABNO 等欄位僅在首段 (`SATB='1'`) 有意義
4. **SQLite 無 DISTINCT ON** — 用 `GROUP BY` + `MAX()` 或相關子查詢替代
5. **CO02M.DNO 多義性** — 可能是藥品碼、檢查碼或疾病管理碼，依前綴判斷
6. **CO02M → CO09D 關聯** — `DNO` 可能對應 `KDRUG` 或 `DNO`，JOIN 需 `OR`
7. **PostgreSQL 保留字** — co03l 的 `date`, `time`, `case` 欄位需用雙引號
8. **CO09S.DDATE 特殊格式** — 期初庫存為 `YYYMM**`，系統記錄為 `@@`，過濾時注意
9. **CO10A.AREMARK** — 進貨時為有效期限（西元 `YYYYMMDD`），調整時通常為空

---

## 適用情境範例

**情境 1：建立糖尿病管理儀表板**
→ CO03L (LABNO LIKE 'E1%') 找糖尿病患者
→ CO18H (HITEM IN Z0SHbA1c, Z0SAC, Z0SCRE, Z0SEGFR...) 檢驗數據
→ CO02M (DNO IN P1406C~P1410C) 照護追蹤記錄
→ CO01M 病患基本資料

**情境 2：藥品庫存管理系統**
→ CO09D 藥品主檔與庫存
→ CO09S 庫存異動歷程
→ CO10A 進貨記錄與效期
→ CO02M 處方消耗分析

**情境 3：預防保健追蹤提醒**
→ VISHFAM 家醫計畫成員
→ CO01M (MPERSONID = PAT_PID) 關聯病歷號
→ CO03L (LISRS) 預防保健記錄
→ CO18H 生理量測數據

**情境 4：病歷紀錄查詢與分析**
→ CO02H (STEXT) 醫師 SOAP 病歷內容（需按 SATB 合併分段）
→ CO01M 病患基本資料
→ CO02M + CO09D 同次看診的處方用藥
→ CO02H.SLABNO 主診斷 ICD-10 碼

**情境 5：門診即時看板**
→ CO05O (TBKDT=今日) 今日掛號
→ CO01M 病患基本資料
→ CO03L 歷史就診資訊
