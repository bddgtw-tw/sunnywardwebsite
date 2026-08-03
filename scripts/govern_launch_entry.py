from pathlib import Path
from site_config import PRODUCTION_ORIGIN


ROOT = Path(__file__).resolve().parents[1]

ROOT_INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sunnyward | Select Language</title>
  <meta name="description" content="Choose English, Traditional Chinese or Japanese to explore Sunnyward commercial furniture and verified project records.">
  <meta name="robots" content="noindex,follow">
  <link rel="canonical" href="__PRODUCTION_ORIGIN__/en/">
  <link rel="alternate" hreflang="en" href="__PRODUCTION_ORIGIN__/en/">
  <link rel="alternate" hreflang="zh-TW" href="__PRODUCTION_ORIGIN__/tw/">
  <link rel="alternate" hreflang="ja" href="__PRODUCTION_ORIGIN__/jp/">
  <link rel="alternate" hreflang="x-default" href="__PRODUCTION_ORIGIN__/en/">
  <script>
    (function () {
      var savedLang = localStorage.getItem('sw_lang');
      if (savedLang === 'jp' || savedLang === 'en' || savedLang === 'tw') {
        window.location.replace('./' + savedLang + '/index.html');
        return;
      }
      var browserLang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();
      window.location.replace(browserLang.indexOf('zh') > -1 ? './tw/index.html' : browserLang.indexOf('ja') > -1 ? './jp/index.html' : './en/index.html');
    })();
  </script>
</head>
<body style="background:#f9f8f6;display:flex;align-items:center;justify-content:center;height:100vh;font-family:Arial,sans-serif;margin:0;color:#2e2722;">
  <main style="text-align:center;padding:2rem;">
    <p style="font-size:.9rem;letter-spacing:.1em;text-transform:uppercase;color:#b88e6b;">Choose your language</p>
    <p><a href="./en/">English</a> · <a href="./tw/">繁體中文</a> · <a href="./jp/">日本語</a></p>
  </main>
</body>
</html>
'''

ERROR_PAGE = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Page Not Found | Sunnyward</title><meta name="robots" content="noindex,follow">
<style>:root{font-family:Arial,sans-serif}*{box-sizing:border-box}body{margin:0;min-height:100vh;display:grid;place-items:center;padding:2rem;background:#f8f7f4;color:#211c18}main{width:min(720px,100%);padding:clamp(2rem,6vw,4.5rem);background:#fff;border-top:4px solid #b46f44}.code{color:#b46f44;font-size:.78rem;letter-spacing:.18em;text-transform:uppercase}h1{margin:.7rem 0 1rem;font:400 clamp(2.5rem,8vw,5.5rem)/1.05 Georgia,serif}p{color:#645b55;line-height:1.75}nav{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:2rem}a{display:inline-block;padding:.8rem 1rem;border:1px solid #b46f44;color:#8a4f2f;text-decoration:none}a:hover,a:focus{background:#b46f44;color:#fff}</style></head>
<body><main><span class="code">404 · Page not found</span><h1>Find your way back.</h1><p>The requested page may have moved. Choose a language to continue.<br>找不到指定頁面，請選擇語言返回網站。<br>ページが見つかりません。言語を選択してサイトに戻ってください。</p><nav aria-label="Language homepages"><a data-site-path="/en/" href="/en/">English</a><a data-site-path="/tw/" href="/tw/">繁體中文</a><a data-site-path="/jp/" href="/jp/">日本語</a></nav></main>
<script>(function(){var prefix=location.hostname.endsWith('github.io')?'/sunnywardwebsite':'';document.querySelectorAll('[data-site-path]').forEach(function(link){link.href=prefix+link.getAttribute('data-site-path')})})();</script></body></html>
'''

(ROOT / "index.html").write_text(
    ROOT_INDEX.replace("__PRODUCTION_ORIGIN__", PRODUCTION_ORIGIN),
    encoding="utf-8",
    newline="\n",
)
(ROOT / "404.html").write_text(ERROR_PAGE, encoding="utf-8", newline="\n")
for name in ("office.html", "outdoor.html"):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    if 'name="robots"' not in text:
        text = text.replace("<head>", '<head>\n    <meta name="robots" content="noindex,nofollow">', 1)
    path.write_text(text, encoding="utf-8", newline="\n")
print("Built the root language entry, custom 404 and noindex protection for legacy previews.")
