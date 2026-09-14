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

    # If title is empty, too short, or mismatched, build an authentic title from package name
    if not title or len(title) < 20 or ("Tour Package" in title and category in ["wellness", "puja", "stay"]):
        dest_city = destination.split(",")[0].strip() if destination else "India"
        clean_name = re.sub(r'\s*\|.*$', '', name).strip()
        has_dest = dest_city.lower() in clean_name.lower()
        in_dest = "" if has_dest else f" in {dest_city}"

        # Match product theme accurately while retaining package name keywords
        if category == "puja" or "puja" in clean_name.lower() or "pandit" in clean_name.lower():
            if "puja" in clean_name.lower():
                base = f"{clean_name} Booking & Pandit Seva" if len(clean_name) <= 30 else f"{clean_name}{in_dest}"
            else:
                base = f"{clean_name} Puja Booking & Pandit Seva" if len(clean_name) <= 25 else f"{clean_name} Puja{in_dest}"
        elif category == "stay" or any(k in clean_name.lower() for k in ["dharamshala", "ashram", "hotel", "stay", "trh", "gmvn"]):
            if any(k in clean_name.lower() for k in ["dharamshala", "ashram", "hotel", "stay", "room"]):
                base = f"{clean_name} Room Booking{in_dest}" if len(clean_name) <= 28 else f"{clean_name}{in_dest}"
            else:
                base = f"{clean_name} Dharamshala Stay{in_dest}" if len(clean_name) <= 25 else f"{clean_name} Stay{in_dest}"
        elif category == "wellness" or any(k in clean_name.lower() for k in ["ayurved", "yoga", "detox", "retreat", "panchakarma"]):
            if any(k in clean_name.lower() for k in ["retreat", "program", "healing"]):
                base = f"{clean_name}{in_dest}" if len(clean_name) <= 35 else f"{duration} {clean_name}"[:45]
            else:
                base = f"{clean_name} Wellness Retreat{in_dest}" if len(clean_name) <= 25 else f"{clean_name}{in_dest}"
        else:
            if any(k in clean_name.lower() for k in ["yatra", "tour", "darshan"]):
                base = f"{clean_name}{in_dest}" if len(clean_name) <= 35 else f"{duration} {clean_name}"[:45]
            else:
                base = f"{duration} {clean_name} Spiritual Tour{in_dest}" if len(clean_name) <= 25 else f"{clean_name} Tour{in_dest}"

        title = f"{base} | YatraDham"

    # Enforce exact 50-60 character boundary cleanly
    title = re.sub(r'\b([A-Za-z0-9]+)(?:[\s,]+)\1\b', r'\1', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title).strip()

    # If title is shorter than 50 chars, enhance suffix or brand representation
    if len(title) < 50:
        if title.endswith(" | YatraDham") and len(title) + 4 <= 60:
            title = title[:-12] + " | YatraDham.Org"
        elif not title.endswith("YatraDham") and not title.endswith("YatraDham.Org"):
            if len(title) <= 45:
                title = f"{title} | YatraDham.Org"
            elif len(title) <= 48:
                title = f"{title} | YatraDham"

    # If still shorter than 50 chars, expand main title with category-relevant terms
    if len(title) < 50:
        main_part = title.split(" | ")[0]
        brand = " | YatraDham.Org"
        if category == "tour":
            if "tour" not in main_part.lower() and "package" not in main_part.lower() and len(f"{main_part} Tour Package") + len(brand) <= 60:
                title = f"{main_part} Tour Package{brand}"
            elif "package" not in main_part.lower() and len(f"{main_part} Package") + len(brand) <= 60:
                title = f"{main_part} Package{brand}"
            elif len(f"{main_part} Yatra Booking") + len(brand) <= 60:
                title = f"{main_part} Yatra Booking{brand}"
            elif len(f"{main_part} Booking") + len(brand) <= 60:
                title = f"{main_part} Booking{brand}"
        elif category == "stay":
            if "stay" not in main_part.lower() and "room" not in main_part.lower() and len(f"{main_part} Room Stay") + len(brand) <= 60:
                title = f"{main_part} Room Stay{brand}"
            elif "booking" not in main_part.lower() and len(f"{main_part} Room Booking") + len(brand) <= 60:
                title = f"{main_part} Room Booking{brand}"
            elif len(f"{main_part} Booking") + len(brand) <= 60:
                title = f"{main_part} Booking{brand}"
        elif category == "puja":
            if "puja" not in main_part.lower() and len(f"{main_part} Puja Booking") + len(brand) <= 60:
                title = f"{main_part} Puja Booking{brand}"
            elif "booking" not in main_part.lower() and len(f"{main_part} Booking & Seva") + len(brand) <= 60:
                title = f"{main_part} Booking & Seva{brand}"
        elif category == "wellness":
            if "retreat" not in main_part.lower() and len(f"{main_part} Wellness Retreat") + len(brand) <= 60:
                title = f"{main_part} Wellness Retreat{brand}"
            elif len(f"{main_part} Healing Retreat") + len(brand) <= 60:
                title = f"{main_part} Healing Retreat{brand}"

    if len(title) < 50:
        main_part = title.split(" | ")[0]
        if len(main_part) + len(" Online Booking | YatraDham") <= 60:
            title = f"{main_part} Online Booking | YatraDham"
        elif len(main_part) + len(" Guide | YatraDham.Org") <= 60:
            title = f"{main_part} Guide | YatraDham.Org"

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

    title = re.sub(r'\b([A-Za-z0-9]+)(?:[\s,]+)\1\b', r'\1', title, flags=re.IGNORECASE)
    return {"title_tag": title}
