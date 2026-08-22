"""Real-Time SEO & GEO (Generative Engine Optimization) Linter for YatraDham."""
import re
from typing import Dict, Any, List


def calculate_flesch_reading_ease(text: str) -> int:
    """Calculate Flesch Reading Ease score (0-100)."""
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]
    
    if not words or not sentences:
        return 70

    word_count = len(words)
    sentence_count = len(sentences)
    
    # Syllable approximation
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
    """Audit content for SEO and AI Overview (GEO) citation compliance."""
    kw = (primary_keyword or "").strip().lower()
    title = (title_tag or "").strip()
    meta = (meta_description or "").strip()
    
    # Aggregate all text
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
    words = re.findall(r'\b[a-zA-Z0-9\'-]+\b', full_text)
    total_words = len(words)
    
    # Keyword occurrences
    kw_words = re.findall(r'\b[a-zA-Z0-9\'-]+\b', kw)
    kw_match_count = 0
    if kw:
        # Match primary keyword phrase or primary tokens
        kw_pattern = re.escape(kw)
        kw_match_count = len(re.findall(kw_pattern, full_text, re.IGNORECASE))
        if kw_match_count == 0 and len(kw_words) > 1:
            # Check for core token presence
            core_token = kw_words[0]
            kw_match_count = len(re.findall(re.escape(core_token), full_text, re.IGNORECASE))

    density = round((kw_match_count / max(1, total_words)) * 100, 2)
    
    # First 100 words check
    first_100_words = " ".join(words[:100]).lower()
    in_first_100 = bool(kw and any(token in first_100_words for token in kw_words if len(token) > 3))
    
    in_title = bool(kw and any(token in title.lower() for token in kw_words if len(token) > 3))
    in_meta = bool(kw and any(token in meta.lower() for token in kw_words if len(token) > 3))
    
    reading_ease = calculate_flesch_reading_ease(full_text)
    
    # GEO Answer-First Check: Overview has concise, factual opening without fluff
    overview = sections_dict.get("package_overview", "")
    geo_ready = len(overview) >= 60 and ("is" in overview or "includes" in overview or "offers" in overview)
    
    # Score calculation (0 - 100)
    score = 40  # base
    if 50 <= len(title) <= 65: score += 12
    elif len(title) > 0: score += 6
    
    if 130 <= len(meta) <= 160: score += 12
    elif len(meta) > 0: score += 6
    
    if in_title: score += 10
    if in_meta: score += 8
    if in_first_100: score += 8
    if 0.8 <= density <= 2.8: score += 10
    if reading_ease >= 55: score += 5
    if json_ld_present: score += 5
    
    checks = [
        {"name": "Title Tag Length (50-65 chars)", "passed": 50 <= len(title) <= 65, "value": f"{len(title)} chars"},
        {"name": "Meta Description Length (130-160 chars)", "passed": 130 <= len(meta) <= 160, "value": f"{len(meta)} chars"},
        {"name": "Keyword in Title Tag", "passed": in_title, "value": "Found" if in_title else "Missing"},
        {"name": "Keyword in Meta Description", "passed": in_meta, "value": "Found" if in_meta else "Missing"},
        {"name": "Keyword in First 100 Words", "passed": in_first_100, "value": "Found" if in_first_100 else "Missing"},
        {"name": "Optimal Keyword Density (0.8% - 2.8%)", "passed": 0.8 <= density <= 2.8, "value": f"{density}%"},
        {"name": "Flesch Reading Ease (>= 55)", "passed": reading_ease >= 55, "value": f"{reading_ease}/100"},
        {"name": "GEO Answer-First AI Block Ready", "passed": geo_ready, "value": "Optimized" if geo_ready else "Review"},
        {"name": "Stacked JSON-LD Schema Generated", "passed": json_ld_present, "value": "Valid JSON-LD" if json_ld_present else "Missing"}
    ]
    
    return {
        "linter_score": min(100, score),
        "word_count": total_words,
        "keyword_density": density,
        "title_char_count": len(title),
        "meta_char_count": len(meta),
        "reading_ease": reading_ease,
        "checks": checks
    }
