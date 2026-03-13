# 進階主題

## 資料匿名化指南

在匯出資料供研究或外部分析時，必須先匿名化個人識別資訊（PII）。

### 匿名化欄位對照

| 欄位 | 原始值 | 匿名化方式 | 匿名化後範例 |
|------|--------|-----------|------------|
| KCSTMR（病患碼） | `0000024` | 隨機對應表 | `PAT_A7X9K2` |
| 身分證字號 | `A123456789` | SHA-256 雜湊 | `a8f5f167...` |
| 姓名 | `王大明` | 替換為假名 | `匿名病患 024` |
| 生日 | `0750315` | 年份模糊化（±2年） | `0770000` |
| 地址 | 完整地址 | 只保留縣市 | `台北市` |
| 電話 | `0912345678` | 遮罩 | `0912***678` |

### 匿名化原則

1. **不可逆**：用於外部分享的資料必須不可逆匿名化
2. **一致性**：同一病患在不同表格中的匿名化 ID 必須一致
3. **保留分析價值**：日期可模糊化但應保留就診間隔
4. **最小揭露**：只輸出分析所需的最少欄位

### 實作範例（SQLite）

```sql
-- 建立匿名化對應表（一次性建立）
CREATE TABLE anon_map AS
SELECT KCSTMR, 'PAT_' || UPPER(HEX(RANDOMBLOB(3))) AS anon_id FROM CO01M;

-- 匿名化匯出（保留分析所需欄位）
SELECT
    a.anon_id as patient_id,
    SUBSTR(m.MBIRTHDT, 1, 3) || '0000' as approx_birth,  -- 只保留年份
    CASE WHEN m.MSEX = '1' THEN 'M' ELSE 'F' END as sex,
    l.DATE as visit_date,
    l.LABNO as icd_code
FROM CO01M m
JOIN anon_map a ON m.KCSTMR = a.KCSTMR
JOIN CO03L l ON m.KCSTMR = l.KCSTMR
ORDER BY a.anon_id, l.DATE;
```

---

## VISHFAM 系統補充說明

> ⚠️ **重要說明**：以下 Schema 描述的是 **VISHFAM 系統**（家醫照護管理平台），
> 與展望 HIS 核心資料庫的欄位名稱和結構有所不同。
>
> 例如：VISHFAM 系統中的 CO03L 包含 `MEM1`~`MEM4` 欄位（SOAP 分欄位），
> 但展望 HIS 的 CO03L 是就診記錄（含 LABNO, LABDT 等），SOAP 是 CO02H.STEXT。
>
> 若您同時使用兩套系統，請確認您正在連接的是哪個資料庫。

### VISHFAM 核心資料表

```
CSTMR（病患主檔）
├── CO03L（門診記錄）← KCSTMR
│   ├── MEM1: Subjective（主訴）
│   ├── MEM2: Objective（理學檢查）
│   ├── MEM3: Assessment（評估/診斷）
│   ├── MEM4: Plan（處置計畫）
│   ├── ICD1-ICD5: 診斷碼
│   └── DOCTOR: 看診醫師代碼
├── CO04L（處方明細）← KCSTMR + DATE
├── CO05L（檢驗結果）← KCSTMR
├── CO06L（影像報告）← KCSTMR
└── CO07L（過敏記錄）← KCSTMR
```

### VISHFAM 跨表查詢模式

```sql
-- 查詢病患的完整就診紀錄（門診 + 處方 + 檢驗）
SELECT
  c.DATE AS 就診日期,
  c.MEM3 AS 診斷,
  GROUP_CONCAT(DISTINCT p.KNAME) AS 藥品,
  GROUP_CONCAT(DISTINCT l.ITEM || ':' || l.RESULT) AS 檢驗
FROM CO03L c
LEFT JOIN CO04L p ON c.KCSTMR = p.KCSTMR AND c.DATE = p.DATE
LEFT JOIN CO05L l ON c.KCSTMR = l.KCSTMR AND c.DATE = l.DATE
WHERE c.KCSTMR = '0000024'
GROUP BY c.DATE, c.MEM3
ORDER BY c.DATE DESC;
```

> **注意**：VISHFAM 的 CO04L、CO05L、CO06L、CO07L 在展望核心 HIS 中對應的是 CO02M、CO18H、CO02F 等表格，
> 欄位名稱完全不同。跨系統查詢時請特別謹慎。

---

## 跨資料表 JOIN 常見模式

展望 HIS 核心資料庫最常用的 JOIN 組合和適用場景。

### 病患 + 就診 + 處方（最常用的三表 JOIN）

用途：查看特定病患的就診記錄和用藥。

```sql
SELECT
    m.KCSTMR, m.MNAME,
    l.DATE AS 就診日, l.LABNO AS 主診斷,
    o.DNO AS 藥碼, o.DNAME AS 藥名, o.DQTY AS 數量, o.DDAY AS 天數
FROM CO01M m
JOIN CO03L l ON m.KCSTMR = l.KCSTMR
JOIN CO02M o ON l.KCSTMR = o.KCSTMR AND l.DATE = o.IDATE AND l.TIME = o.ITIME
WHERE m.KCSTMR = '0000024'
ORDER BY l.DATE DESC, o.DNO;
```

### 就診 + SOAP + 處方（完整看診紀錄）

用途：重建一次看診的完整內容。

```sql
SELECT
    l.DATE, l.TIME, l.LABNO AS 診斷,
    GROUP_CONCAT(DISTINCT h.STEXT ORDER BY h.SATB) AS SOAP,
    GROUP_CONCAT(DISTINCT o.DNAME || '×' || o.DQTY) AS 處方
FROM CO03L l
LEFT JOIN CO02H h ON l.KCSTMR = h.KCSTMR AND l.DATE = h.SDATE AND l.TIME = h.STIME
LEFT JOIN CO02M o ON l.KCSTMR = o.KCSTMR AND l.DATE = o.IDATE AND l.TIME = o.ITIME
WHERE l.KCSTMR = '0000024' AND l.DATE = '1140220'
GROUP BY l.DATE, l.TIME, l.LABNO;
```

### 就診 + 檢驗結果（追蹤慢性病指標）

用途：查看病患的歷次檢驗結果趨勢。

```sql
SELECT
    l.DATE AS 就診日,
    h.CHECKNO AS 檢驗代碼,
    h.CHECKNAME AS 檢驗名稱,
    h.RESULT AS 結果,
    h.UNIT AS 單位,
    h.REFRANGE AS 參考值
FROM CO03L l
JOIN CO18H h ON l.KCSTMR = h.KCSTMR AND l.DATE = h.IDATE
WHERE l.KCSTMR = '0000024'
  AND h.CHECKNO IN ('09002', '09015')  -- HbA1c, eGFR
ORDER BY l.DATE DESC;
```

### JOIN 條件速查

| 來源表 | 目標表 | JOIN 欄位 |
|--------|--------|-----------|
| CO01M → CO03L | 病患→就診 | `KCSTMR` |
| CO03L → CO02M | 就診→處方 | `KCSTMR + DATE/IDATE + TIME/ITIME` |
| CO03L → CO02H | 就診→SOAP | `KCSTMR + DATE/SDATE + TIME/STIME` |
| CO03L → CO18H | 就診→檢驗 | `KCSTMR + DATE/IDATE` |
| CO03L → CO03M | 就診→診斷詳細 | `KCSTMR + DATE/IDATE + TIME/ITIME` |

> **陷阱**：CO03L 的欄位叫 `DATE` 和 `TIME`，但 CO02M 叫 `IDATE` 和 `ITIME`，
> CO02H 叫 `SDATE` 和 `STIME`。JOIN 時要注意這個命名差異。
