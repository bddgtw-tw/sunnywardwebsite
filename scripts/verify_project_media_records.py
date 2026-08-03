from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "project_media_records.json"
LANGS = ("en", "tw", "jp")
RISKY_PATTERNS = (
    "uc-testimonial",
    "increase in table turnover",
    "guest satisfaction",
    "ten times the lifespan",
    "zero stain absorption",
    "十倍",
    "10倍",
    "顧客滿意度",
    "回転率の顕著な向上",
)


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    errors: list[str] = []
    expected_ids = {record["id"] for record in source["records"]}

    for record in source["records"]:
        media = ROOT / "_assets" / "projects" / record["video"]
        if not media.exists() or media.stat().st_size == 0:
            errors.append(f"Missing source media: {record['video']}")

    for lang in LANGS:
        path = ROOT / lang / "projects.html"
        content = path.read_text(encoding="utf-8")
        section_ids = set(re.findall(r'<section\b(?=[^>]*class="[^"]*ultimate-case-section[^"]*")(?=[^>]*id="([^"]+)")[^>]*>', content))
        if section_ids != expected_ids:
            errors.append(f"Project section set mismatch in {lang}/projects.html")
        if content.count('class="uc-narrative') != len(expected_ids):
            errors.append(f"Narrative count mismatch in {lang}/projects.html")
        for pattern in RISKY_PATTERNS:
            if pattern.casefold() in content.casefold():
                errors.append(f"Unverified claim pattern {pattern!r} in {lang}/projects.html")
        for record in source["records"]:
            if record["titles"][lang] not in content:
                errors.append(f"Missing verified title for {lang}/{record['id']}")
            if f"<code>{record['video']}</code>" in content:
                errors.append(f"Internal source filename visibly exposed for {lang}/{record['id']}")

    if errors:
        print("Project media record checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Verified {len(source['records']) * len(LANGS)} localized project records and {len(source['records'])} source media files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
