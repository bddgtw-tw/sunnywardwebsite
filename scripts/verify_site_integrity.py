from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
LANGS = ("en", "tw", "jp")
ALLOWED_TYPES = {"Corporation", "ContactPoint", "PostalAddress", "Product", "Brand", "Country", "PropertyValue", "BreadcrumbList", "ListItem", "CreativeWork", "VideoObject", "Organization", "WebSite", "CollectionPage", "ItemList", "ContactPage"}
projects = json.loads((ROOT / "data" / "verified_project_pages.json").read_text(encoding="utf-8"))["projects"]
products = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
BANNED_HOMEPAGE_CLAIMS = ("across 30+ countries", "Countries Served", "Every product in our catalogue meets", "eliminating storage costs", "dedicated material science team", "行銷全球 30", "產品線均通過美、歐、日", "大幅減少現場等待與倉儲", "専属の材料科学", "輸出国", "米・欧・日規格", "保管コストを劇的に削減", "Exclusive Partnership", "獨家合作夥伴", "独占提携パートナー")


def walk_schema(value: object, page: Path) -> None:
    if isinstance(value, dict):
        schema_type = value.get("@type")
        if schema_type:
            assert schema_type in ALLOWED_TYPES, f"Unknown schema type {schema_type!r}: {page}"
        for child in value.values():
            walk_schema(child, page)
    elif isinstance(value, list):
        for child in value:
            walk_schema(child, page)


for lang in LANGS:
    homepage = ROOT / lang / "index.html"
    home_text = homepage.read_text(encoding="utf-8")
    home = BeautifulSoup(home_text, "html.parser")
    cards = home.select(".projects-grid > a.project-card")
    assert len(cards) == len(projects), f"Wrong homepage project count: {lang}"
    assert "images.unsplash.com/photo-1493976040374" not in home_text
    assert "images.unsplash.com/photo-1517248135467" not in home_text
    assert "images.unsplash.com/photo-1560185007" not in home_text
    assert "images.unsplash.com/photo-1617814076367" not in home_text
    assert not any(claim in home_text for claim in BANNED_HOMEPAGE_CLAIMS), f"Unsupported homepage claim: {lang}"
    for project in projects:
        href = f'projects/{project["slug"]}.html'
        assert len(home.select(f'a.project-card[href="{href}"]')) == 1, f"Missing verified homepage project: {lang} {href}"
    for product in (products[0], products[2]):
        href = f'products/{product["slug"]}.html'
        assert len(home.select(f'a[href="{href}"]')) == 1, f"Missing verified homepage product: {lang} {href}"

    for page in sorted((ROOT / lang).glob("**/*.html")):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        assert soup.title and soup.title.get_text(strip=True), f"Missing title: {page}"
        assert len(soup.select('meta[name="description"]')) == 1, f"Missing description: {page}"
        assert len(soup.select('link[rel="canonical"]')) == 1, f"Missing canonical: {page}"
        assert len(soup.select('link[rel="alternate"][hreflang]')) == 4, f"Wrong hreflang count: {page}"
        assert len(soup.select("h1")) == 1, f"Wrong H1 count: {page}"
        for node in soup.select('script[type="application/ld+json"]'):
            walk_schema(json.loads(node.string or node.get_text()), page)

robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
assert "Sitemap: https://sunnyward.com/sitemap.xml" in robots
print("Verified multilingual metadata, schema types, homepage project evidence and robots policy.")
