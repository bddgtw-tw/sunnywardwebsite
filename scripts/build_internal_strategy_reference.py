#!/usr/bin/env python3
"""Build private brand DNA and project decision-maker reference records."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAND_DIR = ROOT / "internal-reference" / "brand"


DNA = {
    "document": "Sunnyward enterprise DNA",
    "version": "1.0",
    "status": "internal_reference",
    "public_export": False,
    "purpose": "Guide future AI decisions, brand writing, design direction and project interpretation; not customer-facing copy.",
    "evidence_boundary": {
        "supported": [
            "Furniture and international trade experience since 1988",
            "Commercial furniture sourcing, customization and project coordination",
            "Regional operating presence in Malaysia and Singapore",
            "Focus on hospitality, restaurant, leisure, office, retail and commercial environments",
            "Available project media demonstrates installed furniture in completed spaces",
        ],
        "not_yet_supported": [
            "Exact project quantities, specifications, contract scope or commercial outcomes",
            "Named customer testimonials or attributed quotations",
            "Performance, revenue, traffic, durability or sustainability metrics",
            "Claims that Sunnyward designed or delivered an entire project unless approved documents confirm the scope",
        ],
    },
    "core_identity": {
        "category": "B2B commercial furniture project partner",
        "role": "Connect design intent with practical furniture sourcing, customization and project coordination.",
        "geographic_character": "Southeast Asia grounded, internationally usable, operationally pragmatic.",
        "brand_archetype": ["experienced guide", "practical coordinator", "design-conscious operator"],
        "desired_impression": ["quiet confidence", "commercial reliability", "refined judgment", "approachable expertise"],
    },
    "brand_promise": "Help commercial-space teams move from furniture intent to a coordinated, practical and visually coherent result.",
    "principles": [
        {"name": "Commercial reality first", "meaning": "Balance appearance with circulation, maintenance, repeat use, lead time and operational constraints."},
        {"name": "Coherence over spectacle", "meaning": "Furniture should reinforce the whole space rather than compete for attention."},
        {"name": "Evidence before claims", "meaning": "Separate documented facts, reasonable interpretation and unverified assumptions."},
        {"name": "Coordination reduces friction", "meaning": "Create a clearer route across selection, customization, review and delivery planning."},
        {"name": "Regional intelligence", "meaning": "Consider Southeast Asian climate, hospitality patterns, maintenance conditions and commercial use."},
    ],
    "primary_audiences": [
        {"role": "Owner, developer or operator", "needs": ["commercial fit", "brand coherence", "budget and schedule confidence", "operational usability"]},
        {"role": "Architect or interior designer", "needs": ["design-intent alignment", "material and finish options", "technical coordination", "clear review process"]},
        {"role": "Procurement or project manager", "needs": ["specification clarity", "repeatability", "lead-time visibility", "risk and delivery coordination"]},
        {"role": "Operations or facilities lead", "needs": ["durability", "maintenance", "circulation", "replacement practicality"]},
    ],
    "verbal_identity": {
        "tone": ["clear", "measured", "specific", "commercially literate", "warm but not promotional"],
        "prefer": ["can support", "designed to consider", "helps coordinate", "shown in the completed setting", "project-specific review"],
        "avoid": ["best-in-class", "guaranteed results", "transformative", "revolutionary", "perfect", "unsupported superlatives"],
    },
    "visual_identity": {
        "character": ["architectural calm", "material warmth", "functional elegance", "generous negative space", "credible commercial environments"],
        "motion": "Slow, stable and deliberate; never shaky, flashy or social-media paced.",
        "palette": ["warm timber", "sand", "stone", "muted bronze", "deep olive", "charcoal"],
        "avoid": ["residential styling", "excess gold", "neon color", "visual clutter", "unreal furniture geometry"],
    },
    "ai_use_rules": [
        "Use this file as interpretation guidance, never as proof of a specific project fact.",
        "Do not publish internal personas, anxieties or hypotheses as statements made by a real client.",
        "When project evidence is incomplete, describe what a buyer can evaluate and what the approach can reasonably support.",
        "Keep internal strategy separate from localized public copy.",
    ],
}


COMMON_PENDING = [
    "Who approved the furniture and what was their formal role?",
    "What products, quantities, finishes and custom requirements were approved?",
    "What constraints, standards, budget range and delivery milestones applied?",
    "What exact scope was performed by Sunnyward?",
    "Is there an approved client quotation or measurable outcome?",
]


PROFILES = {
    "ampang-cafe-furniture-installation": {
        "project_id": "case-ampang-cafe", "date": "2025-10", "space_type": "cafe / food and beverage", "furniture_focus": "upholstered lounge seating",
        "persona": {"role": "Cafe owner-operator or interior project lead", "context": "Creating a destination cafe where atmosphere and dwell time matter alongside efficient service.", "priorities": ["distinctive but coherent guest atmosphere", "comfortable dwell time", "clear circulation around lounge volumes", "materials that can be maintained in daily F&B use"], "anxieties": ["oversized seating reducing usable capacity", "upholstery aging poorly", "furniture competing with the interior concept"], "success": "A memorable cafe environment that remains comfortable, navigable and operationally practical."},
        "interpretation": "Use the project to discuss how lounge furniture scale, spacing and upholstery can reinforce a hospitality concept without obstructing movement.",
    },
    "dragon-ginseng-interior-furniture": {
        "project_id": "case-massage", "date": "2024-05", "space_type": "wellness / arrival and waiting", "furniture_focus": "sofa and lounge seating",
        "persona": {"role": "Wellness business operator or guest-experience manager", "context": "Managing a customer journey in which the arrival and waiting area should reduce visual and emotional friction.", "priorities": ["calm first impression", "comfortable waiting", "appropriate personal space", "easy cleaning and upkeep"], "anxieties": ["a clinical or crowded feeling", "seating that wears visibly", "poor circulation at reception"], "success": "A composed transition space that supports comfort and confidence before the service begins."},
        "interpretation": "Frame furniture as part of the arrival experience and spatial calm, without claiming therapeutic or business outcomes.",
    },
    "family-restaurant-furniture-installation": {
        "project_id": "case-woodfire", "date": "2024-01", "space_type": "family restaurant", "furniture_focus": "dining chairs",
        "persona": {"role": "Restaurant operator or operations manager", "context": "Serving mixed family groups in a repeat-use dining environment with changing party sizes.", "priorities": ["flexible table groupings", "comfortable seating", "clear service aisles", "durable and cleanable finishes"], "anxieties": ["congestion during peak periods", "inconsistent chair placement", "maintenance burden", "capacity lost through poor spacing"], "success": "A dining layout that feels welcoming while supporting everyday service and reconfiguration."},
        "interpretation": "Focus on seating rhythm, adaptable groupings and the balance between capacity, comfort and circulation.",
    },
    "kai-restaurant-furniture-installation": {
        "project_id": "case-hotel-fb", "date": "2026-01", "space_type": "premium restaurant / hotel F&B", "furniture_focus": "dining chairs",
        "persona": {"role": "Hotel F&B leader, restaurant owner or design project manager", "context": "Delivering a premium dining environment where guest comfort, service movement and visual consistency must work together.", "priorities": ["refined guest impression", "chair comfort across a full meal", "alignment with the interior palette", "unobstructed table service"], "anxieties": ["furniture appearing generic", "seat proportions conflicting with tables", "visual inconsistency across repeated placements", "service clearances being overlooked"], "success": "A composed dining room in which furniture supports both the hospitality experience and practical service."},
        "interpretation": "Use as a reference for premium dining coordination, material harmony and service-aware spacing; do not imply full interior design scope.",
    },
    "legoland-cafeteria-furniture-installation": {
        "project_id": "case-legoland-cafe", "date": "2025-12", "space_type": "attraction cafeteria", "furniture_focus": "high-traffic tables and chairs",
        "persona": {"role": "Attraction F&B operations or facilities manager", "context": "Managing high-volume family dining with strong visual branding and rapid turnover.", "priorities": ["high-throughput seating", "family-friendly layouts", "easy cleaning", "clear circulation", "visual alignment with the venue"], "anxieties": ["peak-time bottlenecks", "furniture damage", "slow reset and cleaning", "layouts that do not accommodate groups"], "success": "A robust, recognizable cafeteria environment that supports fast daily operations and varied family groups."},
        "interpretation": "Discuss high-traffic planning, color coordination and operational reset without claiming visitor or revenue results.",
    },
    "ll-waterpark-poolside-furniture-installation": {
        "project_id": "case-waterpark", "date": "2025-05", "space_type": "waterpark poolside", "furniture_focus": "outdoor leisure furniture",
        "persona": {"role": "Leisure venue operator or facilities manager", "context": "Planning rest zones in a wet, exposed and high-circulation public environment.", "priorities": ["weather and moisture suitability", "safe circulation", "movable rest-zone planning", "maintenance and storage practicality"], "anxieties": ["slip or obstruction risks", "rapid material deterioration", "furniture drifting into circulation routes", "uneven distribution of rest areas"], "success": "Clearly defined, inviting poolside rest zones that remain practical to manage under outdoor conditions."},
        "interpretation": "Focus on exposure, spacing, circulation and operational placement; avoid unsupported claims about material performance.",
    },
    "noodles-restaurant-furniture-installation": {
        "project_id": "case-noodles", "date": "2024-04", "space_type": "casual noodle restaurant", "furniture_focus": "compact dining chairs",
        "persona": {"role": "Fast-casual restaurant operator or rollout manager", "context": "Balancing compact floor use, customer turnover and a recognizable dining identity.", "priorities": ["efficient seating density", "quick cleaning and reset", "clear customer and staff movement", "consistent repeated furniture"], "anxieties": ["crowded aisles", "chairs obstructing service", "finishes that show wear quickly", "a generic or mismatched appearance"], "success": "An efficient dining floor that remains coherent, approachable and easy to operate."},
        "interpretation": "Use the project to explore compact planning, repeatability and service clearance rather than promising turnover improvements.",
    },
    "office-outdoor-area-furniture-installation": {
        "project_id": "case-office-outdoor", "date": "2024-01", "space_type": "office outdoor area", "furniture_focus": "outdoor seating",
        "persona": {"role": "Workplace, facilities or corporate real-estate manager", "context": "Extending the workplace into an outdoor area for breaks, informal conversation and flexible use.", "priorities": ["everyday comfort", "weather-aware materials", "easy maintenance", "clear access", "visual alignment with workplace architecture"], "anxieties": ["an underused outdoor area", "furniture that is difficult to maintain", "poor shade or circulation relationships", "an improvised appearance"], "success": "A credible extension of the workplace that feels intentional and supports multiple informal uses."},
        "interpretation": "Discuss flexible workplace use and architectural coherence without asserting productivity or wellbeing outcomes.",
    },
    "sushi-plus-outlet-furniture-installation": {
        "project_id": "case-sushi-plus", "date": "2026-06", "space_type": "chain restaurant outlet", "furniture_focus": "dining chairs and tables",
        "persona": {"role": "Chain rollout, procurement or outlet operations manager", "context": "Delivering a recognizable outlet format within a compact commercial footprint and repeatable procurement process.", "priorities": ["brand consistency", "repeatable specifications", "compact seating efficiency", "fast maintenance and replacement", "opening-schedule coordination"], "anxieties": ["variation between outlets", "procurement delays", "furniture that conflicts with brand colors", "replacement parts or models becoming difficult to source"], "success": "A coherent outlet environment with practical, repeatable furniture choices and clear operating space."},
        "interpretation": "Frame the project around outlet consistency, repeatability and compact planning; do not claim chain-wide scope unless verified.",
    },
    "tsutaya-bookstore-furniture-installation": {
        "project_id": "case-toastmaster", "date": "2024-11", "space_type": "bookstore / mixed-use retail", "furniture_focus": "chairs, tables and lounge seating",
        "persona": {"role": "Retail experience, store development or facilities manager", "context": "Supporting browsing, reading, waiting and casual work within a culture-led retail environment.", "priorities": ["longer-use comfort", "different seating modes", "quiet visual integration", "clear sightlines and circulation", "durable public-use materials"], "anxieties": ["seating disrupting merchandise flow", "an overly office-like atmosphere", "mixed furniture feeling uncoordinated", "maintenance in a high-touch environment"], "success": "A layered retail environment where furniture supports varied dwell activities without overwhelming the bookstore experience."},
        "interpretation": "Use as a reference for mixed-use seating and dwell-oriented retail planning; avoid classifying it as an office project.",
    },
}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    write_json(BRAND_DIR / "sunnyward-enterprise-dna.json", DNA)
    for slug, profile in PROFILES.items():
        record = {
            "schema_version": "1.0",
            "status": "internal_reference",
            "public_export": False,
            "project_id": profile["project_id"],
            "slug": slug,
            "source_basis": {
                "confirmed": [
                    f"Archived project media dated {profile['date']}",
                    f"Media-backed space classification: {profile['space_type']}",
                    f"Visible furniture focus: {profile['furniture_focus']}",
                ],
                "unavailable": ["approved client brief", "contract scope", "product schedule", "quantities", "specifications", "client interview", "measured outcome"],
            },
            "working_decision_maker_persona": {"evidence_status": "inferred_for_internal_planning", **profile["persona"]},
            "project_background_hypothesis": {"evidence_status": "inferred_for_internal_planning", "guidance": profile["interpretation"]},
            "publication_boundary": [
                "Do not identify this persona as the actual client or quote it as a real stakeholder.",
                "Do not convert priorities, anxieties or success criteria into claims about completed outcomes.",
                "Public copy may describe observable conditions and reasonable project considerations using bounded language.",
                "Replace inferred content when approved project documents become available.",
            ],
            "pending_verification": COMMON_PENDING,
        }
        write_json(ROOT / "project-input" / slug / "text" / "strategy.json", record)
    print(f"Built one enterprise DNA record and {len(PROFILES)} private project strategy records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
