#!/usr/bin/env python3
"""Verify that public search signals follow the configured production origin."""

from __future__ import annotations

import argparse
import json
import re
import socket
import ssl
import urllib.request
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
from urllib.parse import urlparse

from site_config import (
    CONFIG_PATH,
    CUSTOM_DOMAIN,
    GITHUB_PAGES_ORIGIN,
    LANGUAGES,
    PRODUCTION_ORIGIN,
    ROOT,
    public_url,
)


class SearchSignals(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonical: list[str] = []
        self.alternates: list[tuple[str, str]] = []
        self.og_urls: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical.append(values.get("href") or "")
        if tag == "link" and values.get("rel") == "alternate" and values.get("hreflang"):
            self.alternates.append((values["hreflang"] or "", values.get("href") or ""))
        if tag == "meta" and values.get("property") == "og:url":
            self.og_urls.append(values.get("content") or "")


def assert_offline() -> None:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    assert PRODUCTION_ORIGIN == f"https://{CUSTOM_DOMAIN}"
    assert urlparse(GITHUB_PAGES_ORIGIN).hostname == "bddgtw-tw.github.io"
    expected_hreflangs = set(LANGUAGES.values()) | {"x-default"}
    checked = 0
    for folder in LANGUAGES:
        for page in (ROOT / folder).glob("**/*.html"):
            html = page.read_text(encoding="utf-8")
            parser = SearchSignals()
            parser.feed(html)
            robots = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
            if robots and "noindex" in robots.group(1).lower():
                continue
            assert len(parser.canonical) == 1, f"Canonical count in {page}: {parser.canonical}"
            assert parser.canonical[0].startswith(PRODUCTION_ORIGIN + "/"), page
            assert set(code for code, _ in parser.alternates) == expected_hreflangs, page
            assert all(url.startswith(PRODUCTION_ORIGIN + "/") for _, url in parser.alternates), page
            assert all(url.startswith(PRODUCTION_ORIGIN + "/") for url in parser.og_urls), page
            assert GITHUB_PAGES_ORIGIN not in html, f"Deployment origin leaked into {page}"
            checked += 1
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    assert GITHUB_PAGES_ORIGIN not in sitemap + robots + llms
    assert f"Sitemap: {public_url('sitemap.xml')}" in robots
    assert all(
        url.startswith(PRODUCTION_ORIGIN + "/")
        for url in re.findall(r"<loc>([^<]+)</loc>", sitemap)
    )
    assert config["default_language"] in LANGUAGES
    print(f"offline domain governance passed: {checked} indexable pages use {PRODUCTION_ORIGIN}")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


def assert_live() -> None:
    """Fail unless the production domain is serving the governed public site."""

    failures: list[str] = []
    try:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(CUSTOM_DOMAIN, 443)})
        print(f"live DNS {CUSTOM_DOMAIN}: {', '.join(addresses)}")
    except socket.gaierror as exc:
        failures.append(f"DNS lookup failed for {CUSTOM_DOMAIN}: {exc}")

    cname = ROOT / "CNAME"
    if not cname.exists():
        failures.append("repository CNAME is not configured")
    else:
        state = cname.read_text(encoding="utf-8").strip()
        if state != CUSTOM_DOMAIN:
            failures.append(f"repository CNAME is {state!r}, expected {CUSTOM_DOMAIN!r}")
        else:
            print(f"repository CNAME: {state}")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    public_urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    checked = 0
    context = ssl.create_default_context()
    for url in public_urls:
        try:
            with urllib.request.urlopen(url, timeout=15, context=context) as response:
                html = response.read().decode("utf-8")
                if response.status != 200:
                    failures.append(f"{url} returned HTTP {response.status}")
                    continue
                parser = SearchSignals()
                parser.feed(html)
                if parser.canonical != [url]:
                    failures.append(f"{url} canonical is {parser.canonical!r}")
                    continue
                checked += 1
        except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
            failures.append(f"{url} is not ready: {type(exc).__name__}: {exc}")
    print(f"live production pages: {checked}/{len(public_urls)} passed")

    www_url = f"https://www.{CUSTOM_DOMAIN}/"
    try:
        opener = urllib.request.build_opener(NoRedirect)
        opener.open(www_url, timeout=15)
        failures.append(f"{www_url} did not redirect to {PRODUCTION_ORIGIN}/")
    except HTTPError as exc:
        location = exc.headers.get("Location", "")
        if exc.code not in {301, 308} or location.rstrip("/") != PRODUCTION_ORIGIN:
            failures.append(f"{www_url} returned {exc.code} with Location {location!r}")
        else:
            print(f"www redirect: {exc.code} -> {location}")
    except (URLError, TimeoutError) as exc:
        failures.append(f"{www_url} is not ready: {type(exc).__name__}: {exc}")

    if failures:
        print("live domain gate failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"live domain gate passed: {CUSTOM_DOMAIN} serves {checked} governed pages")


parser = argparse.ArgumentParser()
parser.add_argument(
    "--live",
    action="store_true",
    help="require DNS, HTTPS, CNAME, all sitemap pages and the www redirect to be production-ready",
)
args = parser.parse_args()
assert_offline()
if args.live:
    assert_live()
