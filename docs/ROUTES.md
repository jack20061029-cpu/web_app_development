# 路由設計文件 (docs/ROUTES.md)

## 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 食譜列表 | GET | /recipes | templates/recipes/index.html | 顯示所有食譜 |
| 新增食譜表單 | GET | /recipes/new | templates/recipes/new.html | 顯示食譜建立表單 |
| 建立食譜 | POST | /recipes | - | 接收表單資料，新增至 DB，重導向至列表 |
| 食譜詳細 | GET | /recipes/<id> | templates/recipes/detail.html | 顯示單筆食譜 |
| 編輯食譜表單 | GET | /recipes/<id>/edit | templates/recipes/edit.html | 顯示食譜編輯表單 |
| 更新食譜 | POST | /recipes/<id>/update | - | 接收表單資料，更新 DB，重導向至詳細頁 |
| 刪除食譜 | POST | /recipes/<id>/delete | - | 從 DB 刪除食譜，重導向至列表 |

## 每個路由的詳細說明

1. **食譜列表** (`GET /recipes`)
   - 輸入：無
   - 處理邏輯：呼叫 `Recipe.get_all()` 取得所有食譜
   - 輸出：渲染 `templates/recipes/index.html`，傳入食譜清單
   - 錯誤處理：若 DB 讀取失敗回傳 500

2. **新增食譜表單** (`GET /recipes/new`)
   - 輸入：無
   - 處理邏輯：僅渲染表單頁面
   - 輸出：`templates/recipes/new.html`
   - 錯誤處理：無

3. **建立食譜** (`POST /recipes`)
   - 輸入：表單欄位 `title`, `description`, `cooking_time_minutes`, `ingredients`, `steps`
   - 處理邏輯：建立 `Recipe` 物件並呼叫 `save()`，成功後取得 `id`
   - 輸出：Redirect to `/recipes`
   - 錯誤處理：驗證失敗返回表單並顯示錯誤訊息

4. **食譜詳細** (`GET /recipes/<id>`)
   - 輸入：URL 參數 `id`
   - 處理邏輯：`Recipe.get_by_id(id)`，若無則 404
   - 輸出：`templates/recipes/detail.html`
   - 錯誤處理：ID 不存在回 404

5. **編輯食譜表單** (`GET /recipes/<id>/edit`)
   - 輸入：`id`
   - 處理邏輯：取得現有食譜資料，傳入表單
   - 輸出：`templates/recipes/edit.html`
   - 錯誤處理：ID 不存在回 404

6. **更新食譜** (`POST /recipes/<id>/update`)
   - 輸入：`id` 以及表單欄位
   - 處理邏輯：取得模型、更新屬性、呼叫 `save()`
   - 輸出：Redirect to `/recipes/<id>`
   - 錯誤處理：驗證失敗返回編輯表單

7. **刪除食譜** (`POST /recipes/<id>/delete`)
   - 輸入：`id`
   - 處理邏輯：`Recipe.get_by_id(id)` → `delete()`
   - 輸出：Redirect to `/recipes`
   - 錯誤處理：ID 不存在回 404

## Jinja2 模板清單

- `templates/base.html` – 所有食譜相關模板的基礎版型，包含導覽列與共用樣式。
- `templates/recipes/index.html` – 食譜列表頁，繼承 `base.html`，顯示卡片或表格。
- `templates/recipes/detail.html` – 顯示單筆食譜的詳細資訊。
- `templates/recipes/new.html` – 新增食譜表單。
- `templates/recipes/edit.html` – 編輯食譜表單，使用相同的欄位結構。

---

*此文件由 /api-design skill 產出，供團隊分工與後續實作參考。*
