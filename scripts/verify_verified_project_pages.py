from __future__ import annotations

import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from site_config import public_url


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "verified_project_pages.json").read_text(encoding="utf-8"))
LANGS = ("en", "tw", "jp")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for project in DATA["projects"]:
        require((ROOT / project["video"]).stat().st_size > 0, f"Missing video: {project['video']}")
        for image in project["images"]:
            require((ROOT / image).stat().st_size > 0, f"Missing image: {image}")
        for lang in LANGS:
            loc = project["locales"][lang]
            page = ROOT / lang / "projects" / f'{project["slug"]}.html'
            text = page.read_text(encoding="utf-8")
            soup = BeautifulSoup(text, "html.parser")
            canonical = public_url(f'{lang}/projects/{project["slug"]}.html')
            require(soup.select_one("h1") and soup.select_one("h1").get_text(strip=True) == loc["name"], f"Wrong H1: {page}")
            require(soup.select_one('link[rel="canonical"]') and soup.select_one('link[rel="canonical"]')["href"] == canonical, f"Wrong canonical: {page}")
            require(len(soup.select('link[rel="alternate"]')) == 4, f"Wrong hreflang count: {page}")
            require(text.count('application/ld+json') == 3, f"Wrong schema count: {page}")
            require('"@type":"Organization"' in text and '"@type":"CreativeWork"' in text and '"@type":"VideoObject"' in text, f"Missing schema: {page}")
            video = soup.select_one("video[controls]")
            require(video is not None, f"Missing video tag: {page}")
            require(video.get("playsinline") is not None and video.get("preload") == "none", f"Project video must load on demand: {page}")
            require(video.get("poster", "").startswith("../../") and video.get("aria-label"), f"Missing video poster or label: {page}")
            require(project["slug"] in sitemap, f"Missing sitemap entry: {canonical}")
            listing = (ROOT / lang / "projects.html").read_text(encoding="utf-8")
            require(listing.count(f'href="projects/{project["slug"]}.html"') == 1, f"Wrong list link: {lang}/{project['slug']}")
            banned = ("ten times", "zero stain", "guest satisfaction", "client testimonial")
            require(not any(x in text.lower() for x in banned), f"Unsupported claim: {page}")
            require(not re.search(r'href="https://bddgtw-tw\.github\.io', text), f"GitHub URL embedded: {page}")
    expected = len(DATA["projects"]) * len(LANGS)
    require(len(re.findall(r'<loc>[^<]*/projects/[^<]+</loc>', sitemap)) == expected, "Unexpected project detail sitemap count")
    print(f"Verified {expected} localized project pages, list links, local media, schemas and sitemap entries.")


if __name__ == "__main__":
    main()
