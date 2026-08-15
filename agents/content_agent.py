"""Content agent: generates all 19 structured sections."""
import json
from typing import Dict, Any
from llm_client import LLMClient


SYSTEM_PROMPT = """You are an expert travel content writer for Indian spiritual tourism.
Given package details, generate ALL 19 sections as a single valid JSON object.

CRITICAL RULES:
- Sentences must be MAX 22 words each.
- Target Flesch reading ease 50-70.
- Use natural, engaging language.
- No keyword stuffing.
- Every section must be populated.
- Output ONLY valid JSON. No markdown, no explanation.

JSON SCHEMA:
{
  "package_overview": "string (2-3 sentences)",
  "quick_facts": {
    "package_name": "string",
    "cost": "string",
    "duration": "string",
    "destination": "string",
    "level": "string",
    "accommodation": "string",
    "food": "string",
    "activities": "string"
  },
  "why_choose_heading": "string",
  "why_choose_intro": "string (1 sentence)",
  "why_choose_bullets": ["string", "string", "string", "string", "string"],
  "who_can_benefit_heading": "string",
  "who_can_benefit_intro": "string (1 sentence)",
  "who_can_benefit_bullets": ["string", "string", "string", "string", "string"],
  "program_highlights": {
    "heading": "string",
    "morning": [{"time": "string", "activity": "string"}, {"time": "string", "activity": "string"}],
    "daytime": [{"time": "string", "activity": "string"}, {"time": "string", "activity": "string"}],
    "evening": [{"time": "string", "activity": "string"}, {"time": "string", "activity": "string"}]
  },
  "meal_section_heading": "string",
  "meal_section_bullets": ["string", "string"],
  "accommodation_heading": "string",
  "accommodation_bullets": ["string", "string"],
  "benefits_heading": "string",
  "benefits_items": ["string x8"],
  "how_to_book_heading": "string",
  "how_to_book_steps": ["string x6"],
  "prices_photos_reviews": "string (1-2 sentences with rating)",
  "itinerary": [
    {"day_number": 1, "sessions": [{"time": "string", "activity": "string"}, {"time": "string", "activity": "string"}]},
    {"day_number": 2, "sessions": [{"time": "string", "activity": "string"}, {"time": "string", "activity": "string"}]},
    {"day_number": 3, "sessions": [{"time": "string", "activity": "string"}, {"time": "string", "activity": "string"}]}
  ],
  "pricing_table": [
    {"guests": "string", "cost_per_person": "string"},
    {"guests": "string", "cost_per_person": "string"},
    {"guests": "string", "cost_per_person": "string"},
    {"guests": "string", "cost_per_person": "string"}
  ],
  "inclusions": ["string x6+"],
  "exclusions": ["string x15+"],
  "nearby_locations_heading": "string",
  "nearby_locations": [
    {"name": "string", "distance": "string", "type": "airport|railway|bus|sightseeing"},
    {"name": "string", "distance": "string", "type": "airport|railway|bus|sightseeing"}
  ],
  "cancellation_policy": "string (1 paragraph)",
  "payment_policy_bullets": ["string", "string", "string"],
  "terms_conditions": ["string x13"],
  "faq": [
    {"question": "string", "answer": "string"},
    {"question": "string", "answer": "string"},
    {"question": "string", "answer": "string"},
    {"question": "string", "answer": "string"}
  ]
}"""


def run(package_data: Dict[str, Any], primary_keyword: str, client: LLMClient) -> Dict[str, Any]:
    raw_text = package_data.get('raw_text', '')
    
    user_msg = f"""Generate all 19 sections for this package:
Name: {package_data.get('name', '')}
Destination: {package_data.get('destination', '')}
Duration: {package_data.get('duration', '')}
Primary Keyword: {primary_keyword}

--- RAW PAGE TEXT ---
{raw_text}
---------------------

Extract all the details accurately, especially the Pricing Tables (Cost Per person) and Hotel Details (Accommodation), from the raw text above. Output ONLY the JSON object."""

    content = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=4000,
        temperature=0.7,
        response_format={"type": "json_object"},
    )

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        # Return minimal valid structure
        result = {
            "package_overview": f"Experience an amazing {primary_keyword}.",
            "quick_facts": {
                "package_name": package_data.get("name", ""),
                "cost": package_data.get("cost", ""),
                "duration": package_data.get("duration", ""),
                "destination": package_data.get("destination", ""),
                "level": package_data.get("level", ""),
                "accommodation": package_data.get("accommodation", ""),
                "food": package_data.get("food", ""),
                "activities": package_data.get("activities", ""),
            },
            "why_choose_heading": "Why Choose This Package?",
            "why_choose_intro": "This package offers an unforgettable experience.",
            "why_choose_bullets": ["Expert guidance", "Beautiful location", "Comfortable stay", "Great food", "Affordable pricing"],
            "who_can_benefit_heading": "Who Can Benefit?",
            "who_can_benefit_intro": "Anyone seeking a meaningful travel experience.",
            "who_can_benefit_bullets": ["Solo travelers", "Couples", "Families", "Groups", "Corporate teams"],
            "program_highlights": {
                "heading": "Program Highlights",
                "morning": [{"time": "06:00 AM", "activity": "Morning session"}],
                "daytime": [{"time": "10:00 AM", "activity": "Day session"}],
                "evening": [{"time": "05:00 PM", "activity": "Evening session"}],
            },
            "meal_section_heading": "Meals",
            "meal_section_bullets": ["Healthy vegetarian food", "Fresh organic ingredients"],
            "accommodation_heading": "Accommodation",
            "accommodation_bullets": ["Clean comfortable rooms", "Modern amenities"],
            "benefits_heading": "Benefits",
            "benefits_items": ["Relaxation", "Wellness", "Peace", "Fitness", "Clarity", "Energy", "Balance", "Joy"],
            "how_to_book_heading": "How to Book",
            "how_to_book_steps": ["Choose dates", "Fill form", "Pay advance", "Get confirmation", "Arrive", "Enjoy"],
            "prices_photos_reviews": "Highly rated by guests.",
            "itinerary": [{"day_number": 1, "sessions": [{"time": "02:00 PM", "activity": "Check-in"}]}],
            "pricing_table": [{"guests": "1 Person", "cost_per_person": package_data.get("cost", "TBD")}],
            "inclusions": ["Accommodation", "Food", "Activities"],
            "exclusions": ["Travel", "Insurance", "Personal expenses"],
            "nearby_locations_heading": "Nearby",
            "nearby_locations": [{"name": "Airport", "distance": "20 km", "type": "airport"}],
            "cancellation_policy": "Contact us for cancellation details.",
            "payment_policy_bullets": ["30% advance", "Balance on arrival", "Online payments accepted"],
            "terms_conditions": ["Valid ID required", "Check-in at 2 PM"] + [""] * 11,
            "faq": [{"question": "What to bring?", "answer": "Comfortable clothes."}],
        }

    return result
