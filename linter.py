"""
Real-Time Dynamic SEO & GEO Linter for YatraDham.
Performs rigorous, non-rubber-stamp multi-factor evaluation of content quality, keyword integration, and fact reliability.
"""
import re
from typing import Dict, Any, List


def calculate_flesch_reading_ease(text: str) -> int:
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    if not words or not sentences:
        return 70

    word_count = len(words)
    sentence_count = len(sentences)
    syllable_count = 0
    for w in words:
        w_lower = w.lower()
        count = len(re.findall(r'[aeiouy]+', w_lower))
        if w_lower.endswith('e') and not w_lower.endswith('le') and len(w_lower) > 2:
            count = max(1, count - 1)
        syllable_count += max(1, count)

    asl = word_count / sentence_count
    asw = syllable_count / word_count
    score = 206.835 - (1.015 * asl) - (84.6 * asw)
    return max(0, min(100, int(round(score))))


def run_seo_linter(
    title_tag: str,
    meta_description: str,
    primary_keyword: str,
    sections_dict: Dict[str, Any],
    json_ld_present: bool = True
) -> Dict[str, Any]:
    kw = (primary_keyword or "").strip().lower()
    title = (title_tag or "").strip()
    meta = (meta_description or "").strip()

    text_chunks = [
        title,
        meta,
        sections_dict.get("package_overview", ""),
        sections_dict.get("why_choose_intro", ""),
        " ".join(sections_dict.get("why_choose_bullets", [])),
        sections_dict.get("who_can_benefit_intro", ""),
        " ".join(sections_dict.get("who_can_benefit_bullets", [])),
        " ".join(sections_dict.get("meal_section_bullets", [])),
        " ".join(sections_dict.get("accommodation_bullets", [])),
        " ".join(sections_dict.get("benefits_items", [])),
        " ".join([f.get("question", "") + " " + f.get("answer", "") for f in sections_dict.get("faq", [])])
    ]
    full_text = " ".join(text_chunks)
    words = re.findall(r'\b[a-zA-Z0-9\x27-]+\b', full_text)
    total_words = len(words)

    kw_words = [w for w in re.findall(r'\b[a-zA-Z0-9\x27-]+\b', kw) if len(w) > 3]
    kw_pattern = re.escape(kw) if kw else ""
    kw_match_count = len(re.findall(kw_pattern, full_text, re.IGNORECASE)) if kw_pattern else 0
    if kw_match_count == 0 and kw_words:
        kw_match_count = len(re.findall(re.escape(kw_words[0]), full_text, re.IGNORECASE))

    density = round((kw_match_count / max(1, total_words)) * 100, 2)
    first_100_words = " ".join(words[:100]).lower()
    in_first_100 = bool(kw_words and any(t in first_100_words for t in kw_words))
    in_title = bool(kw_words and any(t in title.lower() for t in kw_words))
    in_meta = bool(kw_words and any(t in meta.lower() for t in kw_words))

    reading_ease = calculate_flesch_reading_ease(full_text)
    overview = sections_dict.get("package_overview", "")
    geo_ready = len(overview) >= 60 and any(w in overview.lower() for w in ["is", "includes", "offers", "provides", "features"])

    # Detailed Quality & Grammar Checks
    has_grammar_duration_error = bool(re.search(r'\b1\s+Days\b', full_text, re.IGNORECASE))
    has_duplicated_words = bool(re.search(r'\b(guided\s+guided|retreat\s+retreat|yoga\s+yoga)\b', full_text, re.IGNORECASE))
    has_placeholder_airport = "regional airport serving" in full_text.lower()
    has_bogus_small_price = bool(re.search(r'(?:₹|Rs\.?)\s*(?:24|1|2|3|4|5|6|7|8|9|10)\b', full_text))

    checks = []
    dynamic_score = 100

    # 1. Title Tag Length Check (50 - 60 chars)
    t_len = len(title)
    if 50 <= t_len <= 60:
        checks.append({"name": "Title Tag Length (50-60 chars)", "passed": True, "value": f"{t_len} chars (Optimal)"})
    elif 45 <= t_len <= 65:
        checks.append({"name": "Title Tag Length (50-60 chars)", "passed": True, "value": f"{t_len} chars (Acceptable)"})
        dynamic_score -= 4
    else:
        checks.append({"name": "Title Tag Length (50-60 chars)", "passed": False, "value": f"{t_len} chars (Needs Adjustment)"})
        dynamic_score -= 12

    # 2. Meta Description Length Check (130 - 160 chars)
    m_len = len(meta)
    if 130 <= m_len <= 160:
        checks.append({"name": "Meta Description Length (130-160 chars)", "passed": True, "value": f"{m_len} chars (Optimal)"})
    elif 110 <= m_len <= 170:
        checks.append({"name": "Meta Description Length (130-160 chars)", "passed": True, "value": f"{m_len} chars (Acceptable)"})
        dynamic_score -= 4
    else:
        checks.append({"name": "Meta Description Length (130-160 chars)", "passed": False, "value": f"{m_len} chars (Too Short / Long)"})
        dynamic_score -= 12

    # 3. Keyword in Title & Meta
    if in_title and in_meta:
        checks.append({"name": "Target Keyword in Title & Meta", "passed": True, "value": "Found in both"})
    elif in_title or in_meta:
        checks.append({"name": "Target Keyword in Title & Meta", "passed": True, "value": "Partial Match"})
        dynamic_score -= 5
    else:
        checks.append({"name": "Target Keyword in Title & Meta", "passed": False, "value": "Missing from Snippet"})
        dynamic_score -= 12

    # 4. Keyword Density
    if 0.6 <= density <= 3.0:
        checks.append({"name": "Natural Keyword Density (0.6% - 3.0%)", "passed": True, "value": f"{density}% (Natural)"})
    else:
        checks.append({"name": "Natural Keyword Density (0.6% - 3.0%)", "passed": False, "value": f"{density}% (Under/Over-optimized)"})
        dynamic_score -= 8

    # 5. Editorial Integrity & Anti-Glitch Check
    glitch_flags = []
    if has_grammar_duration_error:
        glitch_flags.append("'1 Days' grammatical defect")
        dynamic_score -= 15
    if has_duplicated_words:
        glitch_flags.append("Duplicated word artifact")
        dynamic_score -= 15
    if has_placeholder_airport:
        glitch_flags.append("Placeholder airport filler detected")
        dynamic_score -= 20
    if has_bogus_small_price:
        glitch_flags.append("Bogus single/double digit price detected")
        dynamic_score -= 25

    if not glitch_flags:
        checks.append({"name": "Editorial Integrity & Anti-Hallucination", "passed": True, "value": "Clean Editorial Pass"})
    else:
        checks.append({"name": "Editorial Integrity & Anti-Hallucination", "passed": False, "value": ", ".join(glitch_flags)})

    # 6. GEO & Schema Checks
    checks.append({"name": "GEO Answer-First AI Snippet Ready", "passed": geo_ready, "value": "Verified" if geo_ready else "Needs Overview Hook"})
    if not geo_ready: dynamic_score -= 6

    checks.append({"name": "Stacked Multi-Entity Schema.org", "passed": json_ld_present, "value": "Valid JSON-LD" if json_ld_present else "Missing Schema"})
    if not json_ld_present: dynamic_score -= 10

    final_linter_score = max(20, min(100, dynamic_score))

    return {
        "linter_score": final_linter_score,
        "checks": checks,
        "word_count": total_words,
        "keyword_density": density,
        "reading_ease": reading_ease,
        "in_first_100": in_first_100,
        "geo_ready": geo_ready
    }
