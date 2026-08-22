"""Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)."""
import json
import re
from typing import Dict, Any
from llm_client import LLMClient


HINDI_PROMPT = """You are a native Hindi copywriter specializing in Sanatan Dharma pilgrimages and Vedic wellness for YatraDham.Org.
Translate and localize this package into authentic, respectful, devotional Hindi (Devanagari script).
Use natural spiritual vocabulary (e.g. 'सात्विक आहार', 'आरती दर्शन', 'आश्रम प्रवास', 'पंजीकरण').
Output valid JSON only with the same key structure."""

GUJARATI_PROMPT = """You are a native Gujarati copywriter specializing in pilgrimage travel and wellness for YatraDham.Org.
Translate and localize this package into authentic, respectful Gujarati script.
Use culturally appropriate Gujarati terminology for spiritual tours and ashram stays.
Output valid JSON only with the same key structure."""


def localize_content(output_dict: Dict[str, Any], target_language: str, client: LLMClient) -> Dict[str, Any]:
    """Translate and culturally localize SEOOutput sections into Hindi or Gujarati."""
    if target_language not in ["hi", "gu"]:
        return output_dict

    sections = output_dict.get("sections", {})
    title = output_dict.get("title_tag", "")
    meta = output_dict.get("meta_description", "")
    
    system_prompt = HINDI_PROMPT if target_language == "hi" else GUJARATI_PROMPT
    user_payload = {
        "title_tag": title,
        "meta_description": meta,
        "package_overview": sections.get("package_overview", ""),
        "why_choose_heading": sections.get("why_choose_heading", ""),
        "why_choose_bullets": sections.get("why_choose_bullets", []),
        "who_can_benefit_heading": sections.get("who_can_benefit_heading", ""),
        "who_can_benefit_bullets": sections.get("who_can_benefit_bullets", []),
        "meal_section_heading": sections.get("meal_section_heading", ""),
        "meal_section_bullets": sections.get("meal_section_bullets", []),
        "accommodation_heading": sections.get("accommodation_heading", ""),
        "accommodation_bullets": sections.get("accommodation_bullets", []),
        "benefits_heading": sections.get("benefits_heading", ""),
        "benefits_items": sections.get("benefits_items", []),
        "faq": sections.get("faq", [])
    }
    
    try:
        raw_res = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)}
            ],
            max_tokens=3000,
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        
        # Parse JSON
        clean = raw_res.strip()
        if clean.startswith("```json"): clean = clean[7:]
        if clean.startswith("```"): clean = clean[3:]
        if clean.endswith("```"): clean = clean[:-3]
        clean = clean.strip()
        if "{" in clean and "}" in clean:
            clean = clean[clean.find("{"):clean.rfind("}") + 1]
        
        translated = json.loads(clean)
        
        # Merge translated fields
        new_output = dict(output_dict)
        new_output["language"] = target_language
        if "title_tag" in translated: new_output["title_tag"] = translated["title_tag"]
        if "meta_description" in translated: new_output["meta_description"] = translated["meta_description"]
        
        new_sections = dict(sections)
        for k in ["package_overview", "why_choose_heading", "why_choose_bullets", "who_can_benefit_heading", 
                  "who_can_benefit_bullets", "meal_section_heading", "meal_section_bullets", 
                  "accommodation_heading", "accommodation_bullets", "benefits_heading", "benefits_items", "faq"]:
            if k in translated:
                new_sections[k] = translated[k]
        
        new_output["sections"] = new_sections
        return new_output
    except Exception as e:
        # Fallback if API is offline
        return output_dict
