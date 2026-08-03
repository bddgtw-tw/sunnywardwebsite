from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
script = (ROOT / "js" / "contact-inquiry.js").read_text(encoding="utf-8")
assert "window.location.href = `mailto:" not in script
assert "mailto:sales@sunnyward.com" in script
assert "https://wa.me/60165262894" in script
assert "Nothing has been sent" not in script  # Exact copy differs by locale; transmission remains user-triggered.
assert "form.reportValidity()" in script and "navigator.clipboard.writeText" in script
for removed in ("value('project_type')", "value('market')", "value('quantity')", "value('timeline')"):
    assert removed not in script, f"Removed high-friction field remains in draft: {removed}"

for lang in ("en", "tw", "jp"):
    page = (ROOT / lang / "contact.html").read_text(encoding="utf-8")
    assert page.count('id="contact-inquiry-form"') == 1
    assert page.count('src="../js/contact-inquiry.js?v=20260715-b2b-brief"') == 1
    assert "window.location.href = `mailto:" not in page
    for name in ("name", "company", "email", "phone", "subject", "message"):
        assert page.count(f'name="{name}"') == 1, f"Missing field {lang}:{name}"
    for removed_name in ("project_type", "market", "quantity", "timeline"):
        assert f'name="{removed_name}"' not in page, f"High-friction field remains {lang}:{removed_name}"
    for required_id in ("contact-name", "contact-email", "contact-message"):
        element = page.split(f'id="{required_id}"', 1)[1].split('>', 1)[0]
        assert " required" in element, f"Required field not enforced {lang}:{required_id}"
    assert page.count('id="inquiry-actions"') == 1
    assert page.count('id="inquiry-email-action"') == 1
    assert page.count('id="inquiry-whatsapp-action"') == 1
    assert page.count('id="inquiry-copy-action"') == 1
    assert "within 2 hours" not in page and "2 小時內" not in page and "2時間以内" not in page
    assert "60167252894" in page
print("Verified explicit user-controlled Email and WhatsApp enquiry flows for three languages.")
