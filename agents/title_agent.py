"""Title tag agent: 50-60 chars, optimized for click-through rate with accurate product matching."""
import json, re
from typing import Dict, Any
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an elite SEO title tag specialist for YatraDham.Org, India's first dedicated religious tourism and wellness travel platform.

Given a package name and destination, write ONE compelling SEO title tag.

STRICT RULES:
- MUST be EXACTLY between 50 and 60 characters including spaces. Count carefully.
- MUST include the destination (city/state).
- Format: "Primary Benefit/Feature in Destination | YatraDham"
- NEVER repeat words unnecessarily.
- Keep it punchy, authentic and clickable.

GOOD examples:
- "Ayurvedic Stress Relief Retreat in Kerala | YatraDham" (55 chars)
- "3-Day Panchakarma Detox in Kangra, HP | YatraDham" (50 chars)
- "Yoga & Meditation Ashram Stay in Rishikesh | YatraDham" (54 chars)
- "Corporate Wellness & Stress Relief in Delhi | YatraDham" (55 chars)

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
CRITICAL: Do NOT repeat words. Match the exact program topic. End with " | YatraDham"."""

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
    except Exception:
        result = {}

    title = result.get("title_tag", "")

    # If title is empty or generic, build an authentic title from package name
    if not title or len(title) < 20 or "Tour Package" in title and category == "wellness":
        dest_city = destination.split(",")[0].strip() if destination else "India"
        clean_name = re.sub(r'\s*\|.*$', '', name).strip()
        
        # Match product theme accurately
        if "corporate" in clean_name.lower():
            base = f"Corporate Wellness & Leadership Retreat in {dest_city}"
        elif "ayurved" in clean_name.lower() or "panchakarma" in clean_name.lower():
            if "panchakarma" in clean_name.lower():
                base = f"{duration} Panchakarma Detox in {dest_city}"
            else:
                base = f"{duration} Ayurveda Retreat in {dest_city}"
        elif "kriya" in clean_name.lower() or "silence" in clean_name.lower() or "ashram" in clean_name.lower():
            base = f"{duration} Meditation & Ashram Stay in {dest_city}"
        elif "yoga" in clean_name.lower():
            base = f"{duration} Yoga & Wellness Retreat in {dest_city}"
        elif category == "wellness":
            base = f"{clean_name} in {dest_city}" if len(clean_name) < 40 else f"{duration} Wellness Retreat in {dest_city}"
        elif category == "stay":
            base = f"{clean_name} Stay Booking in {dest_city}" if len(clean_name) < 38 else f"Dharamshala Stay in {dest_city}"
        elif category == "puja":
            base = f"{clean_name} Online Puja Booking" if len(clean_name) < 40 else f"Online Puja & Pandit Booking in {dest_city}"
        else:
            base = f"{duration} {dest_city} Spiritual Yatra Tour"

        title = f"{base} | YatraDham"

    # Enforce exact 50-60 character boundary cleanly at word boundaries
    if len(title) > 60:
        suffix = " | YatraDham"
        max_main_len = 60 - len(suffix)
        main_part = title.split(" | ")[0]
        if len(main_part) > max_main_len:
            words = main_part.split(" ")
            shortened = ""
            for w in words:
                if len((shortened + " " + w).strip()) <= max_main_len:
                    shortened = (shortened + " " + w).strip()
                else:
                    break
            main_part = shortened if shortened else main_part[:max_main_len]
        title = f"{main_part}{suffix}"

    return {"title_tag": title}
