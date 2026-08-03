#!/usr/bin/env python3
"""Verify that private AI strategy references stay outside public deployment."""

from __future__ import annotations

import json
from pathlib import Path

from export_public_deployment import PUBLIC_DIRS


ROOT = Path(__file__).resolve().parents[1]

assert "internal-reference" not in PUBLIC_DIRS, "Internal brand references entered the public export allowlist"
assert "project-input" not in PUBLIC_DIRS, "Private project inputs entered the public export allowlist"

dna_path = ROOT / "internal-reference" / "brand" / "sunnyward-enterprise-dna.json"
dna = json.loads(dna_path.read_text(encoding="utf-8"))
assert dna["status"] == "internal_reference" and dna["public_export"] is False

strategies = sorted((ROOT / "project-input").glob("*/text/strategy.json"))
assert len(strategies) == 10, f"Expected 10 private project strategy records, found {len(strategies)}"
for path in strategies:
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["status"] == "internal_reference", f"Wrong strategy status: {path}"
    assert record["public_export"] is False, f"Strategy marked for public export: {path}"
    assert record["working_decision_maker_persona"]["evidence_status"] == "inferred_for_internal_planning"
    assert record["publication_boundary"], f"Publication boundary missing: {path}"

for directory in PUBLIC_DIRS:
    public_root = ROOT / directory
    if public_root.exists():
        assert not list(public_root.rglob("strategy.json")), f"Private strategy leaked into public directory: {directory}"

print("Verified one enterprise DNA record and 10 project strategies remain private references.")
