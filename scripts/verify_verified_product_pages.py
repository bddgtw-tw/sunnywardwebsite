from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from site_config import public_url


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "verified_product_pages.json"
PROJECT_SOURCE = ROOT / "data" / "verified_project_pages.json"
LANGS = ("en", "tw", "jp")


class PageSignals(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.canonical = ""
        self.alternates: dict[str, str] = {}
        self.images: list[dict[str, str | None]] = []
        self.jsonld: list[str] = []
        self._jsonld = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href", "")
        elif tag == "link" and values.get("rel") == "alternate":
            self.alternates[values.get("hreflang", "")] = values.get("href", "")
        elif tag == "img":
            self.images.append(values)
        elif tag == "script" and values.get("type") == "application/ld+json":
            self._jsonld = True
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._jsonld:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._jsonld:
            self.jsonld.append("".join(self._buffer))
            self._jsonld = False


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    project_slugs = {
        project["slug"]
        for project in json.loads(PROJECT_SOURCE.read_text(encoding="utf-8"))["projects"]
    }
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    errors: list[str] = []

    for lang in LANGS:
        catalog = json.loads((ROOT / lang / "products.json").read_text(encoding="utf-8"))
        records = {item["sku"]: item for item in catalog["products"]}
        catalogue_html = (ROOT / lang / "products.html").read_text(encoding="utf-8")
        for product in source["products"]:
            sku = product["sku"]
            slug = product["slug"]
            page_path = ROOT / lang / "products" / f"{slug}.html"
            canonical = public_url(f"{lang}/products/{slug}.html")
            if not page_path.exists():
                fail(errors, f"Missing page: {page_path.relative_to(ROOT)}")
                continue

            page_html = page_path.read_text(encoding="utf-8")
            parser = PageSignals()
            parser.feed(page_html)
            if parser.h1 != 1:
                fail(errors, f"{page_path.relative_to(ROOT)} has {parser.h1} H1 elements")
            if parser.canonical != canonical:
                fail(errors, f"Canonical mismatch: {page_path.relative_to(ROOT)}")
            if set(parser.alternates) != {"x-default", "en", "zh-TW", "ja"}:
                fail(errors, f"Hreflang set mismatch: {page_path.relative_to(ROOT)}")
            if canonical not in sitemap:
                fail(errors, f"Missing sitemap URL: {canonical}")
            if f'products/{slug}.html' not in catalogue_html:
                fail(errors, f"Missing static catalogue link: {lang}/products/{slug}.html")
            if len(parser.jsonld) != 3:
                fail(errors, f"Expected Organization, Product and Breadcrumb JSON-LD: {page_path.relative_to(ROOT)}")
            else:
                schemas = [json.loads(block) for block in parser.jsonld]
                if {item.get("@type") for item in schemas} != {"Organization", "Product", "BreadcrumbList"}:
                    fail(errors, f"Unexpected JSON-LD types: {page_path.relative_to(ROOT)}")
                product_schema = next(item for item in schemas if item.get("@type") == "Product")
                if product_schema.get("countryOfOrigin", {}).get("name") != product["origin"]:
                    fail(errors, f"Missing schema origin: {page_path.relative_to(ROOT)}")
                properties = product_schema.get("additionalProperty", [])
                if len(properties) != 1 or properties[0].get("value") != product["dimensions"]["raw"]:
                    fail(errors, f"Missing schema dimensions: {page_path.relative_to(ROOT)}")

            reference = product.get("planning_reference")
            if reference not in project_slugs:
                fail(errors, f"Unknown planning reference for {sku}: {reference}")
            if f'../projects/{reference}.html' not in page_html:
                fail(errors, f"Missing bounded project reference: {page_path.relative_to(ROOT)}")
            if 'class="verified-product-procurement"' not in page_html:
                fail(errors, f"Missing procurement guidance: {page_path.relative_to(ROOT)}")
            if f'../contact.html?product={sku}' not in page_html:
                fail(errors, f"Missing contextual enquiry link: {page_path.relative_to(ROOT)}")
            if page_html.count('class="verified-product-reference"') != 1:
                fail(errors, f"Unexpected project-reference count: {page_path.relative_to(ROOT)}")

            if len(parser.images) != len(product["images"]):
                fail(errors, f"Product image count mismatch: {page_path.relative_to(ROOT)}")
            if len(product.get("image_dimensions", [])) != len(product["images"]):
                fail(errors, f"Image dimension metadata mismatch for {sku}")
            for index, image in enumerate(parser.images):
                src = image.get("src") or ""
                local = (page_path.parent / src).resolve()
                if not local.exists():
                    fail(errors, f"Missing image {src} from {page_path.relative_to(ROOT)}")
                    continue
                if local.stat().st_size > 500_000:
                    fail(errors, f"Oversized public image {src}: {local.stat().st_size} bytes")
                expected_width, expected_height = product["image_dimensions"][index]
                if image.get("width") != str(expected_width) or image.get("height") != str(expected_height):
                    fail(errors, f"Image dimensions missing or wrong for {src}")
                if image.get("decoding") != "async":
                    fail(errors, f"Missing async decoding for {src}")
                if index == 0:
                    if image.get("loading") != "eager" or image.get("fetchpriority") != "high":
                        fail(errors, f"First product image is not prioritized: {page_path.relative_to(ROOT)}")
                elif image.get("loading") != "lazy" or image.get("fetchpriority"):
                    fail(errors, f"Secondary product image loads eagerly: {src}")

            record = records.get(sku)
            if not record:
                fail(errors, f"Missing catalog SKU {sku} in {lang}")
                continue
            if record.get("detail_page") != f"products/{slug}.html":
                fail(errors, f"Catalog detail link mismatch for {lang}/{sku}")
            if record.get("dimensions") != product.get("dimensions"):
                fail(errors, f"Catalog dimension mismatch for {lang}/{sku}")
            if record.get("name") != product["locales"][lang]["name"]:
                fail(errors, f"Catalog name mismatch for {lang}/{sku}")

    if errors:
        print("Verified product page checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Verified {len(source['products']) * len(LANGS)} product pages, catalog links, images, schemas and sitemap entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
