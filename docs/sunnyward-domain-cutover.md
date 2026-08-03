# Sunnyward 正式網域切換檢查表

網站公開網址的唯一設定來源是 `data/site_config.json`。正式網域切換前，不要只修改個別 HTML。

## 切換前

1. 保留 Google Workspace 的全部 MX、SPF、DKIM 與 DMARC 紀錄。
2. 在 GitHub Pages 專案設定加入 `sunnyward.com`，確認網域驗證狀態。
3. 依 GitHub 當下官方文件配置 apex A／AAAA 紀錄；`www` 使用指向 GitHub Pages 主機名稱的 CNAME。
4. 確認舊網站需要保留或轉址的網址清單。
5. 執行 `python scripts/verify_domain_governance.py`，確認網站檔案內的正式網址設定一致。切換前執行 `--live` 預期會失敗，這代表上線閘門確實阻擋尚未完成的正式網域。

## 切換後

1. 確認 `https://sunnyward.com/`、三個語言首頁、產品頁與案例頁皆為 HTTP 200。
2. 確認 `www.sunnyward.com` 以單次 301/308 轉向主要網域。
3. 確認 HTTPS 憑證有效，GitHub Pages 已啟用強制 HTTPS。
4. 確認 canonical、hreflang、Open Graph、schema、robots.txt、sitemap.xml 全部使用 `https://sunnyward.com`。
5. 將 sitemap 提交至 Google Search Console 與 Bing Webmaster Tools，觀察索引、轉址與 404。
6. 實測 Email、WhatsApp、產品與案例帶入詢價的完整流程。
7. 執行 `python scripts/verify_domain_governance.py --live`；只有 30 個 sitemap 頁面、HTTPS、CNAME 與 `www` 單次轉址全部通過，才視為正式切換完成。

## 回復條件

若 HTTPS、主要頁面、郵件 DNS 或大量舊網址轉址任何一項失敗，先回復網站 DNS；不要刪除郵件相關 DNS 紀錄。
