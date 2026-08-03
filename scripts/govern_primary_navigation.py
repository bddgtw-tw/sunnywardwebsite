#!/usr/bin/env python3
"""Keep the five primary destinations consistent across every locale landing page."""

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "about.html", "products.html", "projects.html", "contact.html")
LABELS = {
    "en": ("Home", "About", "Products", "Projects", "Contact"),
    "tw": ("首頁", "關於 Sunnyward", "產品", "案例", "聯絡我們"),
    "jp": ("ホーム", "Sunnywardについて", "製品", "導入事例", "お問い合わせ"),
}


def link(soup: BeautifulSoup, href: str, label: str, active: bool):
    tag = soup.new_tag("a", href=href)
    tag["class"] = ["nav-link"] + (["active"] if active else [])
    if active:
        tag["aria-current"] = "page"
    tag.string = label
    return tag


changed = 0
for locale, labels in LABELS.items():
    for filename in PAGES:
        path = ROOT / locale / filename
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for redundant in soup.select('script[src$="js/init.js"], script[src$="../js/init.js"]'):
            redundant.decompose()
        menu = soup.select_one("ul.nav-menu")
        drawer = soup.select_one("nav#mobile-drawer")
        assert menu is not None and drawer is not None, f"Primary navigation missing: {path}"

        menu.clear()
        for href, label in zip(PAGES, labels, strict=True):
            item = soup.new_tag("li")
            item.append(link(soup, href, label, href == filename))
            menu.append(item)

        for old in list(drawer.find_all("a", class_="nav-link", recursive=False)):
            old.decompose()
        marker = drawer.contents[0] if drawer.contents else None
        for href, label in reversed(tuple(zip(PAGES, labels, strict=True))):
            tag = link(soup, href, label, href == filename)
            if marker is None:
                drawer.append(tag)
            else:
                marker.insert_before(tag)

        path.write_text(str(soup), encoding="utf-8")
        changed += 1

print(f"Governed five-link primary navigation on {changed} locale landing pages.")
