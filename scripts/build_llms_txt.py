from pathlib import Path
import json
from site_config import public_url


ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / "data" / "verified_product_pages.json").read_text(encoding="utf-8"))["products"]
projects = json.loads((ROOT / "data" / "verified_project_pages.json").read_text(encoding="utf-8"))["projects"]
lines = ["# Sunnyward", "", "> Sunnyward provides commercial furniture sourcing, customization and project coordination for architects, designers, hospitality operators and project buyers.", "", "## Official multilingual pages", f"- [English]({public_url('en/')})", f"- [Traditional Chinese]({public_url('tw/')})", f"- [Japanese]({public_url('jp/')})", "", "## Selected commercial products"]
for product in products:
    product_url = public_url(f"en/products/{product['slug']}.html")
    lines.append(f"- [{product['locales']['en']['name']}]({product_url}) — SKU {product['sku']}; dimensions, materials and product images.")
lines += ["", "## Commercial furniture projects"]
for project in projects:
    project_url = public_url(f"en/projects/{project['slug']}.html")
    lines.append(f"- [{project['locales']['en']['name']}]({project_url}) — {project['date']}; installation video and site images available.")
lines += ["", "## Enquiries", f"- [Prepare a project enquiry]({public_url('en/contact.html')})", "- Sales email: sales@sunnyward.com", "- WhatsApp: +6016-526 2894 & +6016-725 2894", "- Include product SKU or reference project, company, delivery market, quantity and target timeline.", "", "## Languages", "- English, Traditional Chinese and Japanese."]
(ROOT / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
print(f"Built llms.txt with {len(products)} products and {len(projects)} commercial projects.")
