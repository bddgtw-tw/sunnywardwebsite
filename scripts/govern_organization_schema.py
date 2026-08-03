#!/usr/bin/env python3
"""Synchronize the bounded Sunnyward entity on public landing pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

from organization_schema import ORGANIZATION_ID, organization_schema


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "products.html", "projects.html", "contact.html")
SCRIPT_RE = re.compile(r'\s*<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def reference_embedded_organization(value: object) -> object:
    if isinstance(value, list):
        return [reference_embedded_organization(item) for item in value]
    if not isinstance(value, dict):
        return value
    if value.get("@type") in {"Organization", "Corporation"} and (value.get("@id") == ORGANIZATION_ID or value.get("name") == "Sunnyward"):
        return {"@id": ORGANIZATION_ID}
    return {key: reference_embedded_organization(item) for key, item in value.items()}


for lang in ("en", "tw", "jp"):
    for name in PAGES:
        page = ROOT / lang / name
        text = page.read_text(encoding="utf-8")
        schemas: list[dict] = []

        def collect(match: re.Match[str]) -> str:
            schema = json.loads(match.group(1))
            is_old_entity = schema.get("@type") in {"Organization", "Corporation"} and schema.get("name") == "Sunnyward"
            if not is_old_entity:
                schemas.append(reference_embedded_organization(schema))
            return ""

        text = SCRIPT_RE.sub(collect, text)
        schemas.insert(0, organization_schema())
        rendered = "\n".join(f'  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>' for schema in schemas)
        text = text.replace("</head>", f"{rendered}\n</head>", 1)
        page.write_text(text, encoding="utf-8", newline="\n")
        print(f"governed organization entity {page.relative_to(ROOT)}")
