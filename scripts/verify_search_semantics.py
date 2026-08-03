from pathlib import Path
import json

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
expected_types = {"index.html":"WebSite", "products.html":"CollectionPage", "projects.html":"CollectionPage", "contact.html":"ContactPage"}
for lang in ("en","tw","jp"):
    for filename, expected in expected_types.items():
        page = ROOT / lang / filename
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        assert len(soup.select('meta[property="og:title"]')) == 1, page
        assert len(soup.select('meta[property="og:description"]')) == 1, page
        assert len(soup.select('meta[property="og:image"]')) == 1, page
        assert len(soup.select('meta[name="twitter:card"]')) == 1, page
        stale = ("full commercial furniture catalog", "60+ dining chairs", "全球商業空間家具案例", "棒球場 VIP", "天板組み合わせシミュレーター", "野球場VIP")
        searchable = soup.title.get_text(" ", strip=True) + " " + soup.select_one('meta[name="description"]')["content"]
        assert not any(term.lower() in searchable.lower() for term in stale), f"Stale search copy: {page}"
        schemas = [json.loads(node.string or node.get_text()) for node in soup.select('script[type="application/ld+json"]')]
        assert expected in {schema.get("@type") for schema in schemas}, f"Missing {expected}: {page}"
        if filename in {"products.html","projects.html"}:
            schema = next(x for x in schemas if x.get("@type") == "CollectionPage")
            assert schema["mainEntity"]["numberOfItems"] == 3
    for page in list((ROOT/lang/"products").glob("*.html")) + list((ROOT/lang/"projects").glob("*.html")):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        assert len(soup.select('meta[name="twitter:card"]')) == 1, page

llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
assert llms.count("dimensions, materials and product images") == 3
assert llms.count("installation video and site images available") == 3
assert "office furniture, dining chairs, bar stools" not in llms
print("Verified governed social metadata, page schemas and AI-readable public records.")
