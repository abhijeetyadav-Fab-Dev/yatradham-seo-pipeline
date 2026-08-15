"""Keyword agent: enforces 2-4 word primary keyword."""
import json
from typing import Dict, Any
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an SEO keyword expert for Indian spiritual travel packages.
Given package details, output a JSON object with:
- primary_keyword: exactly 2-4 words, natural, no stuffing. Example: "Yoga Retreat Rishikesh"
- secondary_keywords: array of 3-5 related phrases

Rules:
- Primary keyword MUST be 2-4 words only.
- Use location + package type format.
- No duplicate words.
- Output valid JSON only."""


def run(package_data: Dict[str, Any], client: LLMClient) -> Dict[str, Any]:
    user_msg = f"Package: {package_data.get('name', '')}\nDestination: {package_data.get('destination', '')}\nDuration: {package_data.get('duration', '')}\nActivities: {package_data.get('activities', '')}"
    content = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=500,
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        result = {"primary_keyword": package_data.get("name", "Yoga Retreat"), "secondary_keywords": []}

    # Enforce 2-4 words
    pk = result.get("primary_keyword", "")
    word_count = len(pk.split())
    if word_count < 2 or word_count > 4:
        # Fallback
        words = [w for w in (package_data.get("name", "") + " " + package_data.get("destination", "")).split() if w]
        result["primary_keyword"] = " ".join(words[:3]) if len(words) >= 3 else " ".join(words) + " Retreat"

    return result
