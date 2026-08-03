#!/usr/bin/env python3
"""One-time organizer for the private, human-managed project input folders."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

from build_project_content_folders import LOCALES, ROOT, SLUGS, localized_record, source_path


INPUT_ROOT = ROOT / "project-input"


def main() -> None:
    assert INPUT_ROOT.resolve().parent == ROOT.resolve()
    INPUT_ROOT.mkdir(exist_ok=True)
    pages = {
        locale: BeautifulSoup((ROOT / locale / "projects.html").read_text(encoding="utf-8"), "html.parser")
        for locale in LOCALES
    }

    for project_id, slug in SLUGS.items():
        folder = INPUT_ROOT / slug
        text_dir, image_dir, video_dir = folder / "text", folder / "images", folder / "video"
        for directory in (text_dir, image_dir, video_dir):
            directory.mkdir(parents=True, exist_ok=True)

        for locale, soup in pages.items():
            section = soup.find("section", id=project_id)
            assert section is not None
            target = text_dir / f"{locale}.json"
            target.write_text(
                json.dumps(localized_record(section), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        source_section = pages["en"].find("section", id=project_id)
        video = source_path(source_section.select_one("video")["src"])
        shutil.copy2(video, video_dir / video.name)

        media = []
        poster = source_section.select_one("video").get("poster")
        if poster:
            media.append(source_path(poster))
        media.extend(source_path(image["src"]) for image in source_section.select(".photo-carousel img"))
        for image in dict.fromkeys(media):
            shutil.copy2(image, image_dir / image.name)

        inventory = {
            "project_id": project_id,
            "slug": slug,
            "private_input": True,
            "text_files": sorted(path.name for path in text_dir.iterdir() if path.is_file()),
            "image_files": sorted(path.name for path in image_dir.iterdir() if path.is_file()),
            "video_files": sorted(path.name for path in video_dir.iterdir() if path.is_file()),
        }
        (folder / "source-inventory.json").write_text(
            json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    print(f"Organized {len(SLUGS)} private project input folders.")


if __name__ == "__main__":
    main()
