"""Meta description agent: 145-155 chars, natural language, no repetition."""
import json
import re
from typing import Dict, Any
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an elite SEO meta description specialist for YatraDham.Org, India's first dedicated religious tourism and wellness travel platform.

Given a title tag and package details, write ONE compelling meta description.

STRICT RULES:
- MUST be EXACTLY between 145 and 155 characters including spaces. Count carefully.
- MUST include the destination (city/state) and package type naturally.
- MUST end with a call-to-action: "Book now!", "Enquire today!", or "Reserve your spot!"
- Write for humans — persuasive, active voice, benefit-focused.
- NEVER repeat the package name or title tag word-for-word inside the description.
- NEVER concatenate the package name multiple times (this is the most critical rule).
- Include specific details when available: duration, therapies, accommodation type.
- Use the brand name "YatraDham" only once if it fits.
- Never truncate mid-sentence or mid-word.

GOOD examples:
- "Rejuvenate with a 22-day Ayurvedic stress relief retreat in Palakkad, Kerala. Includes villa stay, Satvik meals & doctor consultation. Book now!"
- "Experience a 3-day yoga and Ayurveda retreat in Nepal with guided meditation, organic meals & mountain views. Reserve your spot!"
- "Detox your body with 5-day Panchakarma in Almora. Includes herbal therapies, yoga sessions & vegetarian meals. Enquire today!"

BAD examples (NEVER do these):
- "Experience our 22 DAYS 22 Day Ayurvedic Stress Relief Retreat In Kerala in 22 Day Ayurvedic Stress Relief Retreat In Kerala"
- "Experience our 3 Days 3 Days Yoga & Ayurveda Retreat in Nepal in 3 Day Yoga And Ayurveda Retreat In Nepal"

Output valid JSON only: {"meta_description": "your description here"}"""


def run(package_data: Dict[str, Any], title_tag: str, primary_keyword: str, client: LLMClient) -> Dict[str, Any]:
    name = package_data.get('name', '')
    destination = package_data.get('destination', '')
    duration = package_data.get('duration', '')
    raw_text = package_data.get('raw_text', '')[:500]  # First 500 chars for context

    user_msg = f"""Title Tag: {title_tag}
Primary Keyword: {primary_keyword}
Package Name: {name}
Destination: {destination}
Duration: {duration}
Page Context: {raw_text}

Generate ONE perfect SEO meta description between 145 and 155 characters.
CRITICAL: Do NOT repeat the package name. Write a FRESH, benefit-focused summary ending with a CTA."""

    content = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=300,
        temperature=0.5,
        response_format={"type": "json_object"},
    )

    # Robust JSON extraction
    try:
        clean = content.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()
        if "{" in clean and "}" in clean:
            clean = clean[clean.find("{"):clean.rfind("}") + 1]
        result = json.loads(clean)
    except json.JSONDecodeError:
        result = {}

    meta = result.get("meta_description", "")

    # Anti-repetition check: if the package name appears more than once, rebuild
    if meta and name and meta.lower().count(name.lower()[:20]) > 1:
        meta = ""  # Force fallback — repetitive content detected

    # Smart fallback if empty — build from components, never repeat name
    if not meta:
        # Extract actual destination city from raw data
        dest = destination if destination else "India"
        dur = duration if duration else ""

        # Build a natural description from components
        if "ayurved" in name.lower() or "ayurved" in primary_keyword.lower():
            meta = f"Rejuvenate with a {dur} Ayurvedic wellness retreat in {dest}. Includes therapies, yoga, healthy meals & verified stay through YatraDham. Book now!"
        elif "yoga" in name.lower() or "yoga" in primary_keyword.lower():
            meta = f"Join a {dur} yoga retreat in {dest} with guided meditation, pranayama, healthy meals & comfortable accommodation via YatraDham. Book now!"
        elif "detox" in name.lower() or "panchakarma" in primary_keyword.lower():
            meta = f"Experience a {dur} Panchakarma detox program in {dest}. Includes herbal therapies, yoga, organic meals & verified accommodation. Enquire today!"
        else:
            meta = f"Discover a {dur} wellness retreat in {dest}. Includes accommodation, meals, guided activities & YatraDham booking support. Reserve your spot!"

        meta = meta.replace("  ", " ").strip()

    # Enforce length: 145-155 characters
    if len(meta) < 145:
        meta = (meta.rstrip("!.") + ". Discover authentic wellness with YatraDham. Book now!").replace("  ", " ").strip()
    if len(meta) > 155:
        meta = meta[:152].rsplit(" ", 1)[0] + "..."
        if len(meta) < 145:
            meta = meta.rstrip(".") + " Book now!"

    # Force CTA at end
    ctas = ["book now", "enquire today", "reserve your spot", "plan your trip", "contact us"]
    has_cta = any(cta in meta.lower() for cta in ctas)
    if not has_cta:
        meta = meta.rstrip(".!") + ". Book now!"
        if len(meta) > 155:
            meta = meta[:152].rsplit(" ", 1)[0] + ". Book now!"

    result["meta_description"] = meta
    return result
