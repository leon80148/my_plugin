# 庫存系統詳細參考

> 來源：WHI.EXE 庫存管理模組交班文件（Visual FoxPro）。
> 本文件涵蓋庫存計算邏輯、系統參數、報表程式、月結檔結構，
> 以及 SKILL.md 中未展開的進階欄位與查詢模式。

## 系統架構

WHI.EXE 是 HIS 系統中的**庫存管理模組**，負責藥品/耗材的進銷存管理。
核心報表程式位於 `INV_RPT\` 目錄。

### 報表程式索引

| 函式 | 檔案 | 報表標題 |
|------|------|---------|
| `P_INV_21` | `INV21P0.INP` | 存貨報表 / 月異動狀況表 |
| `P_INV_22` | `INV22P0.INP` | 各類單據異動明細表 |
| `P_INV_26` | `INV26P0.INP` | 產品別耗用統計表 / 排行表 |
| `P_INV_27` | `INV27P0.INP` | 產品別耗用明細表 |
| `P_INV_28` | `INV28P0.INP` | 醫師別耗用統計表 / 排行表 |
| `P_INV_29` | `INV29P0.INP` | 安全存量明細表 |
| `P_INV_2A` | `INV2AP0.INP` | 醫療費用日報表 |
| `P_INV_2B` | `INV2BP0.INP` | 產品別未耗用統計表 |
| `P_INV_2C` | `INV2CP0.INP` | **產品別月異動統計表** |
| `P_INV_43` | `INV43P0.INP` | 盤點明細表 |
| `P_INV_44` | `INV44P0.INP` | 盤盈虧明細表 |
| `P_INV_46RPT` | `INV461P0.INP` | **存貨月報表**（標準/固定格式） |
| `P_INV_46RPT` | `INV462P0.INP` | **存貨月報表**（基隆礦工醫院專用版） |

---

## 系統參數（VISI0.VIS）

### 異動類型代碼

| 參數名稱 | 值 | 說明 |
|---------|-----|------|
| `C__I_STO_ATYPE` | `"2I"` | **進貨單據**（`"2"` 或 `"I"`） |
| `C__I_CON_ATYPE` | `"5O"` | **出貨單據**（`"5"` 或 `"O"`） |
| `C__I_ST1_ATYPE` | `"4"` | **貨退廠商單據** |
| `C__I_CO1_ATYPE` | `"3"` | **客戶退回單據** |
| `C__I_PIO_ATYPE` | `"678"` | **庫存單據**（6=撥入, 7=撥出, 8=調整） |
| `C__I_ADJ_ATYPE` | `"8"` | **庫存調整項目** |
| `C__I_BEGIN` | `"B"` | **庫存期初量之異動別代號**（CO09S.DIO 的值） |

### 報表與計算參數

| 參數名稱 | 值 | 說明 |
|---------|-----|------|
| `N__I_OPEN` | `1` | 庫存每月開帳基準日 |
| `L__I_OPENFIX` | `.T.` | 開帳基準日是否固定 |
| `N__I_QTY_DECIMAL` | `1` | 存貨月報數量小數位數 |
| `N__I_AMT_DECIMAL` | `0` | 存貨月報金額小數位數 |
| `C__I_PRICE` | `"0"` | 報表單價：`"0"`=平均成本, `"1"`=末進價, `"2"`=健保價, `"3"`=歷次進價 |
| `C__I_AMT` | `"0"` | 金額計算：`"0"`=期初+進貨-期末=出貨, `"1"`=期初+進貨-出貨=期末 |
| `L__I_AIR` | `.F.` | 空總專用月異動報表 |
| `L__I_MRPTFIX` | `.F.` | 存貨月報是否固定格式 |

### 藥品分類代碼（CO09D.DTYPE）

| 代碼 | 分類 | 代碼 | 分類 |
|------|------|------|------|
| 1 | 診察 | 11 | 麻醉 |
| 2 | 內服 | 12 | 材料 |
| 3 | 外用 | 13 | 輸血 |
| 4 | 注射 | 14 | 透析 |
| 5 | 注技 | 15 | 病房 |
| 6 | 檢驗 | 16 | 膳食 |
| 7 | Ｘ光 | 17 | 嬰兒 |
| 8 | 理療 | 18 | 經療 |
| 9 | 處置 | 19 | 代辦 |
| 10 | 手術 | 99 | 藥事 |

> 存貨月報表預設篩選 `VAL(DTYPE) IN(2,3,4,12)`（內服、外用、注射、材料）。

---

## 完整資料表 Schema

### CO10P - 異動類型定義檔

> 記錄數僅 3 筆，定義庫存異動類型的代碼、名稱及增減方向

| 欄位 | 型態 | 說明 |
|------|------|------|
| PTYP1 | C(1) | **異動類型代碼**（主鍵），與 CO10A.ATYPE 及 CO09S.DIO 關聯 |
| PTITL | C(20) | **異動類型名稱**（報表取前 4 字元顯示） |
| PQTY | C(1) | **數量方向**：`"+"`=入庫增加, `"-"`=出庫減少 |
| PCM | C(1) | — |
| PDR / PCR | C(10) | — |
| PINC | C(1) | — |
| PUNIT | C(1) | — |
| PRIC / PAP / PAR | C(1) | — |
| PTR | C(2) | — |
| PSQ | C(1) | — |

> 存貨月報表會將所有異動類型讀入陣列 `COPY ALL TO ARRAY PP FIELDS PTYP1,PTITL,PQTY`，
> 動態產生報表的各類異動欄位標題。

### CO02P - 交易明細檔（藥局調劑）

> 記錄數約 288,927 筆。是產品別月異動統計表（P_SG_I2CA）計算每日異動量的主要來源。
> **注意**：此表與 CO02M（處方記錄）不同，CO02P 記錄的是藥局端的實際調劑/交易明細。

| 欄位 | 型態 | 說明 |
|------|------|------|
| KCSTMR | C(7) | 客戶代碼 |
| PDATE | C(7) | **交易日期**（YYYMMDD，民國年） |
| PTIME | C(6) | 交易時間（HHMMSS） |
| PLM / PRMK / PCLM | C(1) | — |
| KDRUG | C(6) | **藥品代碼** |
| PTP | N(2) | — |
| PTYPE | C(1) | — |
| PQTY | N(9,3) | — |
| POQTY | N(9,3) | — |
| PTQTY | N(9,2) | **異動數量**（實際扣庫量，含正負號） |
| PPR | N(9,2) | — |
| PFQ | C(10) | — |
| PSDT / PEDT | C(7) | — |
| DBCODE | C(20) | 條碼 |

**索引**: `CO02P.CDX` — 主要 TAG: `PDATE`

### CO14M - 庫位/廠商主檔

> 記錄數約 85 筆。記錄倉庫/庫位/廠商基本資料。

| 欄位 | 型態 | 說明 |
|------|------|------|
| MTYPE | C(1) | **庫位類型**：`'1'`=主要, `'3'`=倉庫 |
| MNO | C(7) | **庫位/廠商代碼**（與 MTYPE 合為複合主鍵） |
| MNAME | C(26) | **名稱** |
| MATT | C(10) | — |
| MBUSINO | C(10) | 統一編號 |
| MTEL1 / MTEL2 | C(15) | 電話 |
| MADDR1 / MADDR2 | C(40) | 地址 |
| MREMARK | C(254) | 備註 |
| MFAX | C(20) | 傳真 |
| MEMAIL | C(30) | 電郵 |
| MPD | C(1) | — |
| MKIND | C(2) | — |
| MDIS | N(2) | — |
| MDISC | C(20) | — |
| MDRUGLIC | C(14) | 藥商執照號碼 |

**索引**: `CO14M.CDX` — TAG: `MNO`（複合 `MTYPE+MNO`）

### CO09D - 藥品主檔（擴充欄位）

以下列出 SKILL.md 未收錄的重要欄位（完整 Schema 共 102 個欄位）：

| 欄位 | 型態 | 說明 |
|------|------|------|
| DPRICE | N(15,3) | 單價（存貨月報使用） |
| DLPRI | N(15,3) | **末進價**（最後一次進貨單價） |
| DSTS | C(1) | **狀態**：`'*'`=停用 |
| DBCODE | C(20) | **條碼** |
| KNO | C(12) | **健保碼**（與 DNO 不同，DNO 為 C(12) 的藥品編號） |
| DGRP | C(12) | 群組碼（存貨月報篩選用） |
| DGROUP | C(30) | 群組名稱 |
| DRESET | C(11) | 重設/啟用日期（用於篩選有效品項） |
| DTP1 | C(2) | 藥品分類屬性 1 |
| DTP5 | C(2) | 藥品分類屬性 5（報表篩選用） |
| DSITEM | C(2) | **自費分類**（報表篩選用） |
| DPLACE | C(2) | 儲位代碼 |
| DPMIN / DPMINP | N(15,3) | — |
| DORDQTY | N(15,3) | — |
| DESTQTY | N(15,3) | — |
| COSTPRI | N(15,3) | — |
| DUM2 | C(3) | 單位（另一組） |
| DUM3 | C(4) | 單位（第三組） |
| MUL3 | N(15,3) | — |
| DNOP | C(15) | — |
| DATC | C(7) | ATC 碼 |
| DP1~DP5 | N(15,3) | 各組價格 |
| DLDPDT | C(7) | 價格切換日期 |
| ACCSUBJ | C(10) | 會計科目 |

**索引**: `CO09D.CDX` — 主要 TAG: `KDRUG`

### CO09S - 庫存餘額檔（擴充說明）

> 記錄數約 117,096 筆。記錄長度 41 bytes。

完整欄位（僅 6 個）：

| 欄位 | 型態 | 說明 |
|------|------|------|
| DLCT | C(1) | **庫位**：`'O'`=本庫, `'D'`=其他庫位，空白視為 `'O'` |
| KDRUG | C(6) | **藥品代碼** |
| DDATE | C(7) | **異動日期**（YYYMMDD，民國年） |
| DIO | C(1) | **異動類型**（對應 CO10P.PTYP1）：`'B'`=期初, `'2'`=進貨, `'5'`=出貨, `'@'`=作廢排除 |
| DQTY | N(10,3) | **庫存數量** |
| DAMT | N(15,3) | 庫存金額 |

**複合索引**: `DLCT+KDRUG+DDATE+...+DIO`

**期初存量 SEEK 語法**（FoxPro）：
```
SEEK 'O' + KDRUG + 月初日期 + '**B' IN CO09S
```
- `'O'` = DLCT 庫位（本庫）
- `'B'` = DIO 類型（期初餘額）

### CO10A - 庫存異動交易檔（擴充欄位）

> 記錄數約 2,898 筆。

| 欄位 | 型態 | 說明 |
|------|------|------|
| ATYPE | C(1) | **異動類型**（對應 CO10P.PTYP1） |
| KDONO | C(7) | **單據號碼** |
| ADATE | C(7) | **異動日期**（YYYMMDD） |
| MTYPE | C(1) | 庫位類型（與 MNO 合併對應 CO14M） |
| RNO | C(7) | 空白時預設為 `'O'` |
| MNO | C(7) | **庫位代碼**（對應 CO14M.MNO） |
| KDRUG | C(6) | **藥品代碼** |
| AQTY | N(15,3) | **異動數量**（正負方向由 CO10P.PQTY 決定） |
| APRICE | N(15,3) | **單價** |
| ATOTAL | N(15,3) | **異動金額** |
| AREMARK | C(40) | 備註（進貨時為有效期限，西元 YYYYMMDD） |
| AITEM | C(2) | 項次 |
| AUM | C(3) | 單位 |
| VDATE | C(7) | — |

**索引**: `CO10A.CDX` — 主要 TAG: `ADATE`

### CO9Dxxxx.DBF - 月結成本結算檔

> 由「成本結算作業」(`VISI_CREATECO9D()`) 產生。
> 檔名規則：`CO9D` + 年月代碼（由 `VISI_DTYMM5("CO9D", C_ITE1)` 產生）

| 欄位 | 說明 |
|------|------|
| KDRUG | 藥品代碼 |
| DLCT | 庫位 |
| DPRICE | 單價 |
| QTYBB | **期初存貨**（數量） |
| AMTBB | **期初金額** |
| QTYEE | **本期結存**（數量） |
| AMTEE | **結存金額** |
| 各異動類型欄位 | 由 CO10P 動態產生（數量+金額成對） |

---

## 庫存計算邏輯

### 存貨月報表公式（P_SG_I46）

存貨月報表讀取**月結檔** `CO9Dxxxx.DBF`，不做即時計算。

報表欄位結構：
```
藥代 + 藥品名稱 + 單位 + 單價 + 期初存貨 + 期初金額
  + [各異動類型數量+金額] + 本期結存 + 結存金額 + 末進價
```

金額計算方向（`C__I_AMT`）：
- `"0"`（預設）：出貨 = 期初 + 進貨 - 期末
- `"1"`：期末 = 期初 + 進貨 - 出貨

### 產品別月異動統計表公式（P_SG_I2CA）

即時從交易明細計算，核心公式：

```
期末存量 = 期初存量 + 進貨庫存調整量 - 交易異動量
EQTY    = BQTY     + IQTY            - OQTY
```

計算步驟：

**步驟 1：取得期初存量 (BQTY)**
- 來源：CO09S（庫存餘額檔）
- 查找方式：`SEEK 'O' + KDRUG + 月初日期 + '**B' IN CO09S`
- 取 CO09S.DQTY 作為 BQTY

**步驟 2：取得進貨庫存調整量 (IQTY)**
- 來源：CO10A（庫存異動交易檔）
- 查詢月初日期當天的進貨類型異動總量：
  ```sql
  SELECT SUM(AQTY) FROM CO10A
  WHERE KDRUG = ? AND ADATE = 月初日期 AND ATYPE IN ('2', 'I')
  ```

**步驟 3：累計每日交易異動量 (OQTY + Q01~Q31)**
- 來源：CO02P（交易明細檔）
- 逐筆掃描月份內所有交易，按日累加 PTQTY 到對應的 Q01~Q31 欄位
- 同時累加到 OQTY 總計

**步驟 4：計算期末存量 (EQTY)**
- `EQTY = BQTY + IQTY - OQTY`

### 計算流程圖

```
輸入: 年月 (C_ITE1)
  │
  ▼
VISI_DTAREA() → 計算月初(C_DT1)、月底(C_DT2)
  │
  ▼
開啟表單: CO09D, CO09S, CO02P, CO10A
  │
  ▼
SEEK C_ITE1 IN CO02P  (定位到月初)
  │
  ▼
┌── SCAN CO02P (PDATE <= C_DT2) ──┐
│                                   │
│  ① 篩選藥品分類 (DTYPE/DSITEM)   │
│  ② SEEK KDRUG IN AA              │
│     ├─ 新藥品 → 取 BQTY + IQTY  │
│     └─ 已存在                     │
│  ③ 累加 Q{dd} += PTQTY           │
│     OQTY += PTQTY                 │
│                                   │
└───────────────────────────────────┘
  │
  ▼
SCAN AA → EQTY = BQTY + IQTY - OQTY
  │
  ▼
輸出報表 / 匯出 EXCEL
```

---

## 目前庫存查詢方法

### 方法一：直接查 CO09S（簡易加總）

```sql
SELECT S.KDRUG       AS 藥品代碼,
       D.DDESC       AS 藥品名稱,
       D.DUM1        AS 單位,
       SUM(S.DQTY)   AS 目前庫存
  FROM CO09S S
  JOIN CO09D D ON S.KDRUG = D.KDRUG
 WHERE S.DIO <> '@'        -- 排除作廢
   AND S.DLCT = 'O'        -- 本庫
 GROUP BY S.KDRUG, D.DDESC, D.DUM1;
```

### 方法二：期初 + 異動計算

```sql
SELECT D.KDRUG                                    AS 藥品代碼,
       D.DDESC                                    AS 品名,
       D.DUM1                                     AS 單位,
       COALESCE(B.BQTY, 0)                        AS 期初存量,
       SUM(CASE WHEN P.PQTY = '+' THEN A.AQTY ELSE 0 END) AS 入庫合計,
       SUM(CASE WHEN P.PQTY = '-' THEN A.AQTY ELSE 0 END) AS 出庫合計,
       COALESCE(B.BQTY, 0)
         + SUM(CASE WHEN P.PQTY = '+' THEN A.AQTY ELSE 0 END)
         - SUM(CASE WHEN P.PQTY = '-' THEN A.AQTY ELSE 0 END) AS 目前庫存
  FROM CO09D D
  LEFT JOIN (
      SELECT KDRUG, DQTY AS BQTY
        FROM CO09S
       WHERE DIO = 'B' AND DDATE = '期初日期'
  ) B ON D.KDRUG = B.KDRUG
  LEFT JOIN CO10A A ON D.KDRUG = A.KDRUG AND A.ADATE >= '期初日期'
  LEFT JOIN CO10P P ON A.ATYPE = P.PTYP1
 GROUP BY D.KDRUG, D.DDESC, D.DUM1, B.BQTY;
```

### 存貨月報表查詢（需月結檔存在）

```sql
-- 查詢某月份的存貨月報（讀取 CO9Dxxxx.DBF 月結檔）
SELECT D.KDRUG, D.DDESC, D.DUM1, D.DPRICE,
       M.QTYBB AS 期初數量, M.AMTBB AS 期初金額,
       M.QTYEE AS 結存數量, M.AMTEE AS 結存金額,
       D.DLPRI AS 末進價
FROM CO9Dxxxx M
JOIN CO09D D ON M.KDRUG = D.KDRUG
WHERE D.DSTS <> '*'                    -- 排除停用
  AND VAL(D.DTYPE) IN (2, 3, 4, 12)   -- 內服/外用/注射/材料
ORDER BY D.KDRUG;
```

### 進銷存月報查詢

```sql
-- 某月份各藥品的進/出/調整彙總
SELECT D.KDRUG, D.DDESC2 AS 藥品名稱, D.DUM1 AS 單位,
       SUM(CASE WHEN A.ATYPE IN ('2','I') THEN A.AQTY ELSE 0 END) AS 進貨量,
       SUM(CASE WHEN A.ATYPE IN ('5','O') THEN A.AQTY ELSE 0 END) AS 出貨量,
       SUM(CASE WHEN A.ATYPE = '4' THEN A.AQTY ELSE 0 END)        AS 退貨量,
       SUM(CASE WHEN A.ATYPE = '3' THEN A.AQTY ELSE 0 END)        AS 客退量,
       SUM(CASE WHEN A.ATYPE = '8' THEN A.AQTY ELSE 0 END)        AS 調整量
FROM CO10A A
JOIN CO09D D ON A.KDRUG = D.KDRUG
WHERE A.ADATE BETWEEN '1150301' AND '1150331'  -- 替換為目標月份
GROUP BY D.KDRUG, D.DDESC2, D.DUM1
ORDER BY D.KDRUG;
```

### 庫存異動明細（含單據與廠商）

```sql
SELECT A.ADATE AS 日期,
       A.KDONO AS 單號,
       P.PTITL AS 異動類型,
       D.DDESC2 AS 藥品名稱,
       CASE WHEN P.PQTY = '+' THEN A.AQTY ELSE -A.AQTY END AS 異動量,
       A.APRICE AS 單價,
       A.ATOTAL AS 金額,
       M.MNAME AS 廠商/庫位,
       A.AREMARK AS 備註
FROM CO10A A
JOIN CO09D D ON A.KDRUG = D.KDRUG
JOIN CO10P P ON A.ATYPE = P.PTYP1
LEFT JOIN CO14M M ON A.MTYPE = M.MTYPE AND A.MNO = M.MNO
WHERE A.KDRUG = ?
ORDER BY A.ADATE DESC;
```

---

## 表單關聯圖（庫存子系統）

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  CO09D   │         │  CO10A   │         │  CO10P   │
│ 藥品主檔  │◄────────│ 庫存異動  │────────►│ 異動類型  │
│          │ KDRUG   │          │ ATYPE   │          │
│ .KDRUG   │         │ .KDRUG   │ =       │ .PTYP1   │
│ .DDESC   │         │ .ATYPE   │         │ .PTITL   │
│ .DUM1    │         │ .ADATE   │         │ .PQTY    │
│ .DTYPE   │         │ .AQTY    │         │ (+/-)    │
│ .DSTS    │         │ .ATOTAL  │         └──────────┘
│ .DLPRI   │         │ .MNO     │
│ .DBCODE  │         │ .MTYPE   │
│ .KNO     │         │ .KDONO   │
└────┬─────┘         └────┬─────┘
     │                    │ MTYPE+MNO
     │               ┌────▼─────┐
     │               │  CO14M   │
     │               │ 庫位/廠商 │
     │               │ .MNO     │
     │               │ .MNAME   │
     │               │ .MTYPE   │
     │               └──────────┘
     │
     │ KDRUG
┌────▼─────┐         ┌──────────┐        ┌────────────┐
│  CO09S   │         │  CO02P   │        │ CO9Dxxxx   │
│ 庫存餘額  │         │ 交易明細  │        │ 月結成本檔  │
│          │         │(藥局調劑) │        │            │
│ .DLCT    │         │ .PDATE   │        │ .QTYBB     │
│ .KDRUG   │◄────────│ .KDRUG   │        │ .AMTBB     │
│ .DDATE   │         │ .PTQTY   │        │ .QTYEE     │
│ .DIO     │         │ .KCSTMR  │        │ .AMTEE     │
│ .DQTY    │         └──────────┘        │ .DPRICE    │
│ .DAMT    │                              │ .DLCT      │
└──────────┘                              └────────────┘
```

---

## 注意事項

1. **PTQTY vs AQTY 方向性**：CO02P.PTQTY 是實際扣庫量（含正負號），CO10A.AQTY 是絕對數量（正負由 CO10P.PQTY 決定）
2. **存貨月報表需先結算**：`P_SG_I46` 讀取月結檔 `CO9Dxxxx.DBF`，必須先執行 `VISI_CREATECO9D()` 才能產生。若不存在，系統提示「成本結算檔案不存在」
3. **CO10P 只有 3 筆記錄**：異動類型較少，大部分邏輯由 `C__I_*_ATYPE` 系統參數控制
4. **CO09S 複合鍵**：索引順序為 `DLCT+KDRUG+DDATE+...+DIO`，查詢必須按此順序組合
5. **DLCT 庫位**：`'O'`=本庫，空白也視為本庫，`'D'`=其他庫位
6. **MEM 設定檔**：報表設定存入 `SPCI2C0.MEM` / `SPCI460.MEM`，下次開啟自動還原
7. **DTYPE 對應**：SKILL.md 中的 `02=內服, 03=外用, 04=注射` 是零補位格式，VISI0.VIS 中的原始值為 `2, 3, 4, 12`（無零補位），使用 `VAL(DTYPE)` 轉數值比對
8. **CO14M JOIN 條件**：必須用 `MTYPE+MNO` 複合鍵，不能只用 MNO
