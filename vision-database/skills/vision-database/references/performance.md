# 效能優化指南

## 建議索引

針對常見查詢模式，建立以下索引以加速查詢效能：

```sql
-- CO03L：依病歷號+日期查詢就診歷史（最常用）
CREATE INDEX idx_co03l_kcstmr_date ON CO03L (KCSTMR, DATE DESC);

-- CO03L：依診斷碼篩選病患
CREATE INDEX idx_co03l_labno ON CO03L (LABNO);

-- CO18H：依病歷號+檢驗項目查詢趨勢
CREATE INDEX idx_co18h_kcstmr_hitem_hdate ON CO18H (KCSTMR, HITEM, HDATE DESC);

-- CO02M：依病歷號+日期查詢處方
CREATE INDEX idx_co02m_kcstmr_idate ON CO02M (KCSTMR, IDATE DESC);

-- CO02H：依病歷號+日期查詢 SOAP Notes
CREATE INDEX idx_co02h_kcstmr_sdate ON CO02H (KCSTMR, SDATE DESC, STIME DESC, SATB ASC);

-- CO05O：今日門診看板
CREATE INDEX idx_co05o_tbkdt_tsts ON CO05O (TBKDT, TSTS);

-- CO09S：庫存異動查詢
CREATE INDEX idx_co09s_kdrug_ddate ON CO09S (KDRUG, DDATE DESC);
```

## Materialized View（PostgreSQL）

針對儀表板反覆查詢的統計資料，使用 Materialized View 預先計算：

```sql
-- 月度門診統計（每日排程更新）
CREATE MATERIALIZED VIEW mv_monthly_stats AS
SELECT
    SUBSTR("date", 1, 5) as year_month,
    COUNT(DISTINCT "kcstmr") as unique_patients,
    COUNT(*) as total_visits,
    SUM(CASE WHEN "labno" LIKE 'E11%' THEN 1 ELSE 0 END) as diabetes_visits,
    SUM(CASE WHEN "labno" LIKE 'I10%' OR "labno" LIKE 'I11%' THEN 1 ELSE 0 END) as hypertension_visits
FROM co03l
GROUP BY SUBSTR("date", 1, 5);

-- 定期刷新（建議排程每日凌晨執行）
REFRESH MATERIALIZED VIEW mv_monthly_stats;
```

## 分頁查詢模式

大量資料查詢時，避免單純的 `LIMIT/OFFSET`，改用 Keyset Pagination：

```sql
-- 不建議：OFFSET 越大越慢
SELECT * FROM CO03L ORDER BY DATE DESC, TIME DESC LIMIT 50 OFFSET 10000;

-- 建議：Keyset Pagination（以上一頁最後一筆的 DATE+TIME 作為游標）
SELECT * FROM CO03L
WHERE (DATE, TIME) < (?, ?)    -- 上一頁最後一筆的 DATE 和 TIME
ORDER BY DATE DESC, TIME DESC
LIMIT 50;
```

Keyset Pagination 的優點：
- 無論在第幾頁，查詢時間穩定一致
- 避免 OFFSET 造成的重複或遺漏（資料異動時）
- 搭配索引效能更佳

## EXPLAIN 用法

優化查詢前，先用 `EXPLAIN` 確認查詢計劃：

```sql
-- SQLite：查看查詢計劃
EXPLAIN QUERY PLAN SELECT * FROM CO03L WHERE KCSTMR = '0000024' AND DATE > '1140101';

-- PostgreSQL：查看詳細執行計劃（含實際時間）
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM co03l WHERE "kcstmr" = '0000024' AND "date" > '1140101';
```

**判讀重點**：
- `SCAN TABLE` / `Seq Scan`：全表掃描，資料量大時效能差，考慮加索引
- `SEARCH TABLE USING INDEX` / `Index Scan`：使用索引，效能佳
- `USING COVERING INDEX`：索引已包含所需欄位，無需回表查詢，效能最佳
- PostgreSQL 的 `actual time` 與 `rows` 可確認預估與實際是否偏差過大

## 慢查詢識別（PostgreSQL）

需先啟用 `pg_stat_statements` 擴充套件：

```sql
-- 慢查詢識別（按平均執行時間排序）
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;

-- 表格大小監控
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) as total_size,
       n_live_tup as row_count
FROM pg_stat_user_tables ORDER BY pg_total_relation_size(relid) DESC;

-- 索引使用率分析
SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes ORDER BY idx_scan ASC;

-- 未使用的索引（建議刪除候選）
SELECT indexrelname, idx_scan FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelname NOT LIKE 'pg_%';
```

> **注意**：刪除索引前建議觀察至少一個完整業務週期（通常 1 個月），確認確實未被使用。
