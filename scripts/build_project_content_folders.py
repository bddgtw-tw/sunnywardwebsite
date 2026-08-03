#!/usr/bin/env python3
"""Build one shared text/images/video content folder for every public project."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "projects"
LOCALES = ("en", "tw", "jp")
SLUGS = {
    "case-hotel-fb": "kai-restaurant-furniture-installation",
    "case-woodfire": "family-restaurant-furniture-installation",
    "case-toastmaster": "tsutaya-bookstore-furniture-installation",
    "case-massage": "dragon-ginseng-interior-furniture",
    "case-ampang-cafe": "ampang-cafe-furniture-installation",
    "case-sushi-plus": "sushi-plus-outlet-furniture-installation",
    "case-noodles": "noodles-restaurant-furniture-installation",
    "case-office-outdoor": "office-outdoor-area-furniture-installation",
    "case-legoland-cafe": "legoland-cafeteria-furniture-installation",
    "case-waterpark": "ll-waterpark-poolside-furniture-installation",
}


def source_path(value: str) -> Path:
    cleaned = value.split("?", 1)[0]
    while cleaned.startswith("../"):
        cleaned = cleaned[3:]
    path = (ROOT / cleaned).resolve()
    assert path.is_file() and ROOT.resolve() in path.parents, value
    return path


def localized_record(section) -> dict:
    blocks = section.select(".uc-text-block")
    return {
        "title": section.select_one(".ultimate-case-header h2").get_text(" ", strip=True),
        "meta": section.select_one(".ultimate-case-header .meta").get_text(" ", strip=True),
        "space_type": section.get("data-space"),
        "furniture_type": section.get("data-product"),
        "sections": [
            {
                "heading": block.select_one("h4").get_text(" ", strip=True),
                "body": block.select_one("p").get_text(" ", strip=True),
            }
            for block in blocks
        ],
    }


def main() -> None:
    assert OUTPUT.resolve().parent == ROOT.resolve()
    OUTPUT.mkdir(exist_ok=True)
    pages = {
        locale: BeautifulSoup((ROOT / locale / "projects.html").read_text(encoding="utf-8"), "html.parser")
        for locale in LOCALES
    }
    built = set()
    for project_id, slug in SLUGS.items():
        folder = OUTPUT / slug
        text_dir, image_dir, video_dir = folder / "text", folder / "images", folder / "video"
        for directory in (text_dir, image_dir, video_dir):
            directory.mkdir(parents=True, exist_ok=True)

        for locale, soup in pages.items():
            section = soup.find("section", id=project_id)
            assert section is not None, f"Missing {project_id} in {locale}"
            payload = localized_record(section)
            (text_dir / f"{locale}.json").write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )

        source_section = pages["en"].find("section", id=project_id)
        video = source_path(source_section.select_one("video")["src"])
        video_target = video_dir / f"project-film{video.suffix.lower()}"
        shutil.copy2(video, video_target)

        image_sources = []
        poster = source_section.select_one("video").get("poster")
        if poster:
            image_sources.append(source_path(poster))
        # Archive project stills independently from the public listing. The
        # customer-facing page intentionally shows one film and no screenshot
        # gallery, while these source assets remain available to the internal
        # project-content contract and detail-page pipeline.
        poster_path = source_path(poster) if poster else None
        project_prefix = poster_path.stem.removesuffix("_cropped") if poster_path else video.stem
        image_sources.extend(sorted(video.parent.glob(f"{project_prefix}_q*.jpg")))
        unique_images = list(dict.fromkeys(image_sources))
        media_images = []
        for index, image in enumerate(unique_images, start=1):
            target = image_dir / f"image-{index:02d}{image.suffix.lower()}"
            shutil.copy2(image, target)
            media_images.append(f"images/{target.name}")

        manifest = {
            "schema_version": "sunnyward-project-folder-v1",
            "project_id": project_id,
            "slug": slug,
            "text": {locale: f"text/{locale}.json" for locale in LOCALES},
            "images": media_images,
            "video": f"video/{video_target.name}",
        }
        (folder / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        built.add(slug)

    for stale in (path for path in OUTPUT.iterdir() if path.is_dir() and path.name not in built):
        shutil.rmtree(stale)
    print(f"Built {len(built)} shared project content folders with localized text, images and video.")


if __name__ == "__main__":
    main()
