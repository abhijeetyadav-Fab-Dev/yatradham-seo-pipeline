"""
Champion Blog Benchmark & Checkpoint Auditor
============================================
Reverse-engineered from YatraDham's #1 All-Time Organic Blog:
URL: https://blog.yatradham.org/ro-ro-ropax-service-from-ghogha-to-hazira/
Title: "RoRo Ferry Service, Ghogha to Hazira Booking Price & Timetable"

Why this blog NEVER leaves Rank 1 on Google SERP:
1. High Information Gain: 14 structured tables (timetables, vehicle tariffs, passenger classes, ship capacities).
2. Quantified Transformation Math: 370 km saved, 12 hours reduced to 4 hours, 90 km sea route.
3. Multi-Tier Granularity: Distinct tariffs for Executive, Sleeper, Business, Cabin + Bikes, Cars, Trucks, Buses.
4. Hub-and-Spoke Onward Connections: Distance & stay guides for Somnath, Dwarka, Palitana, Sarangpur, Gir.
5. Connecting Public Transit: GSRTC connecting bus schedules with exact ticket prices (₹23).
6. Operational Rules & Policies: Strict refund % brackets, boarding cutoff, luggage and pet restrictions.
7. Nested FAQ Schema: 8 direct conversational Q&As targeting Google Quick Answers and AI Overviews.
8. Active Community E-E-A-T: 171+ reader queries personally answered by author Sanjay Dangrocha.
"""

import re
import math
from typing import Dict, Any, List, Optional, Tuple


ROPAX_CHAMPION_PROFILE: Dict[str, Any] = {
    "benchmark_url": "https://blog.yatradham.org/ro-ro-ropax-service-from-ghogha-to-hazira/",
    "title": "RoRo Ferry Service, Ghogha to Hazira Booking Price & Timetable",
    "primary_keyword": "roro ferry service ghogha to hazira",
    "total_words": 4871,
    "tables_count": 14,
    "internal_links_count": 434,
    "faqs_count": 8,
    "comments_ugc_count": 171,
    "transformation_metric": "Saves 370 km & reduces 12h road journey to 4h sea route (90 km)",
    "onward_pilgrimage_spokes": [
        {"destination": "Somnath", "distance_km": 260},
        {"destination": "Dwarka", "distance_km": 408},
        {"destination": "Sarangpur", "distance_km": 98},
        {"destination": "Bhaguda", "distance_km": 79},
        {"destination": "Palitana", "distance_km": 70},
        {"destination": "Sasan Gir", "distance_km": 225}
    ],
    "key_fare_brackets": {
        "passenger": ["Executive ₹600", "Sleeper ₹700", "Business ₹700", "VIP Cabin ₹5000", "Cambay Lounge ₹1700"],
        "vehicle": ["Car ₹1200", "Bike ₹99-₹200", "Truck ₹3000", "Bus ₹5500", "Tempo Traveller ₹3000"]
    }
}


def audit_champion_blog_benchmarks(
    content: str,
    title: str = "",
    meta_description: str = "",
    target_keyword: str = "",
    url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluates blog content against the 10 Golden Checkpoints of YatraDham's #1 Champion Blog.
    Returns a 0-100 Champion Score, checkpoint breakdown, pass/fail statuses, and actionable gaps.
    """
    total_text = f"{title}\n{meta_description}\n{content}"
    content_lower = content.lower()
    total_lower = total_text.lower()
    kw = (target_keyword or "").strip().lower()

    words = re.findall(r'\b[a-zA-Z0-9_-]+\b', content)
    word_count = len(words)

    checkpoints: List[Dict[str, Any]] = []
    recommendations: List[str] = []
    earned_score = 0.0

    # -------------------------------------------------------------------------
    # CHECKPOINT 1: Structured Data Table Density (Weight: 12 pts)
    # -------------------------------------------------------------------------
    # Counts Markdown tables (|---|) or HTML <table> tags
    md_table_matches = re.findall(r'\|(?:\s*[:-]+[-| :]*\s*)\|', content)
    html_table_matches = re.findall(r'<table\b', content, re.IGNORECASE)
    table_count = len(md_table_matches) + len(html_table_matches)

    if table_count >= 3:
        cp1_score = 12.0
        cp1_status = "PASSED"
        cp1_msg = f"Outstanding structured presentation: {table_count} tables detected (Ro-Pax benchmark: multiple comparison tables)."
    elif table_count >= 1:
        cp1_score = 7.0
        cp1_status = "PARTIAL"
        cp1_msg = f"Good start with {table_count} table(s), but champion blogs feature 3+ tables for timetables, tariffs, and capacities."
        recommendations.append("Add structured comparison tables for schedules, vehicle/passenger tariffs, and route comparisons.")
    else:
        cp1_score = 0.0
        cp1_status = "FAILED"
        cp1_msg = "No structured tables found. Champion blogs present timetables and tariffs in scannable tables, not walls of text."
        recommendations.append("Convert schedules and pricing lists into clean Markdown or HTML comparison tables.")

    checkpoints.append({
        "id": "cp1_structured_tables",
        "name": "Structured Data Table Density",
        "weight": 12,
        "score": round(cp1_score, 1),
        "status": cp1_status,
        "detail": cp1_msg,
        "actual_value": f"{table_count} tables"
    })
    earned_score += cp1_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 2: Transformation Math & Efficiency Savings (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Quantified distance, time, or cost savings (e.g. saves 370 km, 12h to 4h)
    savings_patterns = [
        r'\b(?:save|saving|saves|saved)\s+\d+\s*(?:km|kms|hours?|hrs?|percent|%)',
        r'\b(?:reduced|reduces|reducing|cut)\s+(?:from|by)\s+\d+.*?(?:to|down to)\s+\d+',
        r'\b\d+\s*(?:hours?|hrs?)\s+(?:by|via)\s+(?:road|car|bus)\s+to\s+\d+\s*(?:hours?|hrs?|minutes?|mins?)',
        r'\b(?:saves?|reduction of)\s+(?:over|around|up to)?\s*\d+\s*(?:km|kilometers|hours)',
        r'\b(?:distance|time)\s+between\s+.*?\s+(?:is|reduced to)\s+\d+\s*(?:km|hours)',
        r'\b\d+\s*km\s+(?:vs|versus|compared to)\s+\d+\s*km'
    ]
    has_transformation_math = any(re.search(pat, content_lower) for pat in savings_patterns)

    if has_transformation_math:
        cp2_score = 10.0
        cp2_status = "PASSED"
        cp2_msg = "Explicit transformation math detected (quantifies exact km, hours, or travel savings)."
    else:
        cp2_score = 0.0
        cp2_status = "FAILED"
        cp2_msg = "Missing quantified traveler efficiency savings (e.g., 'saves 370 km and cuts travel time from 12 hours to 4 hours')."
        recommendations.append("Explicitly state the exact traveler benefit: distance in km saved, travel hours saved, and route efficiency.")

    checkpoints.append({
        "id": "cp2_transformation_math",
        "name": "Traveler Transformation Math",
        "weight": 10,
        "score": round(cp2_score, 1),
        "status": cp2_status,
        "detail": cp2_msg,
        "actual_value": "Quantified savings present" if has_transformation_math else "Missing quantified comparison"
    })
    earned_score += cp2_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 3: Multi-Tier Granular Tariffs & Class Pricing (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Distinct passenger classes or vehicle tariffs with INR ₹ pricing
    inr_price_matches = re.findall(r'(?:₹|rs\.?|inr)\s*(\d{2,6}(?:,\d{3})*)', content_lower)
    pricing_count = len(inr_price_matches)
    has_classes = any(k in content_lower for k in [
        "executive", "sleeper", "business", "economy", "vip", "lounge", "cabin",
        "two-wheeler", "bike", "car", "suv", "tempo", "truck", "bus", "per vehicle", "per seat"
    ])

    if pricing_count >= 4 and has_classes:
        cp3_score = 10.0
        cp3_status = "PASSED"
        cp3_msg = f"Granular multi-tier pricing verified ({pricing_count} specific INR price points across distinct travel classes/vehicles)."
    elif pricing_count >= 2:
        cp3_score = 5.0
        cp3_status = "PARTIAL"
        cp3_msg = f"Basic pricing found ({pricing_count} prices), but lacking granular class breakdowns (e.g., Executive vs Sleeper vs Car vs Bike tariffs)."
        recommendations.append("Add a detailed multi-tier tariff matrix covering different classes, vehicle types, or seating categories.")
    else:
        cp3_score = 0.0
        cp3_status = "FAILED"
        cp3_msg = "Lacks concrete INR pricing points. High-intent travelers demand exact transparent ticket and vehicle costs."
        recommendations.append("Specify exact real-world INR pricing (₹) for all available categories, packages, or vehicle slots.")

    checkpoints.append({
        "id": "cp3_granular_pricing",
        "name": "Multi-Tier Pricing & Tariff Granularity",
        "weight": 10,
        "score": round(cp3_score, 1),
        "status": cp3_status,
        "detail": cp3_msg,
        "actual_value": f"{pricing_count} prices, classes: {has_classes}"
    })
    earned_score += cp3_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 4: Hub-and-Spoke Onward Pilgrimage Connections (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Mentions 3+ connected onward shrines/destinations with approximate distances
    spoke_destinations = [
        "somnath", "dwarka", "palitana", "sarangpur", "bhaguda", "gir", "sasan gir",
        "haridwar", "rishikesh", "badrinath", "kedarnath", "gangotri", "yamunotri",
        "ujjain", "omkareshwar", "varanasi", "ayodhya", "prayagraj", "tirupati", "madurai",
        "rameshwaram", "shirdi", "nashik", "trimbakeshwar", "bhimashankar"
    ]
    detected_spokes = [d for d in spoke_destinations if d in content_lower]
    has_spoke_distances = bool(re.search(r'\b\d+\s*(?:km|kms|kilometers)\s+(?:from|to|away)', content_lower))

    if len(detected_spokes) >= 3 and has_spoke_distances:
        cp4_score = 10.0
        cp4_status = "PASSED"
        cp4_msg = f"Excellent onward hub-and-spoke mapping: {len(detected_spokes)} connected shrines identified with distance metrics."
    elif len(detected_spokes) >= 2:
        cp4_score = 6.0
        cp4_status = "PARTIAL"
        cp4_msg = f"Mentions {len(detected_spokes)} onward destinations ({', '.join(detected_spokes[:3])}), but add exact road distances in km to each."
        recommendations.append("Map out 3 to 5 nearby pilgrimage destinations with exact driving distances (km) and best connecting routes.")
    else:
        cp4_score = 2.0
        cp4_status = "FAILED"
        cp4_msg = "Content is isolated to a single point. Champion articles act as travel hubs by linking onwards to 3-5 nearby pilgrimage sites."
        recommendations.append("Include an 'Onward Journey' section showing nearby temples/places with distances and stay recommendations.")

    checkpoints.append({
        "id": "cp4_hub_and_spoke",
        "name": "Hub-and-Spoke Onward Pilgrimage Mapping",
        "weight": 10,
        "score": round(cp4_score, 1),
        "status": cp4_status,
        "detail": cp4_msg,
        "actual_value": f"{len(detected_spokes)} spokes mapped: {', '.join(detected_spokes[:4])}"
    })
    earned_score += cp4_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 5: Commercial Monetization & YatraDham Stay CTAs (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Contextual CTA buttons or links to book verified Dharamshalas/stays on YatraDham
    yatradham_links = len(re.findall(r'https?://(?:[\w-]+\.)?yatradham\.org[^\s)"]*', content, re.IGNORECASE))
    has_stay_cta = any(k in content_lower for k in [
        "book your stay", "places to stay", "book dharamshala", "dharamshala near",
        "verified stay", "yatradham app", "download app", "yatradham.org"
    ])

    if yatradham_links >= 3 and has_stay_cta:
        cp5_score = 10.0
        cp5_status = "PASSED"
        cp5_msg = f"Optimal monetization ecosystem: {yatradham_links} contextual internal links with prominent Dharamshala/Stay CTAs."
    elif yatradham_links >= 1 or has_stay_cta:
        cp5_score = 6.0
        cp5_status = "PARTIAL"
        cp5_msg = f"Found {yatradham_links} YatraDham link(s). Add dedicated 'Book Your Stay in [Destination]' callout buttons for high conversion."
        recommendations.append("Insert explicit 'Places to Stay' sections with direct links to verified YatraDham Dharamshalas and App CTA.")
    else:
        cp5_score = 0.0
        cp5_status = "FAILED"
        cp5_msg = "No YatraDham stay or puja booking CTAs detected. The content fails to convert pilgrimage traffic into stay bookings."
        recommendations.append("Add contextual 'Book Your Stay' CTAs linking to relevant YatraDham accommodation listings.")

    checkpoints.append({
        "id": "cp5_monetization_ctas",
        "name": "Monetization & YatraDham Stay CTAs",
        "weight": 10,
        "score": round(cp5_score, 1),
        "status": cp5_status,
        "detail": cp5_msg,
        "actual_value": f"{yatradham_links} YatraDham links, CTAs: {has_stay_cta}"
    })
    earned_score += cp5_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 6: First-Mile & Last-Mile Connecting Transit (Weight: 8 pts)
    # -------------------------------------------------------------------------
    # Mentions feeder buses (GSRTC, UTC, HRTC), local rickshaw/auto, station transfers
    connecting_transit_keywords = [
        "gsrtc", "state transport", "bus station", "bus service", "connecting bus",
        "railway station", "nearest airport", "auto rickshaw", "taxi fare", "feeder bus",
        "adajan", "bhavnagar bus", "station to terminal", "local commute"
    ]
    transit_matches = [k for k in connecting_transit_keywords if k in content_lower]

    if len(transit_matches) >= 3:
        cp6_score = 8.0
        cp6_status = "PASSED"
        cp6_msg = f"Complete first-mile/last-mile logistics covered ({', '.join(transit_matches[:3])})."
    elif len(transit_matches) >= 1:
        cp6_score = 4.0
        cp6_status = "PARTIAL"
        cp6_msg = f"Brief transit mentions ({', '.join(transit_matches)}). Include specific local feeder bus timings and station transfers."
        recommendations.append("Detail connecting public transit: state bus timings, nearest railhead, and local taxi/auto fares.")
    else:
        cp6_score = 0.0
        cp6_status = "FAILED"
        cp6_msg = "Missing connecting transit details. Travelers need to know how to reach the boarding point from the nearest railway or bus station."
        recommendations.append("Add a 'How to Reach & Connecting Bus Services' section with route numbers, timings, and ticket fares.")

    checkpoints.append({
        "id": "cp6_connecting_transit",
        "name": "First-Mile & Last-Mile Connecting Transit",
        "weight": 8,
        "score": round(cp6_score, 1),
        "status": cp6_status,
        "detail": cp6_msg,
        "actual_value": f"{len(transit_matches)} transit indicators"
    })
    earned_score += cp6_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 7: Hard Rules, Terms, Cancellation & Luggage Reality (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Specific cancellation tiers, weather disruption, check-in cutoff, pet rules
    policy_keywords = [
        "cancellation", "refund", "cutoff", "boarding time", "terms and conditions",
        "id proof", "luggage", "baggage", "pets", "weather", "gmb", "maritime board",
        "advance booking", "penalty"
    ]
    policy_matches = [k for k in policy_keywords if k in content_lower]
    has_refund_brackets = bool(re.search(r'\b(?:90%|80%|70%|60%|50%|no refund)\b', content_lower))

    if len(policy_matches) >= 4 or (len(policy_matches) >= 2 and has_refund_brackets):
        cp7_score = 10.0
        cp7_status = "PASSED"
        cp7_msg = "Rigorous operational policy guidelines: boarding cutoffs, refund percentages, and baggage/pet rules documented."
    elif len(policy_matches) >= 2:
        cp7_score = 5.0
        cp7_status = "PARTIAL"
        cp7_msg = "Basic rules present, but lacking concrete refund breakdown percentages and terminal reporting deadlines."
        recommendations.append("Provide a clear 'Cancellation, Refund & Baggage Policy' subsection with exact refund tiers and cutoff times.")
    else:
        cp7_score = 0.0
        cp7_status = "FAILED"
        cp7_msg = "No operational rules or refund policies found. Pilgrims require clear guidance on cancellations and boarding guidelines."
        recommendations.append("Include terms of journey: reporting time (e.g. 1 hr before), cancellation refund tiers, and allowed luggage.")

    checkpoints.append({
        "id": "cp7_operational_policies",
        "name": "Operational Rules, Refund & Luggage Policies",
        "weight": 10,
        "score": round(cp7_score, 1),
        "status": cp7_status,
        "detail": cp7_msg,
        "actual_value": f"{len(policy_matches)} policy terms, refund brackets: {has_refund_brackets}"
    })
    earned_score += cp7_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 8: Deep Comprehensive Topical Depth (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Ro-Pax blog is 4,800+ words. Champion standard requires >= 1,800 words
    h2_count = len(re.findall(r'(?:^|\n)##\s+[^\n]+', content)) + len(re.findall(r'<h2\b', content, re.IGNORECASE))

    if word_count >= 2000 and h2_count >= 7:
        cp8_score = 10.0
        cp8_status = "PASSED"
        cp8_msg = f"Elite encyclopedic depth: {word_count} words across {h2_count} comprehensive H2 subsections."
    elif word_count >= 1200 and h2_count >= 5:
        cp8_score = 7.0
        cp8_status = "PARTIAL"
        cp8_msg = f"Solid depth ({word_count} words, {h2_count} H2s), but champion rank-1 pillar guides expand to 2,000+ words."
        recommendations.append("Expand section breadth to 2,000+ words with additional historical context, local food recommendations, and traveler tips.")
    elif word_count >= 800:
        cp8_score = 4.0
        cp8_status = "PARTIAL"
        cp8_msg = f"Moderate word count ({word_count} words). May be outranked by longer, more comprehensive competitor guides."
        recommendations.append("Double the content depth by detailing step-by-step queues, vehicle protocols, and local sight guides.")
    else:
        cp8_score = 0.0
        cp8_status = "FAILED"
        cp8_msg = f"Content is too thin ({word_count} words). Superficial guides struggle to retain #1 rank."
        recommendations.append("Substantially expand the guide to at least 1,500 words to cover the full pilgrim journey.")

    checkpoints.append({
        "id": "cp8_topical_depth",
        "name": "Comprehensive Topical Depth",
        "weight": 10,
        "score": round(cp8_score, 1),
        "status": cp8_status,
        "detail": cp8_msg,
        "actual_value": f"{word_count} words, {h2_count} H2 sections"
    })
    earned_score += cp8_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 9: High-Intent Conversational FAQ Section (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Ro-Pax has 8 direct snippet-ready Q&As
    faq_question_matches = re.findall(r'(?:###\s*Q\d?:|<strong>Q\d?:|\bQuestion\s*\d?:|\bFAQ\b)', content, re.IGNORECASE)
    has_faqs = "frequently asked questions" in content_lower or "faqs" in content_lower or len(faq_question_matches) >= 3

    # Count individual questions
    q_count = len(re.findall(r'\b(?:what|when|how|where|is|can|do|does|are)\b[^\n?]+\?', content_lower))

    if has_faqs and q_count >= 5:
        cp9_score = 10.0
        cp9_status = "PASSED"
        cp9_msg = f"High-intent FAQ section confirmed with {q_count} direct conversational questions ready for Google AI Overviews and Featured Snippets."
    elif has_faqs and q_count >= 2:
        cp9_score = 6.0
        cp9_status = "PARTIAL"
        cp9_msg = f"FAQ section exists but has only {q_count} questions. Champion benchmark features 6 to 8 exhaustive Q&As."
        recommendations.append("Add 3-5 more conversational FAQs answering hyper-specific traveler doubts (e.g. ticket booking window, food onboard).")
    else:
        cp9_score = 0.0
        cp9_status = "FAILED"
        cp9_msg = "Missing dedicated FAQ section. Google heavily extracts Featured Snippets from concise, direct Q&A blocks."
        recommendations.append("Add an FAQ section with 6-8 direct questions answered in 2-3 clear sentences.")

    checkpoints.append({
        "id": "cp9_conversational_faqs",
        "name": "High-Intent Conversational FAQ Section",
        "weight": 10,
        "score": round(cp9_score, 1),
        "status": cp9_status,
        "detail": cp9_msg,
        "actual_value": f"{q_count} questions detected"
    })
    earned_score += cp9_score

    # -------------------------------------------------------------------------
    # CHECKPOINT 10: Anticipation of Real Traveler Edge Cases (E-E-A-T UGC) (Weight: 10 pts)
    # -------------------------------------------------------------------------
    # Ro-Pax comments cover: can passengers sit inside car? are pets allowed? tempo traveler? senior citizen?
    edge_case_keywords = [
        "sit inside", "in the car", "tempo traveller", "pets", "animals", "dog", "wheelchair",
        "senior citizen", "night parking", "overnight parking", "on-site booking", "counter booking",
        "advance booking", "ev charging", "electric car", "food allowed", "outside food",
        "child ticket", "children", "half ticket"
    ]
    matched_edge_cases = [k for k in edge_case_keywords if k in content_lower]

    if len(matched_edge_cases) >= 4:
        cp10_score = 10.0
        cp10_status = "PASSED"
        cp10_msg = f"Exceptional firsthand practical depth: {len(matched_edge_cases)} real traveler edge cases proactively resolved ({', '.join(matched_edge_cases[:4])})."
    elif len(matched_edge_cases) >= 2:
        cp10_score = 6.0
        cp10_status = "PARTIAL"
        cp10_msg = f"Covers {len(matched_edge_cases)} edge cases ({', '.join(matched_edge_cases)}). Add more practical user concerns (e.g. pets, parking, passenger seating in vehicle)."
        recommendations.append("Proactively answer common user comment doubts: parking charges, pet policy, food rules, and child tickets.")
    else:
        cp10_score = 1.0
        cp10_status = "FAILED"
        cp10_msg = "Lacks real-world traveler edge cases. The champion blog thrives because it answers 171+ specific reader scenarios."
        recommendations.append("Incorporate real-world edge-case advice: 'Can passengers stay inside vehicles during transit?', 'Are pets allowed?', 'Overnight parking at terminal?'.")

    checkpoints.append({
        "id": "cp10_edge_case_anticipation",
        "name": "Real Traveler Edge-Case Anticipation (E-E-A-T)",
        "weight": 10,
        "score": round(cp10_score, 1),
        "status": cp10_status,
        "detail": cp10_msg,
        "actual_value": f"{len(matched_edge_cases)} edge case topics covered"
    })
    earned_score += cp10_score

    # -------------------------------------------------------------------------
    # FINAL AGGREGATION & VERDICT
    # -------------------------------------------------------------------------
    final_score = round(min(100.0, max(0.0, earned_score)), 1)

    if final_score >= 88.0:
        verdict = "RANK_1_CHAMPION_READY"
        verdict_title = "🏆 Rank-1 Champion Ready"
        summary = "This blog incorporates the complete anatomical DNA of YatraDham's #1 Ro-Pax champion guide. High SERP immunity and AI Overview dominance."
    elif final_score >= 72.0:
        verdict = "HIGH_POTENTIAL_CONTENDER"
        verdict_title = "🥈 High Potential Contender"
        summary = "Strong structural foundation. Resolving the remaining partial checkpoints (tables, transit math, or edge cases) will propel it to #1."
    elif final_score >= 55.0:
        verdict = "AVERAGE_INFORMATIONAL_GUIDE"
        verdict_title = "🥉 Average Informational Guide"
        summary = "Meets baseline SEO standards but lacks the high-utility structured data tables, connecting logistics, and edge-case anticipation required to defend rank 1."
    else:
        verdict = "SUPERFICIAL_AT_RISK"
        verdict_title = "⚠️ Superficial / At-Risk Content"
        summary = "Content is missing critical utilitarian checkpoints (tables, exact tariffs, onward spokes, policies). Highly vulnerable to being displaced by high-gain competitors."

    passed_count = sum(1 for cp in checkpoints if cp["status"] == "PASSED")
    partial_count = sum(1 for cp in checkpoints if cp["status"] == "PARTIAL")
    failed_count = sum(1 for cp in checkpoints if cp["status"] == "FAILED")

    return {
        "champion_score": final_score,
        "verdict": verdict,
        "verdict_title": verdict_title,
        "summary": summary,
        "passed_checkpoints": passed_count,
        "partial_checkpoints": partial_count,
        "failed_checkpoints": failed_count,
        "total_checkpoints": len(checkpoints),
        "checkpoints": checkpoints,
        "recommendations": recommendations,
        "benchmark_comparison": {
            "target_blog": title or url or "Your Draft Blog",
            "champion_reference": ROPAX_CHAMPION_PROFILE["title"],
            "champion_url": ROPAX_CHAMPION_PROFILE["benchmark_url"],
            "metrics": {
                "word_count": {"current": word_count, "champion": ROPAX_CHAMPION_PROFILE["total_words"]},
                "tables_count": {"current": table_count, "champion": ROPAX_CHAMPION_PROFILE["tables_count"]},
                "internal_links": {"current": yatradham_links, "champion": ROPAX_CHAMPION_PROFILE["internal_links_count"]},
                "faqs_count": {"current": q_count, "champion": ROPAX_CHAMPION_PROFILE["faqs_count"]}
            }
        }
    }
