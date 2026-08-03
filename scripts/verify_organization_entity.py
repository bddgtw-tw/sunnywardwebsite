#!/usr/bin/env python3
"""Verify one consistent, evidence-bounded Sunnyward entity on every public page."""

from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup

from organization_schema import ORGANIZATION_ID, organization_schema


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = organization_schema()
checked = 0


def walk(value: object):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from walk(item)
    elif isinstance(value, list):
        for item in value:
            yield from walk(item)


for lang in ("en", "tw", "jp"):
    for page in (ROOT / lang).glob("**/*.html"):
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        robots = soup.select_one('meta[name="robots"]')
        if robots and "noindex" in robots.get("content", "").lower():
            continue
        schemas = [json.loads(script.string or "") for script in soup.select('script[type="application/ld+json"]')]
        full_entities = [schema for schema in schemas if schema.get("@type") == "Organization"]
        assert full_entities == [EXPECTED], f"Organization entity mismatch: {page}"
        assert "Global" not in json.dumps(schemas, ensure_ascii=False), f"Unsupported global claim: {page}"
        for schema in schemas:
            for node in walk(schema):
                if node is schema and schema == EXPECTED:
                    continue
                if node.get("@type") in {"Organization", "Corporation"}:
                    raise AssertionError(f"Duplicate embedded organization: {page}: {node}")
        for schema in schemas:
            if schema.get("@type") == "CreativeWork":
                assert schema.get("publisher") == {"@id": ORGANIZATION_ID}, f"Publisher mismatch: {page}"
        checked += 1

assert checked == 33, f"Expected 33 indexable pages, checked {checked}"
print("verified one evidence-bounded Sunnyward organization entity on 33 public pages")
