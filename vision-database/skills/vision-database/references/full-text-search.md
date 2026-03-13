# SOAP Notes 全文搜尋

展望 HIS 系統的 SOAP Notes 儲存在 **CO02H** 資料表（`STEXT` 欄位，每段最多 250 字元）。
以下提供 SQLite FTS5 和 PostgreSQL tsvector 兩種全文搜尋方案。

> ⚠️ 展望系統的 SOAP Notes 欄位是 `CO02H.STEXT`，不是 `CO03L`。
> `CO03L` 是就診記錄（含 ICD 診斷碼），無法做 SOAP 內文搜尋。

## SQLite FTS5

```sql
-- 建立 FTS 虛擬表（映射到 CO02H）
CREATE VIRTUAL TABLE soap_fts USING fts5(
  kcstmr,       -- 病患代碼
  sdate,         -- 看診日期
  stime,         -- 看診時間
  satb,          -- 段落序號
  stext,         -- SOAP 內容（主訴/評估/計畫等）
  content='CO02H',
  content_rowid='rowid'
);

-- 從現有資料填入
INSERT INTO soap_fts(rowid, kcstmr, sdate, stime, satb, stext)
SELECT rowid, KCSTMR, SDATE, STIME, SATB, STEXT FROM CO02H;

-- 全文搜尋：搜尋含「頭痛」的 SOAP 記錄
SELECT DISTINCT kcstmr, sdate
FROM soap_fts
WHERE soap_fts MATCH '頭痛'
ORDER BY sdate DESC;

-- 搜尋特定病患的 SOAP 含「血壓」的記錄
SELECT sdate, stime, stext
FROM soap_fts
WHERE soap_fts MATCH 'kcstmr:0000024 AND 血壓';

-- 合併同一次看診的多段記錄（FTS 結果 + GROUP_CONCAT）
SELECT f.kcstmr, f.sdate, f.stime,
       GROUP_CONCAT(h.STEXT, '') AS full_soap
FROM soap_fts f
JOIN CO02H h ON f.kcstmr = h.KCSTMR AND f.sdate = h.SDATE AND f.stime = h.STIME
WHERE soap_fts MATCH '糖尿病'
GROUP BY f.kcstmr, f.sdate, f.stime
ORDER BY f.sdate DESC;

-- 維護：新增資料後更新 FTS 索引
INSERT INTO soap_fts(rowid, kcstmr, sdate, stime, satb, stext)
SELECT rowid, KCSTMR, SDATE, STIME, SATB, STEXT
FROM CO02H
WHERE rowid > (SELECT MAX(rowid) FROM soap_fts);
```

## PostgreSQL tsvector

```sql
-- 新增 tsvector 欄位（使用 zhparser 或 pg_jieba 做中文分詞）
ALTER TABLE co02h ADD COLUMN soap_tsv tsvector;

-- 更新 tsvector
UPDATE co02h SET soap_tsv = to_tsvector('zhparser', COALESCE("stext", ''));

-- 建立 GIN 索引
CREATE INDEX idx_co02h_soap_tsv ON co02h USING GIN(soap_tsv);

-- 全文搜尋：頭痛 AND 發燒
SELECT DISTINCT "kcstmr", "sdate", "stime"
FROM co02h
WHERE soap_tsv @@ to_tsquery('zhparser', '頭痛 & 發燒')
ORDER BY "sdate" DESC;

-- 結合合併分段：搜尋 + 回傳完整 SOAP 內容
SELECT "kcstmr", "sdate", "stime",
       STRING_AGG("stext", '' ORDER BY "satb" ASC) AS full_soap
FROM co02h
WHERE soap_tsv @@ to_tsquery('zhparser', '血糖')
GROUP BY "kcstmr", "sdate", "stime"
ORDER BY "sdate" DESC;

-- 觸發器：自動維護 tsvector
CREATE OR REPLACE FUNCTION update_soap_tsv() RETURNS trigger AS $$
BEGIN
  NEW.soap_tsv := to_tsvector('zhparser', COALESCE(NEW."stext", ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_soap_tsv BEFORE INSERT OR UPDATE ON co02h
FOR EACH ROW EXECUTE FUNCTION update_soap_tsv();
```

## 注意事項

1. **中文分詞**：PostgreSQL 需要 `zhparser` 或 `pg_jieba` 擴充套件。安裝後執行 `CREATE TEXT SEARCH CONFIGURATION zhparser...`
2. **SQLite FTS5**：內建支援，但無法做中文詞彙分析（每個字元當一個 token）。若要搜尋片語，使用 `LIKE '%關鍵字%'` 更可靠
3. **分段問題**：SOAP Notes 按 SATB 分段，一次看診可能有多筆 FTS 記錄。搜尋後需用 `GROUP BY (KCSTMR, SDATE, STIME)` 去重複
4. **索引維護**：每次寫入 CO02H 後需同步更新 FTS 索引，建議用觸發器自動維護
