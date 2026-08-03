#!/usr/bin/env python3
"""Make project listing media portable and opt-in to load."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / lang / "projects.html" for lang in ("en", "tw", "jp")]
OLD_PREFIX = "https://bddgtw-tw.github.io/sunnywardwebsite/_assets/projects/"
NEW_PREFIX = "../_assets/projects/"

VIDEO = re.compile(
    r'<video src="(?P<src>\.\./_assets/projects/[^"]+\.mp4)"'
    r' autoplay loop muted playsinline preload="metadata"></video>'
)


def optimize(path: Path) -> None:
    text = path.read_text(encoding="utf-8").replace(OLD_PREFIX, NEW_PREFIX)

    def replace_video(match: re.Match[str]) -> str:
        tail = text[match.end():]
        image = re.search(r'<img src="(\.\./_assets/projects/[^"]+_q1\.jpg)"', tail)
        if not image:
            raise RuntimeError(f"Missing poster after {match.group('src')} in {path}")
        return (
            f'<video src="{match.group("src")}" controls playsinline '
            f'preload="none" poster="{image.group(1)}"></video>'
        )

    text, count = VIDEO.subn(replace_video, text)
    optimized = re.findall(
        r'<video src="\.\./_assets/projects/[^"]+\.mp4" controls playsinline '
        r'preload="none" poster="\.\./_assets/projects/[^"]+_q1\.jpg"></video>',
        text,
    )
    if len(optimized) != 10:
        raise RuntimeError(
            f"Expected 10 optimized listing videos in {path}, found {len(optimized)}"
        )
    path.write_text(text, encoding="utf-8")
    print(f"optimized {path.relative_to(ROOT)}: {count} changed, 10 governed")


if __name__ == "__main__":
    for page in PAGES:
        optimize(page)
