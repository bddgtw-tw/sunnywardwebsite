#!/usr/bin/env python3
"""Rebuild the governed public site and run every release verifier."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
BUILD_STEPS = (
    "export_db_to_json.py",
    "govern_public_catalog.py",
    "generate_about_pages.py",
    "generate_verified_product_pages.py",
    "sanitize_public_product_catalogs.py",
    "generate_verified_project_pages.py",
    "govern_project_brand_copy.py",
    "sync_verified_homepage_projects.py",
    "govern_homepage_brand.py",
    "govern_public_claims.py",
    "govern_primary_navigation.py",
    "govern_public_footers.py",
    "govern_language_navigation.py",
    "govern_contact_brief.py",
    "govern_organization_schema.py",
    "govern_customer_facing_language.py",
    "govern_project_video_posters.py",
    "fix_locale_html_paths.py",
    "govern_entry_media.py",
    "build_project_content_folders.py",
    "govern_project_listing_media.py",
    "build_search_sitemap.py",
    "build_llms_txt.py",
)


def run(script: Path) -> None:
    print(f"\n==> {script.name}", flush=True)
    subprocess.run([sys.executable, str(script)], cwd=ROOT, check=True)


def main() -> int:
    for name in BUILD_STEPS:
        run(SCRIPTS / name)
    verifiers = sorted(SCRIPTS.glob("verify_*.py"))
    for verifier in verifiers:
        run(verifier)
    print(f"\nPublic-site release gate passed: {len(BUILD_STEPS)} build steps and {len(verifiers)} verifiers.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
