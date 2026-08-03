#!/usr/bin/env python3
"""Keep one project film per listing item and remove screenshot galleries."""

from pathlib import Path
import re

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]


def govern(path: Path) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    sections = soup.select("section.ultimate-case-section")
    assert len(sections) == 10, f"Expected 10 projects in {path}"
    removed = 0
    for section in sections:
        videos = section.select("video")
        assert len(videos) == 1, f"Each project must have one video in {path}"
        for gallery in section.select(".photo-carousel-wrap"):
            gallery.decompose()
            removed += 1
    assert removed in (0, 10), f"Partial gallery state in {path}: {removed}"
    html = str(soup)
    html = re.sub(
        r"\n?function scrollCarousel\(btn, direction\) \{.*?\n\}\n",
        "\n",
        html,
        flags=re.DOTALL,
    )
    path.write_text(html, encoding="utf-8", newline="\n")
    print(f"governed {path.relative_to(ROOT)}: 10 project films, no screenshot galleries")


def main() -> None:
    for lang in ("en", "tw", "jp"):
        govern(ROOT / lang / "projects.html")


if __name__ == "__main__":
    main()
