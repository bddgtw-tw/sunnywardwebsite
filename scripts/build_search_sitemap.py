from __future__ import annotations

import html
from pathlib import Path

from bs4 import BeautifulSoup
from site_config import LANGUAGES, public_url


ROOT = Path(__file__).resolve().parents[1]
LANGS = LANGUAGES


def indexable_paths(lang: str) -> set[str]:
    paths: set[str] = set()
    for page in (ROOT / lang).glob("**/*.html"):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        robots = soup.select_one('meta[name="robots"]')
        if robots and "noindex" in robots.get("content", "").lower():
            continue
        relative = page.relative_to(ROOT / lang).as_posix()
        paths.add("" if relative == "index.html" else relative)
    return paths


def build_sitemap() -> None:
    paths_by_lang = {lang:indexable_paths(lang) for lang in LANGS}
    reference = paths_by_lang["en"]
    for lang, paths in paths_by_lang.items():
        if paths != reference:
            raise RuntimeError(f"Language URL parity mismatch for {lang}: missing={sorted(reference-paths)}, extra={sorted(paths-reference)}")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for lang in LANGS:
        for path in sorted(reference):
            suffix = f"/{path}" if path else "/"
            loc = public_url(f"{lang}{suffix}")
            lines.append("  <url>")
            lines.append(f"    <loc>{html.escape(loc)}</loc>")
            for folder, hreflang in LANGS.items():
                href = public_url(f"{folder}{suffix}")
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="{html.escape(href)}" />')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{public_url(f"en{suffix}")}" />')
            lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Built sitemap with {len(reference) * len(LANGS)} URLs and four language alternates per URL.")


if __name__ == "__main__":
    build_sitemap()
