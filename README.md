# ☀️ Sunnyward - 官方網站專案

本專案為 **Sunnyward** 官方網站之前端程式碼與產品資料庫。

---

## 📌 專案架構與分支管理

本專案採用 **GitHub 雙分支管理機制**：

- **`draft` (預設開發分支)**：所有日常 HTML/CSS 修改、JSON 產品資料更新或測試均在此分支進行。
- **`main` (正式發布分支)**：僅放已確認無誤、準備 publish 上線的穩定程式碼。

---

## 📂 核心資料目錄

- `tw/products.json` : 繁體中文產品資料庫
- `en/products.json` : 英文產品資料庫
- `Product_Images/` : 產品圖片庫

---

## 🚀 快速操作指南

### 1. 切換至開發分支並提交變更
```bash
git checkout draft
git add .
git commit -m "更新產品資料或頁面"
git push origin draft
```

### 2. 合併發布至正式版 (Publish)
```bash
git checkout main
git merge draft
git push origin main
git checkout draft
```
