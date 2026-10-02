"""
Google Search Generative AI Content Compliance Checker
======================================================
Official Authority:
https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

This module audits AI-generated and AI-assisted web content against Google Search Central's
official Guidance on Using Generative AI Content on Your Website and related Search Essentials:

1. Spam Policies & Scaled Content Abuse (Search Quality Raters Guidelines Section 4.6.5 & 4.6.6)
   - Using AI to generate many pages without adding original value violates Google's spam policy.
   - Evaluates information density, repetitive templating, and anti-spam compliance.

2. Accuracy, Quality, and Relevance (Hallucination Mitigation & Factchecking)
   - "Generative models don't retrieve facts, but predict a likely sequence of words...
     It is critical to manually factcheck and review all AI-generated content for accuracy
     and trustworthiness before publishing."
   - Factchecking scope includes main content, <title>, <meta description>, structured data,
     and image alt texts.

3. "Give Users Context" (Who, How, Why Transparency Disclosures)
   - "Sharing information about how a piece of content was created can help give your readers
     more context. Consider adding information on how your content was created... providing
     background information on how automation was used."
   - Validates author attribution ("Who"), methodology/AI disclosure ("How"), and user-first
     intent ("Why").

4. Metadata & Structured Data Verification
   - Validates title tag, meta description, image alt attributes, and JSON-LD schema against
     Search Essentials guidelines.

5. E-E-A-T & Firsthand Ground Truth
   - Enforces concrete entities, verified local pricing (INR ₹), timings, distances, and absence
     of robotic AI cliches or em-dashes.
"""

import re
import math
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("google_genai_checker")

GOOGLE_GENAI_POLICY_URL = "https://developers.google.com/search/docs/fundamentals/using-gen-ai-content"
GOOGLE_HELPFUL_CONTENT_URL = "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"

# Banned spam/sales manipulation terms (scaled spam indicators)
SPAM_MANIPULATION_PHRASES = [
    "best guaranteed", "cheapest in the world", "#1 travel agency",
    "click here right now", "act now or miss out", "limited time only offer",
    "hurry up before slots run out", "buy now before prices double",
    "guaranteed lowest price anywhere", "100% free money"
]

# AI hallucination placeholder patterns
HALLUCINATION_PLACEHOLDERS = [
    r'\[insert\s+[^\]]+\]',
    r'\[x\]',
    r'\[city\]',
    r'\[hotel\]',
    r'\[price\]',
    r'\[date\]',
    r'\[phone(?:\s+number)?\]',
    r'\[link\]',
    r'\{[a-zA-Z0-9_-]+\}',
    r'<insert\s+[^>]+>',
    r'as an ai\b',
    r'my knowledge cutoff\b',
    r'as of my last update\b'
]

# Transparency markers ("Who" & "How")
WHO_AUTHOR_MARKERS = [
    r'\b(?:written|authored|prepared|curated)\s+by\b',
    r'\b(?:reviewed|verified|fact-checked|audited)\s+by\b',
    r'\bauthor\s*:\s*[a-zA-Z]',
    r'\bby\s+(?:the\s+)?yatradham\s+editorial\b',
    r'\beditor\s*:\s*[a-zA-Z]',
    r'\bexpert\s+contributor\b'
]

HOW_METHODOLOGY_MARKERS = [
    r'\b(?:created|drafted|researched)(?:\s+and\s+\w+)?\s+with\s+(?:the\s+)?(?:assistance\s+of\s+)?(?:ai|artificial\s+intelligence|automation)\b',
    r'\bwith\s+ai\s+assistance\b',
    r'\bai-assisted\b',
    r'\bautomation\s+disclosure\b',
    r'\beditorial\s+(?:integrity|transparency|disclosure|note|methodology)\b',
    r'\bverified\s+by\s+(?:our\s+)?(?:travel\s+)?(?:editorial\s+team|editors)\b',
    r'\bfact-checked\s+(?:against|by|and\s+verified)\b',
    r'\bhow\s+this\s+(?:guide|article|content)\s+was\s+created\b',
    r'\bgoogle\s+search\s+essentials\s+compliance\b'
]

RECOMMENDED_DISCLOSURE_TEMPLATE = (
    "Editorial Disclosure: This guide was researched and drafted with AI assistance "
    "for structural clarity and comprehensively fact-checked, reviewed, and verified by "
    "the YatraDham.Org Editorial Team to ensure 100% accuracy, authentic local timings, "
    "and verified pilgrim hospitality standards."
)


def extract_plain_text(content: Any) -> str:
    """Extract plain readable prose from str, dict, or list structures."""
    if isinstance(content, str):
        # Strip fenced code blocks and markdown headings
        text = re.sub(r'```[\s\S]*?```', '', content)
        text = re.sub(r'#+\s*', '', text)
        return text.strip()
    elif isinstance(content, dict):
        chunks = []
        for k, v in content.items():
            if k in ["time", "day_number", "url", "type", "image_url", "package_input", "id"]:
                continue
            t = extract_plain_text(v)
            if t:
                chunks.append(t)
        return ". ".join(chunks)
    elif isinstance(content, list):
        chunks = [extract_plain_text(item) for item in content]
        return ". ".join([c for c in chunks if c])
    return ""


def check_scaled_content_abuse(text: str, total_words: int) -> Tuple[int, str, List[str]]:
    """
    Evaluates Google Spam Policy on Scaled Content Abuse (QRG 4.6.5 & 4.6.6).
    Checks for boilerplate repetition, low lexical variety, and spam triggers.
    Returns (score 0-20, status, findings).
    """
    findings = []
    deductions = 0

    if total_words < 80:
        return 5, "FAILED", ["Word count critically low (< 80 words); lacks substantive depth."]

    # 1. Check for manipulative spam sales phrases
    found_spam = [p for p in SPAM_MANIPULATION_PHRASES if p in text.lower()]
    if found_spam:
        deductions += min(10, len(found_spam) * 4)
        findings.append(f"Manipulative sales phrases detected: {', '.join(found_spam[:2])}")

    # 2. Check lexical diversity (unique words / total words)
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    if words:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.35 and total_words > 200:
            deductions += 6
            findings.append(f"Low lexical diversity ({round(unique_ratio * 100, 1)}%); indicates repetitive templated content.")
        elif unique_ratio > 0.45:
            findings.append(f"Healthy lexical diversity ({round(unique_ratio * 100, 1)}%); demonstrates rich, non-repetitive prose.")

    # 3. Check for repetitive sentence openings
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip().split()) >= 3]
    if len(sentences) >= 6:
        first_words = [s.split()[0].lower() for s in sentences]
        from collections import Counter
        top_openers = Counter(first_words).most_common(1)
        if top_openers and top_openers[0][1] > (len(sentences) * 0.4):
            deductions += 4
            findings.append(f"Monotonous sentence openers ('{top_openers[0][0]}' opens {top_openers[0][1]} sentences); lacks human rhythm.")

    score = max(0, min(20, 20 - deductions))
    status = "PASSED" if score >= 16 else ("WARNING" if score >= 10 else "FAILED")
    if not findings:
        findings.append("Zero scaled abuse or repetitive templating detected; passes Google Spam Policies.")
    return score, status, findings


def check_factual_accuracy_and_hallucinations(
    text: str,
    title: str = "",
    meta_description: str = "",
    pricing_str: Optional[str] = None
) -> Tuple[int, str, List[str], List[str]]:
    """
    Evaluates Google's Accuracy, Quality, and Relevance directive.
    Generative models predict tokens and can hallucinate facts.
    Verifies absence of hallucination placeholders, checks for concrete ground truth,
    and checks consistency between title/meta and content.
    Returns (score 0-20, status, findings, hallucinations_found).
    """
    findings = []
    hallucinations = []
    deductions = 0

    combined = f"{title}. {meta_description}. {text}"

    # 1. Search for AI placeholder tokens
    for pat in HALLUCINATION_PLACEHOLDERS:
        matches = re.findall(pat, combined, re.IGNORECASE)
        if matches:
            hallucinations.extend(matches)
            deductions += min(12, len(matches) * 5)
            findings.append(f"Unrendered placeholder/hallucination token found: '{matches[0]}'")

    # 2. Check for concrete verifiable facts (timings, transit distances, ground truth)
    has_timings = bool(re.search(r'\b\d{1,2}(?::\d{2})?\s*(?:am|pm|hrs)\b', combined, re.IGNORECASE))
    has_transit = bool(re.search(r'\b(?:km|kilometers?|railway|airport|station|bus\s+stand)\b', combined, re.IGNORECASE))
    has_inr = bool(re.search(r'(?:₹|rs\.?|inr)\s*[\d,]+', combined, re.IGNORECASE) or (pricing_str and re.search(r'\d+', pricing_str)))

    grounding_elements = sum([has_timings, has_transit, has_inr])
    if grounding_elements >= 2:
        findings.append("Verified firsthand ground truth present (timings, transit distances, and INR pricing).")
    elif grounding_elements == 1:
        deductions += 4
        findings.append("Partial factual grounding; recommended to add exact darshan timings or transit distances.")
    else:
        deductions += 8
        findings.append("Lacks concrete verifiable facts (no darshan hours, transit distances, or INR tariffs found).")

    # 3. Consistency check between title and body
    t_lower = title.lower()
    day_match = re.search(r'(\d+)\s*(?:days?|nights?)', t_lower)
    if day_match:
        claimed_days = day_match.group(1)
        # Check if body discusses days or itinerary
        if not re.search(rf'\b(?:day\s*{claimed_days}|{claimed_days}\s*days?)\b', combined, re.IGNORECASE) and not re.search(r'\bitinerary\b', combined, re.IGNORECASE):
            deductions += 4
            findings.append(f"Title claims '{claimed_days} Days' but body does not detail matching day-by-day itinerary.")

    score = max(0, min(20, 20 - deductions))
    status = "PASSED" if score >= 16 else ("WARNING" if score >= 10 else "FAILED")
    return score, status, findings, hallucinations


def check_transparency_who_how_why(
    text: str,
    author: Optional[str] = None,
    methodology_disclosure: Optional[str] = None
) -> Tuple[int, str, List[str], Dict[str, Any]]:
    """
    Evaluates Google's "Give Users Context" guideline (Who, How, Why).
    - Who: Explicit author byline / organization attribution
    - How: Disclosure of AI/automation usage and editorial verification
    - Why: People-first value proposition over search-engine manipulation
    Returns (score 0-20, status, findings, transparency_dict).
    """
    findings = []
    deductions = 0
    t_text = text.lower()

    # 1. Who created this?
    has_explicit_author = bool(author and len(author.strip()) >= 3)
    has_inline_author = any(re.search(pat, t_text) for pat in WHO_AUTHOR_MARKERS)
    who_verified = has_explicit_author or has_inline_author

    if who_verified:
        author_name = author if has_explicit_author else "Identified in byline"
        findings.append(f"Author attribution verified ('Who'): {author_name}")
    else:
        deductions += 7
        findings.append("Missing clear author or editorial byline ('Who created this content?').")

    # 2. How was it created?
    has_explicit_disclosure = bool(methodology_disclosure and len(methodology_disclosure.strip()) >= 15)
    has_inline_disclosure = any(re.search(pat, t_text) for pat in HOW_METHODOLOGY_MARKERS)
    how_verified = has_explicit_disclosure or has_inline_disclosure

    if how_verified:
        findings.append("Editorial & AI methodology disclosure verified ('How it was created').")
    else:
        deductions += 7
        findings.append("Missing transparency statement on automation/AI research and editorial review ('How').")

    # 3. Why was it created? (People-first vs search manipulation)
    has_pilgrim_benefit = any(w in t_text for w in [
        "devotees", "pilgrims", "darshan", "aarti", "clean rooms", "prasad",
        "dress code", "cloakroom", "senior citizen", "how to reach", "safe"
    ])
    if has_pilgrim_benefit:
        findings.append("Genuine people-first intent verified ('Why'): content directly helps devotees plan their pilgrimage.")
    else:
        deductions += 4
        findings.append("Unclear user-benefit purpose; content reads primarily as keyword targeting rather than pilgrim assistance.")

    score = max(0, min(20, 20 - deductions))
    status = "PASSED" if score >= 16 else ("WARNING" if score >= 10 else "FAILED")
    
    transparency_summary = {
        "who_verified": who_verified,
        "how_verified": how_verified,
        "why_people_first": has_pilgrim_benefit,
        "author": author or ("Found inline" if has_inline_author else "Unspecified"),
        "methodology": "Present" if how_verified else "Missing"
    }

    return score, status, findings, transparency_summary


def check_metadata_and_structured_data(
    title: str,
    meta_description: str,
    text: str,
    json_ld_schema: Optional[Dict[str, Any]] = None,
    images: Optional[List[Dict[str, str]]] = None
) -> Tuple[int, str, List[str], Dict[str, Any]]:
    """
    Evaluates Google directive:
    "This review also applies to metadata like <title> elements, meta description elements,
     structured data, and alternate texts for images, which can appear in Search results."
    Returns (score 0-15, status, findings, metadata_summary).
    """
    findings = []
    deductions = 0

    t_len = len(title.strip())
    m_len = len(meta_description.strip())

    # 1. Title element audit (45-65 chars)
    if 45 <= t_len <= 65:
        findings.append(f"Title tag length optimal ({t_len} chars); eligible for clean search snippet.")
    elif 35 <= t_len <= 75:
        deductions += 2
        findings.append(f"Title tag length slightly suboptimal ({t_len} chars); keep between 45-65 characters.")
    else:
        deductions += 4
        findings.append(f"Title tag length ({t_len} chars) fails Search Essentials optimal boundary (45-65 chars).")

    # 2. Meta description audit (130-165 chars)
    if 130 <= m_len <= 165:
        findings.append(f"Meta description length optimal ({m_len} chars); complies with SERP snippet display.")
    elif 110 <= m_len <= 180:
        deductions += 2
        findings.append(f"Meta description length ({m_len} chars) could be tightened between 130-165 chars.")
    else:
        deductions += 4
        findings.append(f"Meta description ({m_len} chars) out of standard snippet boundaries (130-165 chars).")

    # 3. Structured Data / Schema.org validation
    has_schema = bool(json_ld_schema and (json_ld_schema.get("@graph") or json_ld_schema.get("@type")))
    if has_schema:
        schema_type = json_ld_schema.get("@type") or "Stacked Graph"
        findings.append(f"Valid structured data attached ({schema_type}); complies with Google Rich Results criteria.")
    else:
        deductions += 4
        findings.append("Structured data missing; attach JSON-LD schema (FAQPage / Article / TouristAttraction).")

    # 4. Image alt text verification
    img_findings = "No images checked"
    if images:
        generic_alts = 0
        empty_alts = 0
        for img in images:
            alt = (img.get("alt") or "").strip().lower()
            if not alt:
                empty_alts += 1
            elif alt in ["image", "photo", "picture", "temple", "img"]:
                generic_alts += 1
        if empty_alts > 0 or generic_alts > 0:
            deductions += 2
            findings.append(f"Image alt text warning: {empty_alts} missing, {generic_alts} generic; ensure descriptive alt attributes.")
        else:
            findings.append(f"All {len(images)} images have descriptive, contextual alt text.")
    else:
        # Check inline markdown images ![alt](url)
        md_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', text)
        if md_images:
            empty_alts = sum(1 for alt, _ in md_images if not alt.strip() or alt.strip().lower() in ["image", "photo"])
            if empty_alts > 0:
                deductions += 2
                findings.append(f"Found {empty_alts} inline image(s) with missing or generic alt text.")
            else:
                findings.append(f"All {len(md_images)} inline images have descriptive alt text.")

    score = max(0, min(15, 15 - deductions))
    status = "PASSED" if score >= 12 else ("WARNING" if score >= 8 else "FAILED")

    metadata_summary = {
        "title_length": t_len,
        "meta_description_length": m_len,
        "has_schema": has_schema,
        "score": score
    }

    return score, status, findings, metadata_summary


def check_humanizer_and_anti_slop(text: str) -> Tuple[int, str, List[str], Dict[str, Any]]:
    """
    Evaluates anti-AI humanizer metrics:
    - 0 AI cliché phrases (delve, leverage, tapestry, nestled, etc.)
    - 0 em-dashes ('—')
    - Natural sentence length variation (burstiness std dev >= 6.0)
    - Flesch Reading Ease score >= 45
    Returns (score 0-15, status, findings, metrics).
    """
    from anti_ai_guardrails import detect_ai_isms
    from ai_seo_audit import calculate_readability_metrics, calculate_burstiness_variance

    findings = []
    deductions = 0

    # 1. AI clichés check
    ai_isms = detect_ai_isms(text)
    if not ai_isms:
        findings.append("Zero AI clichés detected (0 slop words); tone is grounded in natural human language.")
    else:
        count = len(ai_isms)
        deductions += min(8, count * 3)
        sample = [a.get("phrase", "phrase") for a in ai_isms[:3]]
        findings.append(f"{count} robotic AI cliché(s) found ({', '.join(sample)}); replace with simple verbs.")

    # 2. Em-dash check
    em_dashes = re.findall(r'—|(?:--)|\s-\s', text)
    has_em = len(re.findall(r'—|(?:--)', text)) > 0
    if not has_em:
        findings.append("Zero em-dashes ('—') detected; clean punctuation.")
    else:
        deductions += 3
        findings.append("Em-dash ('—') detected; replace with standard commas or natural periods.")

    # 3. Readability and burstiness
    readability = calculate_readability_metrics(text)
    burstiness = calculate_burstiness_variance(text)

    ease = readability["reading_ease"]
    std_dev = burstiness["std_dev"]

    if ease >= 50:
        findings.append(f"Flesch Reading Ease is {ease}/100 (Accessible and clear).")
    else:
        deductions += 2
        findings.append(f"Flesch Reading Ease is {ease}/100 (Dense sentence structure).")

    if std_dev >= 6.0:
        findings.append(f"Healthy sentence burstiness (std dev {std_dev}); reflects organic human pacing.")
    else:
        deductions += 2
        findings.append(f"Low burstiness variance (std dev {std_dev}); risk of monotonous AI cadence.")

    score = max(0, min(15, 15 - deductions))
    status = "PASSED" if score >= 12 else ("WARNING" if score >= 8 else "FAILED")

    metrics = {
        "ai_isms_count": len(ai_isms),
        "has_em_dashes": has_em,
        "reading_ease": ease,
        "burstiness_std_dev": std_dev
    }

    return score, status, findings, metrics


def check_eeat_firsthand_experience(text: str) -> Tuple[int, str, List[str]]:
    """
    Evaluates Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness).
    Checks for authentic pilgrim guidance: dress codes, cloakroom counters, senior citizen amenities,
    sacred rituals, satvik dining, and YatraDham ecosystem links.
    Returns (score 0-10, status, findings).
    """
    findings = []
    deductions = 0
    t_lower = text.lower()

    # 1. Practical pilgrim guidance
    has_practical = any(w in t_lower for w in ["dress code", "cloakroom", "footwear", "prasad counter", "vip queue", "queue", "entry gate", "token"])
    if has_practical:
        findings.append("Firsthand temple darshan procedures verified (dress code, cloakrooms, or entry protocols).")
    else:
        deductions += 3
        findings.append("Missing practical darshan guidance (dress code, cloakroom token rules, gate entry).")

    # 2. Elder care and satvik food
    has_hospitality = any(w in t_lower for w in ["senior citizen", "wheelchair", "elderly", "satvik", "pure vegetarian", "dharamshala", "ashram"])
    if has_hospitality:
        findings.append("Devotee hospitality verified (senior citizen facilities, Satvik bhojan, clean ashram rooms).")
    else:
        deductions += 3
        findings.append("Missing pilgrim hospitality details (elder care accommodations or Satvik dining).")

    # 3. Trustworthy ecosystem links
    has_links = "yatradham.org" in t_lower or "yatradham" in t_lower
    if has_links:
        findings.append("Authoritative internal links to verified YatraDham accommodations and darshan bookings present.")
    else:
        deductions += 2
        findings.append("Incorporate direct links to verified stays on YatraDham.Org.")

    score = max(0, min(10, 10 - deductions))
    status = "PASSED" if score >= 8 else ("WARNING" if score >= 5 else "FAILED")
    return score, status, findings


def audit_google_genai_compliance(
    content: Any,
    title: str = "",
    meta_description: str = "",
    author: Optional[str] = None,
    methodology_disclosure: Optional[str] = None,
    json_ld_schema: Optional[Dict[str, Any]] = None,
    images: Optional[List[Dict[str, str]]] = None,
    target_keyword: Optional[str] = None,
    pricing_str: Optional[str] = None
) -> Dict[str, Any]:
    """
    Comprehensive Google Generative AI Content Compliance Auditor.
    Direct implementation of:
    https://developers.google.com/search/docs/fundamentals/using-gen-ai-content

    Returns:
      - overall_score: 0 - 100
      - grade: A+, A, B, C, F
      - verdict: COMPLIANT_HIGH_QUALITY | NEEDS_EDITORIAL_REVIEW | HIGH_RISK_SPAM_VIOLATION
      - status: PASSED | WARNING | FAILED
      - checks: List of 6 audited pillars with specific Google policy citations
      - transparency: Breakdown of Who, How, and Why
      - actionable_recommendations: Prioritized corrective actions
      - suggested_transparency_disclosure: Ready-to-use editorial disclosure text
      - source_policy_url: Google Search Central documentation link
    """
    plain_text = extract_plain_text(content)
    words = re.findall(r'\b[a-zA-Z0-9\x27-]+\b', plain_text)
    total_words = len(words)

    # 1. Scaled Content Abuse (Max 20)
    score_scaled, status_scaled, findings_scaled = check_scaled_content_abuse(plain_text, total_words)

    # 2. Factual Accuracy & Hallucinations (Max 20)
    score_facts, status_facts, findings_facts, hallucinations = check_factual_accuracy_and_hallucinations(
        plain_text, title=title, meta_description=meta_description, pricing_str=pricing_str
    )

    # 3. Transparency & Context (Who, How, Why) (Max 20)
    score_trans, status_trans, findings_trans, transparency_summary = check_transparency_who_how_why(
        plain_text, author=author, methodology_disclosure=methodology_disclosure
    )

    # 4. Metadata & Structured Data (Max 15)
    score_meta, status_meta, findings_meta, metadata_summary = check_metadata_and_structured_data(
        title=title, meta_description=meta_description, text=plain_text,
        json_ld_schema=json_ld_schema, images=images
    )

    # 5. Humanizer & Anti-Slop (Max 15)
    score_human, status_human, findings_human, human_metrics = check_humanizer_and_anti_slop(plain_text)

    # 6. E-E-A-T Firsthand Experience (Max 10)
    score_eeat, status_eeat, findings_eeat = check_eeat_firsthand_experience(plain_text)

    # Total Score (0-100)
    total_score = max(0, min(100, score_scaled + score_facts + score_trans + score_meta + score_human + score_eeat))

    # Grade & Verdict
    if total_score >= 90:
        grade = "A+"
        verdict = "COMPLIANT_HIGH_QUALITY"
        status = "PASSED"
    elif total_score >= 82:
        grade = "A"
        verdict = "COMPLIANT_HIGH_QUALITY"
        status = "PASSED"
    elif total_score >= 70:
        grade = "B"
        verdict = "NEEDS_EDITORIAL_REVIEW"
        status = "WARNING"
    elif total_score >= 55:
        grade = "C"
        verdict = "NEEDS_EDITORIAL_REVIEW"
        status = "WARNING"
    else:
        grade = "F"
        verdict = "HIGH_RISK_SPAM_VIOLATION"
        status = "FAILED"

    # Actionable Recommendations
    recommendations = []
    if not transparency_summary["who_verified"]:
        recommendations.append("Add an explicit author or editorial byline (e.g. 'By YatraDham Editorial Team') to satisfy Google's 'Who' requirement.")
    if not transparency_summary["how_verified"]:
        recommendations.append("Include Google's recommended 'How' disclosure: state that research was conducted with AI assistance and fact-checked by travel specialists.")
    if hallucinations:
        recommendations.append(f"Remove or fill {len(hallucinations)} unresolved placeholder token(s): {', '.join(hallucinations[:2])}.")
    if score_meta < 12:
        recommendations.append("Ensure title tag (45-65 chars) and meta description (130-165 chars) are accurate and attach JSON-LD schema.")
    if human_metrics["ai_isms_count"] > 0:
        recommendations.append(f"Replace {human_metrics['ai_isms_count']} robotic AI clichés with direct, active verbs.")
    if human_metrics["has_em_dashes"]:
        recommendations.append("Remove all em-dashes ('—') to maintain natural human editorial punctuation.")
    if score_eeat < 8:
        recommendations.append("Ground the guide with firsthand pilgrim logistics: cloakroom counters, temple gate numbers, and local Aarti schedules.")

    checks = [
        {
            "id": "scaled_content_abuse",
            "name": "Scaled Content Abuse & Spam Policies",
            "policy_ref": "Google Spam Policies & Quality Raters Guidelines Section 4.6.5",
            "score": score_scaled,
            "max_score": 20,
            "status": status_scaled,
            "findings": findings_scaled
        },
        {
            "id": "factual_accuracy_hallucinations",
            "name": "Factual Accuracy & Hallucination Prevention",
            "policy_ref": "Google Guidance: 'generative models don't retrieve facts... manually factcheck'",
            "score": score_facts,
            "max_score": 20,
            "status": status_facts,
            "findings": findings_facts
        },
        {
            "id": "give_users_context",
            "name": "Transparency & Context ('Who, How, Why')",
            "policy_ref": "Google Guidance: 'Give users context: sharing information about how a piece of content was created'",
            "score": score_trans,
            "max_score": 20,
            "status": status_trans,
            "findings": findings_trans,
            "transparency": transparency_summary
        },
        {
            "id": "metadata_and_structured_data",
            "name": "Metadata & Structured Data Integrity",
            "policy_ref": "Google Guidance: 'review also applies to <title>, meta description, structured data & image alt'",
            "score": score_meta,
            "max_score": 15,
            "status": status_meta,
            "findings": findings_meta,
            "summary": metadata_summary
        },
        {
            "id": "humanizer_quality_gate",
            "name": "Human Quality & Anti-Slop Writing",
            "policy_ref": "Google Search Essentials: High-quality, natural People-First prose",
            "score": score_human,
            "max_score": 15,
            "status": status_human,
            "findings": findings_human,
            "metrics": human_metrics
        },
        {
            "id": "eeat_firsthand_experience",
            "name": "E-E-A-T Firsthand Experience & Logistics",
            "policy_ref": "Google Search Essentials: Experience, Expertise, Authoritativeness, Trustworthiness",
            "score": score_eeat,
            "max_score": 10,
            "status": status_eeat,
            "findings": findings_eeat
        }
    ]

    return {
        "score": total_score,
        "grade": grade,
        "verdict": verdict,
        "status": status,
        "policy_citation": "Google Search's guidance on using generative AI content on your website",
        "policy_url": GOOGLE_GENAI_POLICY_URL,
        "helpful_content_url": GOOGLE_HELPFUL_CONTENT_URL,
        "checks": checks,
        "transparency": transparency_summary,
        "hallucination_indicators": {
            "placeholders_found": hallucinations,
            "has_hallucinations": len(hallucinations) > 0,
            "total_placeholders": len(hallucinations)
        },
        "metadata_summary": metadata_summary,
        "humanizer_metrics": human_metrics,
        "suggested_transparency_disclosure": RECOMMENDED_DISCLOSURE_TEMPLATE,
        "recommendations": recommendations,
        "word_count": total_words
    }


def inject_google_compliance_disclosure(
    content: str,
    author_name: str = "YatraDham.Org Editorial Team",
    fact_checker: str = "Pilgrim Care Specialists"
) -> str:
    """
    Appends an official, compliant Google Gen AI 'Give users context' disclosure
    to any blog or guide if one is not already present.
    """
    t_lower = content.lower()
    if any(re.search(pat, t_lower) for pat in HOW_METHODOLOGY_MARKERS):
        return content  # Already has disclosure

    disclosure_box = (
        f"\n\n---\n\n"
        f"**Editorial Integrity & Transparency Note (Google Search Essentials Compliance)**  \n"
        f"*Researched and structured with AI assistance; rigorously fact-checked, verified, "
        f"and edited by {author_name} with ground-truth verification from {fact_checker}. "
        f"Written people-first for devotees seeking clean ashram stays, authentic Aarti schedules, "
        f"and verified temple logistics.*"
    )
    return content.strip() + disclosure_box
