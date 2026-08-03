"""Single source of truth for public site URLs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "site_config.json"
CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
PRODUCTION_ORIGIN = CONFIG["production_origin"].rstrip("/")
GITHUB_PAGES_ORIGIN = CONFIG["github_pages_origin"].rstrip("/")
CUSTOM_DOMAIN = CONFIG["custom_domain"]
DEFAULT_LANGUAGE = CONFIG["default_language"]
LANGUAGES = CONFIG["languages"]


def public_url(path: str = "") -> str:
    """Return an absolute production URL from a root-relative path."""
    return f"{PRODUCTION_ORIGIN}/{path.lstrip('/')}"
