#!/usr/bin/env python3
"""Verify the shared public project-folder contract."""

import json
from pathlib import Path

from build_project_content_folders import LOCALES, OUTPUT, SLUGS


for slug in SLUGS.values():
    folder = OUTPUT / slug
    assert folder.is_dir(), folder
    for name in ("text", "images", "video"):
        assert (folder / name).is_dir(), folder / name
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["slug"] == slug
    assert set(manifest["text"]) == set(LOCALES)
    assert len(manifest["images"]) >= 5
    assert manifest["video"].startswith("video/project-film.")
    for locale in LOCALES:
        payload = json.loads((folder / manifest["text"][locale]).read_text(encoding="utf-8"))
        assert payload["title"] and len(payload["sections"]) == 3
    for relative in [*manifest["images"], manifest["video"]]:
        assert (folder / relative).is_file(), folder / relative

assert len([path for path in OUTPUT.iterdir() if path.is_dir()]) == len(SLUGS)
print(f"Verified {len(SLUGS)} project folders with text, images and video subfolders.")
