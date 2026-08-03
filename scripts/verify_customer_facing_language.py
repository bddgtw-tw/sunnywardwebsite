#!/usr/bin/env python3
"""Fail release when internal evidence-governance language becomes customer-facing."""

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
BANNED = {
    "en": ("verified", "verification", "media-backed", "evidence-led", "publication standard", "record status", "source review", "source media", "pilot catalogue", "structured source", "cross-checked"),
    "tw": ("已核對", "核實", "來源審核", "來源文件", "發布標準", "紀錄狀態", "媒體存檔", "媒體紀錄", "佐證"),
    "jp": ("確認済み", "資料確認", "公開基準", "記録状況", "メディア保存", "メディア記録"),
}


checked = 0
for lang, terms in BANNED.items():
    for path in (ROOT / lang).rglob("*.html"):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for node in soup.select('script:not([type="application/ld+json"]), style'):
            node.decompose()
        exposed = soup.get_text(" ", strip=True)
        exposed += " " + " ".join(tag.get("content", "") for tag in soup.select("meta[content]"))
        folded = exposed.casefold()
        for term in terms:
            assert term.casefold() not in folded, f"Internal governance language exposed: {path}: {term}"
        checked += 1

llms = (ROOT / "llms.txt").read_text(encoding="utf-8").casefold()
for term in BANNED["en"]:
    assert term.casefold() not in llms, f"Internal governance language exposed in llms.txt: {term}"
root_entry = (ROOT / "index.html").read_text(encoding="utf-8").casefold()
assert "verified" not in root_entry and "verification" not in root_entry
print(f"Verified customer-facing language boundary on {checked} localized pages plus root and llms.txt.")
