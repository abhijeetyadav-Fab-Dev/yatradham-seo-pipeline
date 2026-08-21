"""Title tag agent: 50-60 chars, optimized for click-through rate."""
import json
from typing import Dict, Any
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an elite SEO title tag specialist for YatraDham.Org, India's first dedicated religious tourism and wellness travel platform.

Given a package name and destination, write ONE compelling SEO title tag.

STRICT RULES:
- MUST be EXACTLY between 50 and 60 characters including spaces. Count carefully.
- MUST include the destination (city/state).
- Format: "Primary Benefit/Feature in Destination | YatraDham"
- NEVER repeat words unnecessarily (e.g., "Retreat Retreat").
- NEVER include the exact package name if it makes the title too long or repetitive.
- Keep it punchy and clickable.

GOOD examples:
- "Ayurvedic Stress Relief Retreat in Kerala | YatraDham" (55 chars)
- "3-Day Panchakarma Detox in Almora | YatraDham.Org" (49 chars)
- "Yoga & Meditation Ashram Stay in Rishikesh | YatraDham" (54 chars)

Output valid JSON only: {"title_tag": "your title here"}"""


def run(package_data: Dict[str, Any], primary_keyword: str, client: LLMClient) -> Dict[str, Any]:
    name = package_data.get('name', '')
    destination = package_data.get('destination', '')
    duration = package_data.get('duration', '')
    category = package_data.get('category', 'auto')

    user_msg = f"""Primary Keyword: {primary_keyword}
Package Name: {name}
Category: {category}
Destination: {destination}
Duration: {duration}

Generate ONE perfect SEO title tag between 50 and 60 characters for this {category.upper()} package.
CRITICAL: Do NOT repeat words. End with " | YatraDham"."""

    content = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=200,
        temperature=0.4,
        response_format={"type": "json_object"},
    )

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

    title = result.get("title_tag", "")

    # Basic anti-repetition check
    if title and name and title.lower().count(name.lower()[:15]) > 1:
        title = ""

    if not title:
        dest = destination if destination else "India"
        name_lower = f"{name} {primary_keyword}".lower()
        if category == "wellness" or "yoga" in name_lower or "ayurved" in name_lower:
            base = name if len(name) < 45 and not name.lower().startswith("spiritual") else f"Yoga & Wellness Retreat in {dest}"
            title = f"{base} | YatraDham"
        elif category == "stay" or any(k in name_lower for k in ["dharamshala", "ashram stay", "bhavan", "hotel", "room", "trh", "gmvn"]):
            base = name if len(name) < 45 and not name.lower().startswith("spiritual") else f"Dharamshala Stay in {dest}"
            title = f"{base} | YatraDham"
        elif category == "puja" or "puja" in name_lower:
            base = name if len(name) < 45 else f"Online Puja & Pandit Booking in {dest}"
            title = f"{base} | YatraDham"
        else:
            base = name if len(name) < 45 and not name.lower().startswith("spiritual") else f"{duration} {dest} Tour Package"
            title = f"{base} | YatraDham"

    # Enforce length
    if len(title) > 60:
        parts = title.split(" | ")
        if len(parts) == 2:
            main_part = parts[0]
            if len(main_part) > 45:
                main_part = main_part[:42] + "..."
            title = f"{main_part} | YatraDham"
        else:
            title = title[:57] + "..."

    return {"title_tag": title}
