"""
AI SEO Audit & Autonomous Quality Gate Engine
=============================================
Implements:
1. https://github.com/marketplace/actions/ai-seo-audit (15-signal automated SEO audit gate)
2. https://github.com/topics/text-humanizer (0 AI-isms, 0 em-dashes, high burstiness, human rhythm)
3. https://github.com/topics/blog-writing (Answer-first, semantic H1-H3 hierarchy, tables, FAQs)
4. https://github.com/topics/ai-seo & topics/seo (Keyword prominence, density, meta boundaries, internal links)
5. https://github.com/topics/ai-visibility (GEO / Generative Engine Optimization for AI Overviews / SGE)
6. https://github.com/topics/agentic-seo & topics/ai-seo-agent (Information gain & entity gap analysis)
"""

import re
import math
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("ai_seo_audit")

# Banned spam/sales phrases
BANNED_SALES_PHRASES = [
    "best guaranteed", "cheapest in the world", "#1 travel agency", 
    "click here right now", "act now or miss out", "limited time only offer",
    "hurry up before slots run out"
]

# Required YatraDham internal link domains
YATRADHAM_LINK_DOMAINS = [
    "yatradham.org", "temple.yatradham.org", "travel.yatradham.org", "wellness.yatradham.org"
]


def extract_clean_prose(data: Any) -> str:
    """Extract readable prose from nested dicts, lists, or markdown strings, skipping structural tokens."""
    if isinstance(data, str):
        # Strip code blocks and markdown headings to get raw text
        cleaned = re.sub(r'```.*?```', '', data, flags=re.DOTALL)
        cleaned = re.sub(r'#+\s*', '', cleaned)
        return cleaned.strip()
    elif isinstance(data, dict):
        chunks = []
        for k, v in data.items():
            if k in ["time", "day_number", "url", "type", "image_url", "package_input", "id"]:
                continue
            res = extract_clean_prose(v)
            if res:
                chunks.append(res)
        return ". ".join(chunks)
    elif isinstance(data, list):
        chunks = [extract_clean_prose(item) for item in data]
        return ". ".join([c for c in chunks if c])
    return ""


def calculate_readability_metrics(text: str) -> Dict[str, Any]:
    """Calculate Flesch Reading Ease and Flesch-Kincaid Grade Level on natural prose."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip().split()) >= 2]
    
    if not words or not sentences:
        return {"reading_ease": 70, "grade_level": 7.5, "word_count": 0, "sentence_count": 0}

    word_count = len(words)
    sentence_count = len(sentences)
    
    syllable_count = 0
    for w in words:
        w_lower = w.lower()
        count = len(re.findall(r'[aeiouy]+', w_lower))
        if w_lower.endswith('e') and not w_lower.endswith('le') and len(w_lower) > 2:
            count = max(1, count - 1)
        syllable_count += max(1, count)

    asl = word_count / max(1, sentence_count)
    asw = syllable_count / max(1, word_count)
    
    reading_ease = 206.835 - (1.015 * asl) - (84.6 * asw)
    reading_ease = max(0, min(100, int(round(reading_ease))))
    
    grade_level = (0.39 * asl) + (11.8 * asw) - 15.59
    grade_level = max(1.0, min(18.0, round(grade_level, 1)))

    return {
        "reading_ease": reading_ease,
        "grade_level": grade_level,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": round(asl, 1),
    }


def calculate_burstiness_variance(text: str) -> Dict[str, Any]:
    """Calculate sentence length variance and standard deviation for human cadence."""
    clean = re.sub(r'#+\s+[^\n]+', '', text)
    sentences = [s.strip() for s in re.split(r'[.!?]+', clean) if len(s.strip().split()) >= 2]
    
    if len(sentences) < 2:
        return {"std_dev": 12.0, "sentence_lengths": [12], "is_monotonous": False}
        
    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    std_dev = round(math.sqrt(variance), 2)
    
    # std_dev >= 8.0 indicates rich human variation; < 3.5 indicates robotic LLM drone
    return {
        "std_dev": std_dev,
        "mean_length": round(mean, 1),
        "min_length": min(lengths),
        "max_length": max(lengths),
        "is_monotonous": std_dev < 4.0,
    }


def run_ai_seo_audit(
    title: str,
    meta_description: str,
    primary_keyword: str,
    content_body: Any,
    json_ld_schema: Optional[Dict[str, Any]] = None,
    destination: Optional[str] = None,
    pricing_str: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Executes the comprehensive 15-Point AI-SEO-Audit Gate.
    Returns:
      - score (0 - 100)
      - grade (A+, A, B, C, F)
      - checks (list of 15 individual audited checks)
      - humanizer_metrics (AI-isms, em-dashes, burstiness, reading ease)
      - geo_metrics (Answer-first, pricing presence, structured tables)
      - recommendations (actionable fixes)
    """
    from anti_ai_guardrails import detect_ai_isms, detect_55_patterns

    prose = extract_clean_prose(content_body)
    raw_markdown = content_body if isinstance(content_body, str) else extract_clean_prose(content_body)
    kw = (primary_keyword or "").strip().lower()
    t = (title or "").strip()
    m = (meta_description or "").strip()
    
    total_text = f"{t}. {m}. {prose}"
    words = re.findall(r'\b[a-zA-Z0-9\x27-]+\b', total_text)
    total_words = len(words)
    
    kw_words = [w for w in re.findall(r'\b[a-zA-Z0-9\x27-]+\b', kw) if len(w) > 3]
    kw_pattern = re.escape(kw) if kw else ""
    kw_matches = len(re.findall(kw_pattern, total_text, re.IGNORECASE)) if kw_pattern else 0
    if kw_matches == 0 and kw_words:
        kw_matches = len(re.findall(re.escape(kw_words[0]), total_text, re.IGNORECASE))
    
    keyword_density = round((kw_matches / max(1, total_words)) * 100, 2)
    
    # Readability and Burstiness
    readability = calculate_readability_metrics(prose)
    burstiness = calculate_burstiness_variance(prose)
    
    # Anti-AI and Humanizer signals
    detected_ai_isms = detect_ai_isms(total_text)
    clean_for_punct = re.sub(r'\|[^\n]+\|', ' ', total_text)
    clean_for_punct = re.sub(r'```[\s\S]*?```', ' ', clean_for_punct)
    em_dash_matches = re.findall(r'—|(?:--)', clean_for_punct)
    has_em_dashes = len(em_dash_matches) > 0
    patterns_report = detect_55_patterns(total_text)
    
    # AI-Visibility & GEO signals
    first_120_words = " ".join(words[:120]).lower()
    has_answer_first = any(h in first_120_words for h in ["is", "offers", "includes", "provides", "features", "starts from", "timings"])
    has_inr_pricing = bool(re.search(r'(?:₹|rs\.?|inr)\s*[\d,]+', total_text, re.IGNORECASE) or (pricing_str and re.search(r'\d+', pricing_str)))
    has_structured_tables_or_bullets = bool(
        "|" in raw_markdown or 
        (isinstance(content_body, dict) and (content_body.get("pricing_table") or content_body.get("itinerary")))
    )
    
    # Internal linking check
    has_internal_links = any(domain in total_text.lower() for domain in YATRADHAM_LINK_DOMAINS) or (
        isinstance(content_body, dict) and bool(content_body.get("smart_internal_links"))
    )

    checks = []
    deductions = 0
    recommendations = []

    # 1. Title Tag Length & Keyword Placement (50-60 chars optimal, max 65)
    t_len = len(t)
    kw_in_title = bool(kw and (kw in t.lower() or (kw_words and any(w in t.lower() for w in kw_words))))
    if 45 <= t_len <= 65 and kw_in_title:
        checks.append({
            "id": "title_optimization",
            "name": "Title Tag Length & Keyword Placement",
            "status": "PASSED",
            "value": f"{t_len} chars | Keyword present",
            "impact": 0,
        })
    elif 40 <= t_len <= 70:
        checks.append({
            "id": "title_optimization",
            "name": "Title Tag Length & Keyword Placement",
            "status": "WARNING",
            "value": f"{t_len} chars | {'Keyword present' if kw_in_title else 'Keyword missing'}",
            "impact": -5,
        })
        deductions += 5
        if not kw_in_title:
            recommendations.append("Include the primary keyword near the start of the title tag.")
        if t_len > 65:
            recommendations.append("Shorten title tag to under 65 characters to prevent Google SERP truncation.")
    else:
        checks.append({
            "id": "title_optimization",
            "name": "Title Tag Length & Keyword Placement",
            "status": "FAILED",
            "value": f"{t_len} chars (Needs adjustment)",
            "impact": -10,
        })
        deductions += 10
        recommendations.append("Adjust title tag length between 50-60 characters.")

    # 2. Meta Description Length & CTA (140-160 chars)
    m_len = len(m)
    kw_in_meta = bool(kw and (kw in m.lower() or (kw_words and any(w in m.lower() for w in kw_words))))
    has_cta = any(cta in m.lower() for cta in ["book", "reserve", "explore", "view", "discover", "plan", "contact"])
    if 130 <= m_len <= 165 and kw_in_meta and has_cta:
        checks.append({
            "id": "meta_optimization",
            "name": "Meta Description Length & CTA",
            "status": "PASSED",
            "value": f"{m_len} chars | Keyword & CTA verified",
            "impact": 0,
        })
    elif 115 <= m_len <= 175:
        checks.append({
            "id": "meta_optimization",
            "name": "Meta Description Length & CTA",
            "status": "WARNING",
            "value": f"{m_len} chars | {'CTA present' if has_cta else 'Missing CTA'}",
            "impact": -5,
        })
        deductions += 5
        if not has_cta:
            recommendations.append("Add a compelling call-to-action (e.g., 'Book your verified stay on YatraDham.Org') in meta description.")
    else:
        checks.append({
            "id": "meta_optimization",
            "name": "Meta Description Length & CTA",
            "status": "FAILED",
            "value": f"{m_len} chars (Out of bounds)",
            "impact": -10,
        })
        deductions += 10
        recommendations.append("Keep meta description strictly between 140-160 characters.")

    # 3. Keyword Prominence (Title, Meta, First 100 Words)
    in_first_100 = bool(kw and (kw in first_120_words or (kw_words and any(w in first_120_words for w in kw_words))))
    prominence_count = sum([kw_in_title, kw_in_meta, in_first_100])
    if prominence_count >= 2:
        checks.append({
            "id": "keyword_prominence",
            "name": "Keyword Prominence (Title, Meta, First 100 Words)",
            "status": "PASSED",
            "value": f"Appears in {prominence_count}/3 primary positions",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "keyword_prominence",
            "name": "Keyword Prominence (Title, Meta, First 100 Words)",
            "status": "WARNING",
            "value": f"Only found in {prominence_count}/3 positions",
            "impact": -6,
        })
        deductions += 6
        recommendations.append("Ensure target keyword is integrated in the opening paragraph (first 100 words).")

    # 4. Keyword Density (0.8% - 2.5% optimal)
    if 0.6 <= keyword_density <= 2.8:
        checks.append({
            "id": "keyword_density",
            "name": "Natural Keyword Density (0.8% - 2.5%)",
            "status": "PASSED",
            "value": f"{keyword_density}% (Natural human frequency)",
            "impact": 0,
        })
    elif keyword_density < 0.6:
        checks.append({
            "id": "keyword_density",
            "name": "Natural Keyword Density (0.8% - 2.5%)",
            "status": "WARNING",
            "value": f"{keyword_density}% (Under-optimized)",
            "impact": -4,
        })
        deductions += 4
        recommendations.append("Weave primary keyword and its natural variations 1-2 more times throughout body text.")
    else:
        checks.append({
            "id": "keyword_density",
            "name": "Natural Keyword Density (0.8% - 2.5%)",
            "status": "FAILED",
            "value": f"{keyword_density}% (Keyword stuffing risk)",
            "impact": -10,
        })
        deductions += 10
        recommendations.append("Reduce repetitive keyword occurrences to avoid search engine spam penalties.")

    # 5. Heading Hierarchy (H1, H2, H3 semantic structure)
    h1_count = len(re.findall(r'^#\s+[^\n]+', raw_markdown, re.MULTILINE))
    h2_count = len(re.findall(r'^##\s+[^\n]+', raw_markdown, re.MULTILINE))
    if isinstance(content_body, dict):
        # Structured package with section headings
        h2_count = len([k for k in content_body.keys() if "heading" in k or k in ["itinerary", "faq", "pricing_table"]])
        h1_count = 1
    
    if h1_count <= 2 and h2_count >= 2:
        checks.append({
            "id": "heading_hierarchy",
            "name": "Heading Hierarchy (Semantic H1 -> H2 -> H3)",
            "status": "PASSED",
            "value": f"{h2_count} structured sections verified",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "heading_hierarchy",
            "name": "Heading Hierarchy (Semantic H1 -> H2 -> H3)",
            "status": "WARNING",
            "value": f"{h2_count} headings detected",
            "impact": -5,
        })
        deductions += 5
        recommendations.append("Organize content into clear H2 and H3 subheadings with logical semantic nesting.")

    # 6. Readability & Natural Flow (Flesch Reading Ease >= 50)
    ease = readability["reading_ease"]
    if ease >= 55:
        checks.append({
            "id": "reading_ease",
            "name": "Flesch Reading Ease (Clarity & Flow)",
            "status": "PASSED",
            "value": f"{ease}/100 (Conversational & Engaging)",
            "impact": 0,
        })
    elif ease >= 40:
        checks.append({
            "id": "reading_ease",
            "name": "Flesch Reading Ease (Clarity & Flow)",
            "status": "WARNING",
            "value": f"{ease}/100 (Slightly dense)",
            "impact": -4,
        })
        deductions += 4
        recommendations.append("Simplify complex vocabulary to make instructions easier for pilgrims of all ages.")
    else:
        checks.append({
            "id": "reading_ease",
            "name": "Flesch Reading Ease (Clarity & Flow)",
            "status": "FAILED",
            "value": f"{ease}/100 (Difficult to read)",
            "impact": -8,
        })
        deductions += 8
        recommendations.append("Break down multi-clause sentences and use everyday English words.")

    # 7. Sentence Variety & Burstiness (std dev >= 6.5)
    std_dev = burstiness["std_dev"]
    if std_dev >= 6.5:
        checks.append({
            "id": "burstiness_variance",
            "name": "Sentence Length Variety (Human Burstiness)",
            "status": "PASSED",
            "value": f"Std Dev {std_dev} words (Natural pacing)",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "burstiness_variance",
            "name": "Sentence Length Variety (Human Burstiness)",
            "status": "WARNING",
            "value": f"Std Dev {std_dev} words (Monotonous rhythm)",
            "impact": -5,
        })
        deductions += 5
        recommendations.append("Mix short, punchy 3-6 word sentences with longer descriptive explanations.")

    # 8. Zero AI-isms & Robotic Clichés (Aboudjem & blader suite)
    ai_count = len(detected_ai_isms)
    if ai_count == 0:
        checks.append({
            "id": "anti_ai_isms",
            "name": "Zero AI-isms & Slop Vocabulary",
            "status": "PASSED",
            "value": "0 AI cliches detected",
            "impact": 0,
        })
    else:
        first_few = []
        for a in detected_ai_isms[:3]:
            if "phrase" in a:
                first_few.append(a["phrase"])
            elif a.get("examples"):
                first_few.append(str(a["examples"][0]))
            else:
                first_few.append(a.get("pattern", "AI phrase"))
        checks.append({
            "id": "anti_ai_isms",
            "name": "Zero AI-isms & Slop Vocabulary",
            "status": "WARNING",
            "value": f"{ai_count} AI phrases found ({', '.join(first_few)})",
            "impact": -min(15, ai_count * 4),
        })
        deductions += min(15, ai_count * 4)
        recommendations.append(f"Replace AI clichés ({', '.join(first_few)}) with plain human verbs.")

    # 9. Zero-Tolerance Em-Dash Ban
    if not has_em_dashes:
        checks.append({
            "id": "em_dash_ban",
            "name": "Zero-Tolerance Em-Dash Ban ('—')",
            "status": "PASSED",
            "value": "Clean human punctuation (0 em-dashes)",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "em_dash_ban",
            "name": "Zero-Tolerance Em-Dash Ban ('—')",
            "status": "WARNING",
            "value": f"{len(em_dash_matches)} em-dashes found",
            "impact": -5,
        })
        deductions += 5
        recommendations.append("Eliminate dramatic em-dashes ('—') and replace with standard commas or periods.")

    # 10. AI-Visibility & GEO Answer-First Quick Summary
    if has_answer_first:
        checks.append({
            "id": "geo_answer_first",
            "name": "GEO Answer-First AI Overview Ready",
            "status": "PASSED",
            "value": "Direct factual answer in opening snapshot",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "geo_answer_first",
            "name": "GEO Answer-First AI Overview Ready",
            "status": "WARNING",
            "value": "Missing direct summary statement in intro",
            "impact": -6,
        })
        deductions += 6
        recommendations.append("Add a 40-50 word direct Answer-First overview answering what the package includes.")

    # 11. Structured Comparative Data & Pricing in INR
    if has_inr_pricing and has_structured_tables_or_bullets:
        checks.append({
            "id": "structured_pricing_inr",
            "name": "Structured Pricing & Comparative Tables (INR ₹)",
            "status": "PASSED",
            "value": "Explicit INR pricing & tables verified",
            "impact": 0,
        })
    elif has_inr_pricing or has_structured_tables_or_bullets:
        checks.append({
            "id": "structured_pricing_inr",
            "name": "Structured Pricing & Comparative Tables (INR ₹)",
            "status": "WARNING",
            "value": "Partial pricing / table formatting",
            "impact": -4,
        })
        deductions += 4
        recommendations.append("Include explicit INR (₹) rates and structured comparison tables for AI citation.")
    else:
        checks.append({
            "id": "structured_pricing_inr",
            "name": "Structured Pricing & Comparative Tables (INR ₹)",
            "status": "FAILED",
            "value": "Missing structured pricing data",
            "impact": -8,
        })
        deductions += 8
        recommendations.append("Add verified pricing table with room/person breakdowns in INR.")

    # 12. Factual Grounding & Real Logistics
    has_transit = bool(re.search(r'\b(?:km|railway|airport|bus stand|station|distance)\b', total_text, re.IGNORECASE))
    has_timings = bool(re.search(r'\b\d{1,2}(?::\d{2})?\s*(?:am|pm|hrs)\b', total_text, re.IGNORECASE))
    if has_transit and has_timings:
        checks.append({
            "id": "factual_logistics",
            "name": "Firsthand Ground Truth & Logistics (Timings/Transit)",
            "status": "PASSED",
            "value": "Exact darshan hours, transit distances & logistics present",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "factual_logistics",
            "name": "Firsthand Ground Truth & Logistics (Timings/Transit)",
            "status": "WARNING",
            "value": "Limited transit distances or specific ritual timings",
            "impact": -4,
        })
        deductions += 4
        recommendations.append("Add nearest railway station/airport distances in kilometers and morning/evening aarti timings.")

    # 13. Smart Internal Linking Network
    if has_internal_links:
        checks.append({
            "id": "internal_linking",
            "name": "Verified YatraDham Ecosystem Links",
            "status": "PASSED",
            "value": "Contextual links to stays/pujas/tours present",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "internal_linking",
            "name": "Verified YatraDham Ecosystem Links",
            "status": "WARNING",
            "value": "No internal links to YatraDham portals found",
            "impact": -5,
        })
        deductions += 5
        recommendations.append("Incorporate natural internal links to YatraDham dharamshalas, puja sevas, or tour packages.")

    # 14. Stacked JSON-LD Schema.org Validity
    has_valid_schema = bool(json_ld_schema and (json_ld_schema.get("@graph") or json_ld_schema.get("@type")))
    if has_valid_schema:
        checks.append({
            "id": "schema_json_ld",
            "name": "Stacked Multi-Entity Schema.org Markup",
            "status": "PASSED",
            "value": "Valid JSON-LD schema (FAQPage / Service / Article)",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "schema_json_ld",
            "name": "Stacked Multi-Entity Schema.org Markup",
            "status": "WARNING",
            "value": "Schema markup not attached or incomplete",
            "impact": -6,
        })
        deductions += 6
        recommendations.append("Attach rich JSON-LD structured data for rich snippet eligibility.")

    # 15. Content Depth & Word Count Thresholds
    min_expected_words = 120 if (isinstance(content_body, dict) or total_words < 400) else 650
    if total_words >= min_expected_words:
        checks.append({
            "id": "content_depth",
            "name": "Content Depth & Comprehensive Coverage",
            "status": "PASSED",
            "value": f"{total_words} total words (Substantive depth)",
            "impact": 0,
        })
    else:
        checks.append({
            "id": "content_depth",
            "name": "Content Depth & Comprehensive Coverage",
            "status": "WARNING",
            "value": f"{total_words} words (Below target of {min_expected_words})",
            "impact": -8,
        })
        deductions += 8
        recommendations.append(f"Expand content depth to meet the minimum target of {min_expected_words} words.")

    # Final Composite Score Calculation
    final_score = max(20, min(100, 100 - deductions))
    
    if final_score >= 93:
        grade = "A+"
    elif final_score >= 85:
        grade = "A"
    elif final_score >= 75:
        grade = "B"
    elif final_score >= 60:
        grade = "C"
    else:
        grade = "F"

    # Human score calculation (Copyleaks proxy)
    human_score = max(50, min(100, int(100 - (ai_count * 10) - (5 if has_em_dashes else 0) + (5 if std_dev >= 8.0 else 0))))

    status = "EXCELLENT" if final_score >= 88 else ("GOOD" if final_score >= 75 else ("NEEDS_IMPROVEMENT" if final_score >= 60 else "POOR"))
    
    from ai_visibility import calculate_ai_visibility_metrics
    ai_vis_report = calculate_ai_visibility_metrics(
        query_or_topic=kw or title or "Pilgrimage Yatra",
        content=total_text,
        target_domain="yatradham.org",
        pricing_str=pricing_str
    )
    
    geo_visibility = {
        "geo_ready": has_answer_first,
        "has_inr_pricing": has_inr_pricing,
        "has_answer_first": has_answer_first,
        "has_structured_tables": has_structured_tables_or_bullets,
        "ai_visibility_index": ai_vis_report["ai_visibility_index"],
        "platform_scores": ai_vis_report["platform_scores"],
        "citation_share": ai_vis_report["citation_share"],
        "actionable_directives": ai_vis_report["actionable_directives"]
    }

    return {
        "score": final_score,
        "grade": grade,
        "audit_grade": grade,
        "status": status,
        "human_score": human_score,
        "passed_checks_count": sum(1 for c in checks if c["status"] == "PASSED"),
        "total_checks": len(checks),
        "checks": checks,
        "recommendations": recommendations,
        "geo_visibility": geo_visibility,
        "ai_visibility": ai_vis_report,
        "metrics": {
            "word_count": total_words,
            "keyword_density": keyword_density,
            "reading_ease": readability["reading_ease"],
            "grade_level": readability["grade_level"],
            "burstiness_std_dev": burstiness["std_dev"],
            "ai_isms_count": ai_count,
            "em_dash_count": len(em_dash_matches),
            "geo_ready": has_answer_first,
            "inr_pricing_present": has_inr_pricing,
            "schema_present": has_valid_schema,
        }
    }


def auto_heal_content(
    title: Any = "",
    meta_description: str = "",
    primary_keyword: str = "",
    content_body: Any = None,
    voice: str = "professional"
) -> Any:
    """
    Autonomous Agentic SEO Self-Healing Loop:
    Runs the 15-point audit, automatically repairs AI-isms, em-dashes, title/meta lengths,
    and returns sanitized, fully-compliant content.
    If called with a single string, returns healed string.
    If called with title, meta, keyword, content, returns (clean_title, clean_meta, clean_content, audit).
    """
    from anti_ai_guardrails import de_slop_and_humanize, eradicate_em_dashes

    # Single string / standalone content call
    if content_body is None and not meta_description and not primary_keyword:
        if isinstance(title, str):
            clean = eradicate_em_dashes(title)
            return de_slop_and_humanize(clean, voice=voice)
        return title

    clean_content_body = content_body if content_body is not None else ""

    # 1. Clean em-dashes and slop from Title
    clean_title = eradicate_em_dashes(str(title)).strip()
    clean_title = de_slop_and_humanize(clean_title, voice=voice)
    if len(clean_title) > 65:
        clean_title = clean_title[:62].rsplit(" ", 1)[0] + "..." if " " in clean_title[:62] else clean_title[:65]

    # 2. Clean and format Meta Description
    clean_meta = eradicate_em_dashes(meta_description).strip()
    clean_meta = de_slop_and_humanize(clean_meta, voice=voice)
    if not clean_meta:
        clean_meta = f"Book verified {primary_keyword} with authentic services and 24/7 pilgrim support on YatraDham.Org. Reserve now!"
    if len(clean_meta) > 160:
        clean_meta = clean_meta[:157].rsplit(" ", 1)[0] + "..." if " " in clean_meta[:157] else clean_meta[:160]

    # 3. Recursively de-slop and humanize content_body
    def _clean_node(node):
        if isinstance(node, str):
            return de_slop_and_humanize(node, voice=voice)
        elif isinstance(node, list):
            return [_clean_node(item) for item in node]
        elif isinstance(node, dict):
            return {k: _clean_node(v) for k, v in node.items()}
        return node

    clean_content = _clean_node(clean_content_body)

    # 4. Run AI SEO Audit on the healed content
    audit = run_ai_seo_audit(clean_title, clean_meta, primary_keyword, clean_content)
    
    return clean_title, clean_meta, clean_content, audit
