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

    # Enforce 2-4 words and eliminate heading slogans like 'Begin Your Wellness'
    pk = result.get("primary_keyword", "").strip()
    banned_slogans = ["begin your", "start your", "discover our", "welcome to", "about our", "join us"]
    if any(pk.lower().startswith(s) for s in banned_slogans) or len(pk.split()) < 2 or len(pk.split()) > 4:
        name_clean = package_data.get("name", "")
        dest_clean = package_data.get("destination", "").split(",")[0].strip()
        cat = package_data.get("category", "tour").lower()
        
        if cat == "wellness":
            result["primary_keyword"] = f"Yoga Retreat {dest_clean}" if dest_clean else f"{name_clean[:20]} Retreat"
        elif cat == "stay":
            result["primary_keyword"] = f"Dharamshala in {dest_clean}" if dest_clean else f"{name_clean[:20]} Stay"
        elif "chardham" in name_clean.lower():
            result["primary_keyword"] = "Char Dham Yatra Package"
        else:
            result["primary_keyword"] = f"{dest_clean} Tour Package" if dest_clean else f"{name_clean[:20]} Tour"


    # Enrich secondary keywords via Datamuse API (free, keyless)
    try:
        from public_apis_enricher import fetch_semantic_lsi_keywords
        dest_term = package_data.get("destination", "").split(",")[0].strip()
        lsi = fetch_semantic_lsi_keywords(f"{dest_term} yoga wellness", max_results=4)
        if lsi:
            existing = result.get("secondary_keywords", [])
            for term in lsi:
                kw_candidate = f"{term} in {dest_term}".title()
                if kw_candidate not in existing and len(kw_candidate.split()) <= 4:
                    existing.append(kw_candidate)
            result["secondary_keywords"] = existing[:5]
    except Exception:
        pass

    return result

