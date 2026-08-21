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

    meta = str(result.get("meta_description") or "").strip()

    # Anti-repetition check: if the package name appears more than once, rebuild
    if meta and name and meta.lower().count(name.lower()[:20]) > 1:
        meta = ""  # Force fallback — repetitive content detected

    # Smart fallback if empty or too short
    if not meta or len(meta) < 40:
        dest = destination if destination else "Yamunotri, Uttarakhand"
        dur = duration if duration else "15 Days"

        # Build a natural description from components
        if "gmvn" in name.lower() or "trh" in name.lower() or "dharamshala" in name.lower() or "ashram" in name.lower():
            meta = f"Book verified stay at {name[:40]} in {dest}. Clean rooms, hot water, authentic satvik meals & easy temple access. Reserve your spot now!"
        elif "ayurved" in name.lower() or "ayurved" in primary_keyword.lower():
            meta = f"Rejuvenate with a {dur} Ayurvedic wellness retreat in {dest}. Includes therapies, yoga, healthy meals & verified stay. Book now!"
        elif "yoga" in name.lower() or "yoga" in primary_keyword.lower():
            meta = f"Join a {dur} yoga retreat in {dest} with guided meditation, pranayama, healthy meals & verified accommodation. Book now!"
        elif "detox" in name.lower() or "panchakarma" in primary_keyword.lower():
            meta = f"Experience a {dur} Panchakarma detox program in {dest}. Includes herbal therapies, yoga, organic meals & verified stay. Enquire today!"
        else:
            meta = f"Discover verified accommodation & tour packages in {dest} with YatraDham. Clean rooms, satvik meals & seamless booking. Book now!"

    # Clean double periods or whitespace glitches
    meta = meta.replace("..", ".").replace("  ", " ").strip()

    # Ensure CTA at end
    ctas = ["book now", "enquire today", "reserve your spot", "plan your trip", "contact us"]
    if not any(cta in meta.lower() for cta in ctas):
        meta = meta.rstrip(".!, ") + ". Book now!"

    # Enforce strictly: max 155 characters (and NEVER exceed 160)
    if len(meta) > 155:
        target_cta = " Book now!"
        max_base = 155 - len(target_cta)
        base = meta[:max_base].rsplit(" ", 1)[0].rstrip(".!, ")
        meta = f"{base}.{target_cta}"

    # Final length and sanity check
    meta = meta.replace("..", ".").strip()
    if len(meta) > 160:
        meta = meta[:157].rsplit(" ", 1)[0] + "..."

    result["meta_description"] = meta
    return result
