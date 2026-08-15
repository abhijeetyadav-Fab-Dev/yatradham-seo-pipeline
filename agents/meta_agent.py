"""Meta description agent: 145-155 chars + forced CTA."""
import json
from typing import Dict, Any
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an elite SEO meta description specialist for Yatradham, India's leading wellness travel platform.
Given a title and package details, output a JSON object with:
- meta_description: a compelling summary, EXACTLY between 145 and 155 characters including spaces.

STRICT Rules:
- MUST end with a strong call-to-action (CTA) like: "Book now!", "Enquire today!", or "Reserve your spot!"
- MUST be EXACTLY between 145 and 155 characters. Count carefully.
- Include the primary keyword and destination naturally.
- Write for humans — persuasive, active voice, and engaging.
- Never truncate mid-sentence or mid-word.
- Output valid JSON only: {"meta_description": "your meta description here"}"""


def run(package_data: Dict[str, Any], title_tag: str, primary_keyword: str, client: LLMClient) -> Dict[str, Any]:
    name = package_data.get('name', '')
    destination = package_data.get('destination', '')
    duration = package_data.get('duration', '')
    
    user_msg = f"""Title: {title_tag}
Primary Keyword: {primary_keyword}
Package: {name}
Destination: {destination}
Duration: {duration}

Generate ONE perfect SEO meta description between 145 and 155 characters, ending with a call to action."""

    content = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=300,
        temperature=0.5,
        response_format={"type": "json_object"},
    )
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {}

    meta = result.get("meta_description", "")
    
    # Smart Fallback if empty
    if not meta:
        fallback = f"Experience our {duration} {name} in {destination}. Rejuvenate your mind, body, and soul with our expert wellness program. Book your transformative journey today!"
        meta = fallback.replace("  ", " ").strip()
        
    # Enforce length
    if len(meta) < 145:
        meta = (meta + " Discover true peace and authentic wellness with Yatradham. Reserve your spot today!").replace("  ", " ").strip()
    if len(meta) > 155:
        meta = meta[:152].rsplit(" ", 1)[0] + "..."
        if len(meta) < 145:
            meta = (meta + " Book now!").strip()

    # Force CTA
    ctas = ["book now", "enquire today", "reserve your spot", "plan your trip", "contact us today"]
    has_cta = any(cta in meta.lower() for cta in ctas)
    if not has_cta:
        meta = meta.rstrip(".") + ". Book now!"
        if len(meta) > 155:
            meta = meta[:152].rsplit(" ", 1)[0] + ". Book now!"

    result["meta_description"] = meta
    return result
