# 資料品質審計查詢

資料品質是分析的基礎。以下查詢可定期執行，及早發現資料異常。建議每月執行一次並記錄結果。

## 重複記錄偵測

同一病患同日同時間重複掛號，可能為系統重複寫入或操作錯誤：

```sql
-- 重複掛號記錄
SELECT KCSTMR, TBKDT, TBKTIME, COUNT(*) as cnt
FROM CO05O GROUP BY KCSTMR, TBKDT, TBKTIME HAVING cnt > 1;

-- 重複就診記錄（CO03L）
SELECT KCSTMR, DATE, TIME, COUNT(*) as cnt
FROM CO03L GROUP BY KCSTMR, DATE, TIME HAVING cnt > 1;
```

## 缺漏資料分析

無身分證字號或格式異常的病患，影響健保申報與家醫計畫關聯：

```sql
-- 無身分證字號的病患
SELECT KCSTMR, MNAME, MBIRTHDT FROM CO01M
WHERE MPERSONID IS NULL OR MPERSONID = '' OR LENGTH(MPERSONID) != 10;

-- 身分證格式異常（應為1英+9數）
SELECT KCSTMR, MNAME, MPERSONID FROM CO01M
WHERE MPERSONID NOT GLOB '[A-Z][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'
  AND MPERSONID IS NOT NULL AND MPERSONID != '';
```

## 日期合理性檢查

出現未來日期的就診記錄，通常為資料輸入錯誤：

```sql
-- SQLite：未來日期的就診記錄
SELECT KCSTMR, DATE, TIME, LABNO FROM CO03L
WHERE DATE > strftime('%Y%m%d', 'now', '-1911 years');

-- PostgreSQL：未來日期的就診記錄
SELECT kcstmr, date, time, labno FROM co03l
WHERE date > TO_CHAR(NOW() - INTERVAL '1911 years', 'YYYMMDD');
```

> **注意**：民國年日期格式為 7 位字串 `YYYMMDD`，比較前需轉換。

## 孤兒記錄偵測

有處方但無對應就診記錄，可能為資料同步問題：

```sql
-- 有處方但無對應就診記錄
SELECT m.KCSTMR, m.IDATE, m.ITIME, m.DNO
FROM CO02M m LEFT JOIN CO03L l
  ON m.KCSTMR = l.KCSTMR AND m.IDATE = l.DATE AND m.ITIME = l.TIME
WHERE l.KCSTMR IS NULL;

-- 有病歷但無對應就診記錄
SELECT h.KCSTMR, h.SDATE, h.STIME
FROM CO02H h LEFT JOIN CO03L l
  ON h.KCSTMR = l.KCSTMR AND h.SDATE = l.DATE AND h.STIME = l.TIME
WHERE l.KCSTMR IS NULL;
```

## 資料一致性檢查

CO03L 與 CO03M 的診斷碼理論上應一致，不一致可能為修改後未同步：

```sql
-- CO03L 與 CO03M 的診斷碼不一致
SELECT l.KCSTMR, l.DATE, l.LABNO as L_ICD, m.LABNO as M_ICD
FROM CO03L l JOIN CO03M m
  ON l.KCSTMR = m.KCSTMR AND l.DATE = m.IDATE AND l.TIME = m.ITIME
WHERE l.LABNO != m.LABNO;
```

## 資料完整性統計

```sql
-- 每月資料完整性摘要
SELECT
    SUBSTR(DATE, 1, 5) as 年月,
    COUNT(*) as 就診總筆數,
    SUM(CASE WHEN LABNO IS NULL OR LABNO = '' THEN 1 ELSE 0 END) as 無主診斷,
    SUM(CASE WHEN LTIME = '000000' THEN 1 ELSE 0 END) as 未完診
FROM CO03L
GROUP BY SUBSTR(DATE, 1, 5)
ORDER BY 年月 DESC;
```

## 執行建議

| 頻率 | 查詢類型 | 說明 |
|------|---------|------|
| 每日 | 孤兒記錄、未完診 | 當日結束後確認 |
| 每週 | 重複記錄 | 週五收診後 |
| 每月 | 身分證格式、日期合理性、資料統計 | 月初執行 |

## 查詢除錯：為什麼回傳 0 筆？

查詢回傳空結果是最常見的問題。按以下順序檢查：

### 1. 日期格式錯誤（最常見）

展望系統不同資料表使用不同日期格式：

| 資料表 | 欄位 | 格式 | 範例（2026-02-20）|
|--------|------|------|-------------------|
| CO03L | DATE | ROC 7碼 YYYMMDD | `1150220` |
| CO02M | IDATE | ROC 7碼 YYYMMDD | `1150220` |
| CO02H | SDATE | ROC 7碼 YYYMMDD | `1150220` |
| CO05O | TBKDT | ROC 7碼 YYYMMDD | `1150220` |
| CO10A | AREMARK（效期）| 西元 8碼 YYYYMMDD | `20260220` |
| CO18H | HDATE | ROC 7碼 YYYMMDD | `1150220` |

**快速驗證**：先用 `SELECT DISTINCT DATE FROM CO03L ORDER BY DATE DESC LIMIT 5` 確認實際資料的日期格式再寫查詢。

### 2. 字串 vs 數值比較

CO18H.HVAL 儲存為文字。數值比較必須 CAST：

```sql
-- 錯誤：'7.2' > '10' 在字串比較中成立（'7' > '1'）
WHERE HVAL > '7.0'

-- 正確
WHERE CAST(HVAL AS REAL) > 7.0
```

### 3. JOIN 條件不匹配

跨表 JOIN 時，日期欄位名稱不一致：

```sql
-- 錯誤：CO03L 用 DATE，CO02M 用 IDATE
JOIN CO02M m ON l.KCSTMR = m.KCSTMR AND l.DATE = m.DATE

-- 正確
JOIN CO02M m ON l.KCSTMR = m.KCSTMR AND l.DATE = m.IDATE
```

### 4. 分段記錄未合併

CO02H（SOAP）和 CO02F（檢驗報告）存在分段記錄（SATB=0,1,2...）：

```sql
-- 錯誤：只拿到第一段
SELECT STEXT FROM CO02H WHERE KCSTMR = ? AND SDATE = ?

-- 正確：合併所有分段
SELECT GROUP_CONCAT(STEXT, '') as 完整內容
FROM (SELECT STEXT FROM CO02H
      WHERE KCSTMR = ? AND SDATE = ? AND SCLASS = 'S'
      ORDER BY CAST(SATB AS INTEGER))
```

### 5. 快速除錯步驟

```
查詢回傳 0 筆
├── 1. 確認日期格式（ROC 7碼 vs 西元 8碼）
├── 2. 去掉 WHERE 條件逐步加回，找出哪個條件篩掉了所有資料
├── 3. 用 SELECT COUNT(*) FROM 表名 確認表本身有資料
├── 4. 檢查 JOIN 條件的欄位名稱是否對應正確
└── 5. 用 SELECT DISTINCT 欄位名 FROM 表名 LIMIT 10 確認欄位實際存值格式
```
