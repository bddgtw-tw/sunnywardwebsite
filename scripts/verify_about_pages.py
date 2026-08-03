#!/usr/bin/env python3
"""Verify the governed About pages retain the two approved source decks."""

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "en": ("Four business engines", "Workers’ Dormitory", "NORA’s Cafe", "Jacqueline Hsiao"),
    "tw": ("四大事業引擎", "員工宿舍", "NORA’s Cafe", "Jacqueline Hsiao"),
    "jp": ("四つの事業エンジン", "従業員宿舎", "NORA’s Cafe", "Jacqueline Hsiao"),
}


def main() -> int:
    for lang, required in EXPECTED.items():
        path = ROOT / lang / "about.html"
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        text = soup.get_text(" ", strip=True)
        assert len(soup.select("h1")) == 1, f"{lang}: expected exactly one H1"
        assert len(soup.select("main > section")) == 11, f"{lang}: unexpected About section count"
        assert len(soup.select(".about-journey__item")) == 5, f"{lang}: incomplete timeline"
        assert len(soup.select(".about-ecosystem__item")) == 4, f"{lang}: incomplete BFI ecosystem"
        assert len(soup.select(".about-case")) == 2, f"{lang}: incomplete selected cases"
        for phrase in required:
            assert phrase in text, f"{lang}: missing approved source phrase {phrase!r}"
    print("Verified three About pages against both approved business source decks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
