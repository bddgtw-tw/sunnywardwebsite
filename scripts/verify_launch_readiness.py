from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
broken: list[tuple[str, str]] = []
for page in ROOT.glob("**/*.html"):
    if ".git" in page.parts:
        continue
    soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
    local_ids = {node.get("id") for node in soup.select("[id]") if node.get("id")}
    for node in soup.select("[href],[src]"):
        value = node.get("href") if node.has_attr("href") else node.get("src")
        value = (value or "").strip()
        if not value or value.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "/")):
            continue
        parts = urlsplit(value)
        if not parts.path:
            if parts.fragment and parts.fragment not in local_ids:
                broken.append((str(page.relative_to(ROOT)), value))
            continue
        target = (page.parent / unquote(parts.path)).resolve()
        if parts.path.endswith("/"):
            target /= "index.html"
        if not target.exists():
            broken.append((str(page.relative_to(ROOT)), value))
assert not broken, f"Broken internal links: {broken[:20]}"

root_page = (ROOT / "index.html").read_text(encoding="utf-8")
assert 'content="noindex,follow"' in root_page and "繁體中文" in root_page and "日本語" in root_page
for preview in ("office.html", "outdoor.html"):
    assert 'content="noindex,nofollow"' in (ROOT / preview).read_text(encoding="utf-8")
error_page = (ROOT / "404.html").read_text(encoding="utf-8")
error_soup = BeautifulSoup(error_page, "html.parser")
assert 'content="noindex,follow"' in error_page and "/sunnywardwebsite" in error_page and len(error_soup.select("[data-site-path]")) == 3

tree = ET.parse(ROOT / "sitemap.xml")
ns = {"s":"http://www.sitemaps.org/schemas/sitemap/0.9", "x":"http://www.w3.org/1999/xhtml"}
urls = tree.findall("s:url", ns)
assert len(urls) == 33, f"Unexpected sitemap URL count: {len(urls)}"
for item in urls:
    links = item.findall("x:link", ns)
    assert len(links) == 4 and {link.attrib["hreflang"] for link in links} == {"en", "zh-TW", "ja", "x-default"}
print(f"Verified {len(urls)} sitemap URLs, language parity, root entry, custom 404 and all internal links.")
