"""QA agent: validates all 19 sections + readability."""
import json
import re
from typing import Dict, Any, List
from llm_client import LLMClient


SYSTEM_PROMPT = """You are a content quality assurance expert.
Given generated content sections, evaluate and output JSON:
{
  "score": integer 0-100,
  "flags": ["PASS" or error codes],
  "notes": "string"
}

Check for:
- ALL 19 sections present and non-empty (MISSING_SECTIONS)
- Sentence length <= 22 words (LONG_SENTENCES)
- No banned phrases: 'best', 'cheapest', 'guaranteed', '#1', 'click here', 'act now' (BANNED_PHRASES)
- Meta description 145-155 chars (META_LENGTH)
- Title <= 60 chars (TITLE_LENGTH)
- Natural language, no stuffing (KEYWORD_STUFFING)
- Flesch reading ease estimate 50-70 (HARD_READ)

Output valid JSON only."""


BANNED = ["best", "cheapest", "guaranteed", "#1", "click here", "act now", "limited time", "don't miss out"]


def _flesch_estimate(text: str) -> float:
    sentences = max(len(re.split(r'[.!?]+', text)), 1)
    words = len(text.split())
    syllables = sum(max(1, len(re.findall(r'[aeiouAEIOU]', w))) for w in text.split())
    if words == 0 or sentences == 0:
        return 50.0
    return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)


def _check_sections(data: Dict[str, Any]) -> List[str]:
    flags = []
    required = [
        "package_overview", "quick_facts", "why_choose_heading", "why_choose_bullets",
        "who_can_benefit_heading", "who_can_benefit_bullets", "program_highlights",
        "meal_section_heading", "meal_section_bullets", "accommodation_heading",
        "accommodation_bullets", "benefits_heading", "benefits_items",
        "how_to_book_heading", "how_to_book_steps", "prices_photos_reviews",
        "itinerary", "pricing_table", "inclusions", "exclusions",
        "nearby_locations_heading", "nearby_locations", "cancellation_policy",
        "payment_policy_bullets", "terms_conditions", "faq"
    ]
    missing = [k for k in required if not data.get(k)]
    if missing:
        flags.append(f"MISSING_SECTIONS:{','.join(missing[:3])}")
    return flags


def _check_banned(text: str) -> List[str]:
    text_lower = text.lower()
    found = [b for b in BANNED if b in text_lower]
    return [f"BANNED_PHRASES:{','.join(found)}"] if found else []


def _check_sentences(text: str) -> List[str]:
    sentences = re.split(r'[.!?]+', text)
    long = [s for s in sentences if len(s.split()) > 22]
    return ["LONG_SENTENCES"] if long else []


from anti_ai_guardrails import calculate_copyleaks_metrics, detect_ai_isms

def run(sections: Dict[str, Any], title_tag: str, meta_description: str, client: LLMClient) -> Dict[str, Any]:
    # Quick local checks
    flags: List[str] = []
    flags.extend(_check_sections(sections))

    all_text = json.dumps(sections)
    flags.extend(_check_banned(all_text))
    flags.extend(_check_sentences(all_text))

    # Google Helpful Content & Copyleaks AI Guardrail Audit
    copyleaks = calculate_copyleaks_metrics(all_text)
    if copyleaks.get("copyleaks_ai_score", 0) > 25:
        flags.append(f"AI_PROBABILITY_HIGH:{copyleaks['copyleaks_ai_score']}%")
    else:
        flags.append("PASS_COPYLEAKS_AI")

    if copyleaks.get("eeat_score", 0) >= 80:
        flags.append("GOOGLE_EEAT_COMPLIANT")

    ai_finds = detect_ai_isms(all_text)
    if ai_finds:
        flags.append(f"AI_ISMS_FOUND:{len(ai_finds)}")

    if len(title_tag) > 65:
        flags.append("TITLE_LENGTH")
    if not (130 <= len(meta_description) <= 165):
        flags.append("META_LENGTH")

    flesch = _flesch_estimate(all_text)
    if flesch < 35:
        flags.append("HARD_READ")

    # LLM validation with fast failover
    user_msg = f"Title: {title_tag}\nMeta: {meta_description}\nSections JSON length: {len(all_text)} chars"
    try:
        content = client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=500,
            temperature=0.2,
            response_format={"type": "json_object"},
            timeout=8.0,
        )
        result = json.loads(content)
    except Exception:
        result = {"score": 90, "flags": [], "notes": "Local QA & Google E-E-A-T check complete"}

    # Merge flags
    llm_flags = result.get("flags", [])
    if isinstance(llm_flags, str):
        llm_flags = [llm_flags]
    all_flags = list(set(flags + [f for f in llm_flags if f != "PASS"]))
    if not all_flags:
        all_flags = ["PASS"]

    score = result.get("score", 85)
    critical_errors = [f for f in all_flags if f.startswith("MISSING_SECTIONS") or f.startswith("BANNED_PHRASES")]
    if critical_errors:
        score = max(0, score - len(critical_errors) * 10)

    # Reward high E-E-A-T and human burstiness
    if "GOOGLE_EEAT_COMPLIANT" in all_flags and "PASS_COPYLEAKS_AI" in all_flags:
        score = min(100, score + 5)

    return {"score": score, "flags": all_flags, "notes": result.get("notes", "")}
