# [API 名稱] API 參考文件

## 概述

<!-- 用 1-2 句話說明這個 API 能做什麼 -->

[API 名稱] 提供 [功能描述]，讓開發者可以 [達成什麼目標]。

---

## 認證方式

<!-- 說明 API 認證機制 -->

### 取得 API Key

1. 前往 [平台名稱] 的 **開發者設定** 頁面。
2. 點選 **建立 API Key**。
3. 複製產生的金鑰，妥善保存。

> ⚠️ **注意**：API Key 只會顯示一次，請立即複製保存。

### 使用方式

在每個請求的 Header 中加入：

```
Authorization: Bearer YOUR_API_KEY
```

---

## Base URL

| 環境 | URL |
|------|-----|
| 正式環境（Production） | `https://api.example.com/v1` |
| 測試環境（Staging） | `https://staging-api.example.com/v1` |
| 本地開發（Local） | `http://localhost:3000/v1` |

---

## 端點（Endpoints）

### `GET` /resources

取得資源列表。

#### 查詢參數（Query Parameters）

| 名稱 | 型別 | 必填 | 說明 | 預設值 |
|------|------|------|------|--------|
| `page` | integer | 否 | 頁碼 | `1` |
| `per_page` | integer | 否 | 每頁筆數（最大 100） | `20` |
| `sort` | string | 否 | 排序欄位 | `created_at` |
| `order` | string | 否 | 排序方向：`asc` 或 `desc` | `desc` |

#### 回應（Response）

**成功（200 OK）**

```json
{
  "data": [
    {
      "id": "res_abc123",
      "name": "範例資源",
      "status": "active",
      "created_at": "2024-01-15T08:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 42,
    "total_pages": 3
  }
}
```

#### 錯誤回應

| HTTP 狀態碼 | 錯誤代碼 | 說明 |
|-------------|---------|------|
| `401` | `unauthorized` | API Key 無效或未提供 |
| `403` | `forbidden` | 沒有存取權限 |
| `429` | `rate_limit_exceeded` | 超過速率限制 |

---

### `POST` /resources

建立新資源。

#### 請求主體（Request Body）

```json
{
  "name": "新資源名稱",
  "description": "資源描述",
  "config": {
    "option_a": true,
    "option_b": "value"
  }
}
```

#### 請求主體欄位

| 名稱 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `name` | string | 是 | 資源名稱（1-100 字元） |
| `description` | string | 否 | 資源描述 |
| `config` | object | 否 | 設定選項 |

#### 回應（Response）

**成功（201 Created）**

```json
{
  "data": {
    "id": "res_def456",
    "name": "新資源名稱",
    "status": "active",
    "created_at": "2024-01-16T10:00:00Z"
  }
}
```

#### 錯誤回應

| HTTP 狀態碼 | 錯誤代碼 | 說明 |
|-------------|---------|------|
| `400` | `validation_error` | 請求參數驗證失敗 |
| `401` | `unauthorized` | API Key 無效或未提供 |
| `409` | `conflict` | 資源名稱已存在 |
| `422` | `unprocessable_entity` | 請求格式正確但語意有誤 |

---

### `GET` /resources/{id}

取得單一資源詳情。

#### 路徑參數（Path Parameters）

| 名稱 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `id` | string | 是 | 資源 ID |

#### 回應（Response）

**成功（200 OK）**

```json
{
  "data": {
    "id": "res_abc123",
    "name": "範例資源",
    "description": "資源描述",
    "status": "active",
    "config": {},
    "created_at": "2024-01-15T08:30:00Z",
    "updated_at": "2024-01-15T08:30:00Z"
  }
}
```

---

### `PUT` /resources/{id}

更新指定資源。

#### 路徑參數（Path Parameters）

| 名稱 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `id` | string | 是 | 資源 ID |

#### 請求主體（Request Body）

```json
{
  "name": "更新後的名稱",
  "description": "更新後的描述"
}
```

#### 回應（Response）

**成功（200 OK）**

```json
{
  "data": {
    "id": "res_abc123",
    "name": "更新後的名稱",
    "status": "active",
    "updated_at": "2024-01-16T12:00:00Z"
  }
}
```

---

### `DELETE` /resources/{id}

刪除指定資源。

> ⚠️ **注意**：此操作不可逆，刪除後資料無法復原。

#### 路徑參數（Path Parameters）

| 名稱 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `id` | string | 是 | 資源 ID |

#### 回應（Response）

**成功（204 No Content）**

無回應主體。

---

## 速率限制（Rate Limiting）

| 方案 | 限制 | 視窗 |
|------|------|------|
| Free | 100 次 | 每分鐘 |
| Pro | 1,000 次 | 每分鐘 |
| Enterprise | 自訂 | 自訂 |

### 速率限制 Header

每個回應都會包含以下 Header：

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705401600
```

### 超過限制

收到 `429 Too Many Requests` 時，讀取 `Retry-After` Header 取得等待秒數。

---

## 錯誤格式

所有錯誤回應統一格式：

```json
{
  "error": {
    "code": "error_code",
    "message": "人類可讀的錯誤說明",
    "details": [
      {
        "field": "name",
        "message": "不可為空"
      }
    ]
  }
}
```

---

## 程式碼範例

### curl

```bash
# 取得資源列表
curl -X GET "https://api.example.com/v1/resources?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"

# 建立資源
curl -X POST "https://api.example.com/v1/resources" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "我的資源", "description": "描述"}'
```

### Python

```python
import requests

BASE_URL = "https://api.example.com/v1"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

# 取得資源列表
response = requests.get(f"{BASE_URL}/resources", headers=headers)
data = response.json()

# 建立資源
payload = {"name": "我的資源", "description": "描述"}
response = requests.post(f"{BASE_URL}/resources", json=payload, headers=headers)
new_resource = response.json()
```

### JavaScript

```javascript
const BASE_URL = 'https://api.example.com/v1';
const headers = {
  'Authorization': 'Bearer YOUR_API_KEY',
  'Content-Type': 'application/json'
};

// 取得資源列表
const listRes = await fetch(`${BASE_URL}/resources`, { headers });
const data = await listRes.json();

// 建立資源
const createRes = await fetch(`${BASE_URL}/resources`, {
  method: 'POST',
  headers,
  body: JSON.stringify({ name: '我的資源', description: '描述' })
});
const newResource = await createRes.json();
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

const baseURL = "https://api.example.com/v1"

func main() {
    client := &http.Client{}

    // 取得資源列表
    req, _ := http.NewRequest("GET", baseURL+"/resources", nil)
    req.Header.Set("Authorization", "Bearer YOUR_API_KEY")
    resp, _ := client.Do(req)
    defer resp.Body.Close()

    // 建立資源
    body, _ := json.Marshal(map[string]string{
        "name":        "我的資源",
        "description": "描述",
    })
    req, _ = http.NewRequest("POST", baseURL+"/resources", bytes.NewBuffer(body))
    req.Header.Set("Authorization", "Bearer YOUR_API_KEY")
    req.Header.Set("Content-Type", "application/json")
    resp, _ = client.Do(req)
    defer resp.Body.Close()

    fmt.Println("完成")
}
```

---

## 版本管理

目前 API 版本：`v1`

API 版本號包含在 URL 路徑中。當有重大變更時，我們會發佈新版本並保持舊版本至少 **12 個月**。

### 版本棄用通知

棄用版本時，回應 Header 會包含：

```
Deprecation: true
Sunset: Sat, 01 Jan 2026 00:00:00 GMT
Link: <https://api.example.com/v2>; rel="successor-version"
```

---

> 🧯 **還是有問題？** 請參閱 [API 狀態頁面](https://status.example.com) 或聯繫 [開發者支援](mailto:dev-support@example.com)。
