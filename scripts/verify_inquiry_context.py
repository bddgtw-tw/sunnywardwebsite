from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
script = (ROOT / "js" / "inquiry-context.js").read_text(encoding="utf-8")
assert "URLSearchParams" in script
assert "params.get('product')" in script and "params.get('project')" in script
assert "slice(0, 80)" in script and "slice(0, 120)" in script
for lang in ("en", "tw", "jp"):
    page = (ROOT / lang / "contact.html").read_text(encoding="utf-8")
    assert page.count('src="../js/inquiry-context.js?v=20260715-b2b-brief"') == 1, lang
    assert page.index('src="../js/inquiry-context.js?v=20260715-b2b-brief"') < page.index('src="../js/contact-inquiry.js?v=20260715-b2b-brief"'), lang
print("Verified product and project enquiry context for three contact pages.")
