"""Evidence-bounded Sunnyward organization entity for public structured data."""

from __future__ import annotations

from site_config import public_url


ORGANIZATION_ID = public_url("#organization")


def organization_schema() -> dict:
    return {
        "@context": "https://schema.org", "@type": "Organization", "@id": ORGANIZATION_ID,
        "name": "Sunnyward", "legalName": "Sunnyward Pte Ltd", "url": public_url(""),
        "email": "sales@sunnyward.com", "telephone": "+60165262894",
        "contactPoint": [
            {"@type": "ContactPoint", "contactType": "sales", "email": "sales@sunnyward.com", "telephone": "+60165262894", "availableLanguage": ["en", "zh-TW", "ja"]},
            {"@type": "ContactPoint", "contactType": "sales support", "email": "sales@sunnyward.com", "telephone": "+60167252894", "availableLanguage": ["en", "zh-TW", "ja"]}
        ],
        "address": [
            {"@type": "PostalAddress", "streetAddress": "27, Jalan Impian Emas 18, Taman Perusahaan Ringan Pulai", "addressLocality": "Johor Bahru", "addressRegion": "Johor", "postalCode": "81300", "addressCountry": "MY"},
            {"@type": "PostalAddress", "streetAddress": "101 Upper Cross Street, #B1-71, People's Park Centre", "addressLocality": "Singapore", "postalCode": "058387", "addressCountry": "SG"},
        ],
    }
