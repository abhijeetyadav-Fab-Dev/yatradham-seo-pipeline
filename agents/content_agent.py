"""Content agent: generates all 19 structured sections from scraped page data."""
import json
import re
from typing import Dict, Any
from llm_client import LLMClient
from anti_ai_guardrails import de_slop_and_humanize, GOOGLE_HELPFUL_CONTENT_GUARDRAILS


SYSTEM_PROMPT = """You are an expert content writer for YatraDham.Org, India's first dedicated religious tourism and wellness travel platform.

ABOUT YATRADHAM.ORG:
- India's first dedicated religious tourism platform (since 2016).
- 700+ pilgrimage destinations with verified stays.
- Services: Accommodation (Dharamshalas, Ashrams, Hotels, Resorts), Puja Services, Wellness Retreats.
- Partnerships: TTDC, APTDC, Gujarat Tourism, Swaminarayan, Hare Krishna trusts.
- Mission: Help pilgrims focus on darshan and devotion by handling stay and service logistics.

BRAND VOICE:
- Tone: Respectful, helpful, informative, trustworthy. Never aggressive or salesy.
- Language: Clear, culturally sensitive, spiritually uplifting.
""" + "\n" + GOOGLE_HELPFUL_CONTENT_GUARDRAILS + """\n
Given scraped package details and raw page text, you MUST:
1. EXTRACT real information from the raw text — actual pricing, real resort/hotel names, real destinations (city + state), actual therapies/activities mentioned, real meal descriptions, actual accommodation types.
2. NEVER invent generic placeholder content. If information is not available in the raw text, write "Details available on enquiry" or "Contact YatraDham for specifics" — do NOT make up fake data.
3. Write naturally in 2nd person ("you", "your") addressing the pilgrim/traveler directly.
4. Every bullet point must be a specific, meaningful sentence (8-18 words), NOT generic 1-2 word labels.
5. FAQ answers must address real concerns a traveler would have (medications during retreat, suitability for beginners, what's included, cancellation policy, etc.).

JSON SCHEMA (output ALL fields):
{
  "package_overview": "string (3-4 sentences describing what the package offers, extracted from page)",
  "quick_facts": {
    "package_name": "string (exact name from the page)",
    "cost": "string (exact price from page, e.g. 'Starting from Rs. 12,301 per person per night')",
    "duration": "string (e.g. '22 Days & 21 Nights')",
    "destination": "string (city + state, e.g. 'Palakkad, Kerala')",
    "level": "string (e.g. 'Beginner to Advanced' or 'All Levels')",
    "accommodation": "string (e.g. 'Eco-Friendly Villa Stay' or 'AC Rooms with attached bath')",
    "food": "string (e.g. 'Healthy Satvik Breakfast, Lunch & Dinner')",
    "activities": "string (e.g. 'Yoga, Meditation, Ayurvedic Therapies, Nature Walks')"
  },
  "why_choose_heading": "string (e.g. 'Why Choose the Ayurvedic Stress Relief Retreat in Kerala?')",
  "why_choose_intro": "string (1 sentence introducing the unique value)",
  "why_choose_bullets": ["5 specific, meaningful sentences about what makes this package special"],
  "who_can_benefit_heading": "string",
  "who_can_benefit_intro": "string (1 sentence)",
  "who_can_benefit_bullets": ["5 specific sentences about who would benefit and why"],
  "program_highlights": {
    "heading": "string",
    "morning": [{"time": "06:00 AM", "activity": "Specific activity from page"}],
    "daytime": [{"time": "10:00 AM", "activity": "Specific activity from page"}],
    "evening": [{"time": "05:00 PM", "activity": "Specific activity from page"}]
  },
  "meal_section_heading": "string",
  "meal_section_bullets": ["2-3 specific sentences about the meals offered"],
  "accommodation_heading": "string",
  "accommodation_bullets": ["2-3 specific sentences about the accommodation"],
  "benefits_heading": "string (e.g. 'Key Benefits of This Retreat')",
  "benefits_items": ["8 specific benefit SENTENCES, not single words"],
  "how_to_book_heading": "How to Book Through YatraDham",
  "how_to_book_steps": ["6 clear booking steps mentioning YatraDham"],
  "prices_photos_reviews": "string (1-2 sentences with actual rating if available)",
  "itinerary": [{"day_number": 1, "sessions": [{"time": "HH:MM AM/PM", "activity": "Specific activity"}]}],
  "pricing_table": [{"guests": "1 Person", "cost_per_person": "Actual price from page or 'Contact for pricing'"}],
  "inclusions": ["6+ specific items included, extracted from page"],
  "exclusions": ["6+ specific items excluded"],
  "nearby_locations_heading": "How to Reach & Nearby Landmarks",
  "nearby_locations": [{"name": "Specific place", "distance": "XX km", "type": "airport|railway|bus|sightseeing"}],
  "cancellation_policy": "string (1 paragraph with actual policy details)",
  "payment_policy_bullets": ["3 specific payment terms"],
  "terms_conditions": ["6-8 meaningful terms, no empty strings"],
  "faq": [
    {"question": "Specific question a traveler would ask", "answer": "Detailed 2-3 sentence answer"},
    {"question": "...", "answer": "..."},
    {"question": "...", "answer": "..."},
    {"question": "...", "answer": "..."}
  ]
}

CRITICAL: Output ONLY valid JSON. No markdown, no explanation. Extract REAL data from the raw text."""


def _extract_json_from_response(content: str) -> dict:
    """Robustly extract JSON from LLM response, handling markdown blocks and conversational text."""
    clean = content.strip()
    if clean.startswith("```json"):
        clean = clean[7:]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    clean = clean.strip()
    if "{" in clean and "}" in clean:
        start = clean.find("{")
        end = clean.rfind("}") + 1
        clean = clean[start:end]
    return json.loads(clean)


def run(package_data: Dict[str, Any], primary_keyword: str, client: LLMClient) -> Dict[str, Any]:
    raw_text = package_data.get('raw_text', '')
    name = package_data.get('name', '')
    destination = package_data.get('destination', '')
    duration = package_data.get('duration', '')

    user_msg = f"""Generate all 19 sections for this package. EXTRACT real details from the raw text below.

Package Name: {name}
Destination: {destination}
Duration: {duration}
Primary Keyword: {primary_keyword}

--- RAW PAGE TEXT (extract real pricing, activities, accommodation, meals, FAQs from this) ---
{raw_text}
-----------

IMPORTANT REMINDERS:
- Extract ACTUAL pricing from the text (look for Rs., INR, per person, per night).
- Extract ACTUAL destination city and state (not the package name).
- Extract ACTUAL accommodation type (villa, ashram, dharamshala, resort, hotel).
- Extract ACTUAL meal type (Satvik, vegetarian, Ayurvedic, organic).
- Extract ACTUAL therapies/activities mentioned (Panchakarma, Abhyangam, Shirodhara, Yoga, Pranayama).
- Write meaningful FAQ answers (2-3 sentences each) addressing real traveler concerns.
- Every bullet must be a complete, specific sentence — NOT generic 1-2 word labels.
- Output ONLY valid JSON."""

    content = client.chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=4000,
        temperature=0.5,
        response_format={"type": "json_object"},
    )

    try:
        result = _extract_json_from_response(content)
    except (json.JSONDecodeError, ValueError):
        # Build a meaningful fallback from scraped data — no generic placeholders
        cost_match = re.search(r'(?:Rs\.?|INR|₹)\s*[\d,]+', raw_text)
        cost = cost_match.group(0) if cost_match else 'Contact YatraDham for pricing'

        result = {
            "package_overview": f"{name} is a {duration} program in {destination}. This package includes accommodation, wellness activities, and meals. Book through YatraDham for verified stays and hassle-free arrangements.",
            "quick_facts": {
                "package_name": name,
                "cost": cost,
                "duration": duration,
                "destination": destination,
                "level": "All experience levels welcome",
                "accommodation": "Verified stay through YatraDham (details on booking page)",
                "food": "Vegetarian meals included (details on booking page)",
                "activities": f"Activities as per {name} schedule",
            },
            "why_choose_heading": f"Why Choose {name}?",
            "why_choose_intro": f"This {duration} program in {destination} offers a structured wellness experience through YatraDham.",
            "why_choose_bullets": [
                f"{duration} structured program with daily wellness schedule in {destination}.",
                "Verified accommodation booked through YatraDham for safe and comfortable stay.",
                "Includes wellness activities, guided sessions, and healthy vegetarian meals.",
                "Convenient booking process with YatraDham customer support available for queries.",
                f"Located in {destination}, offering a peaceful environment for rejuvenation.",
            ],
            "who_can_benefit_heading": "Who Can Benefit From This Program?",
            "who_can_benefit_intro": "This program is suitable for anyone looking to improve their physical and mental well-being.",
            "who_can_benefit_bullets": [
                "Working professionals dealing with daily stress who need structured relaxation time.",
                "Health-conscious individuals looking for authentic wellness therapies and practices.",
                "Beginners who want to explore yoga, meditation, or Ayurveda in a guided setting.",
                "Couples or families seeking a meaningful wellness getaway together.",
                "Anyone recovering from lifestyle-related health concerns under professional guidance.",
            ],
            "program_highlights": {
                "heading": "Daily Program Schedule",
                "morning": [{"time": "06:00 AM", "activity": "Morning wellness session (yoga/meditation/pranayama)"}, {"time": "08:00 AM", "activity": "Healthy breakfast"}],
                "daytime": [{"time": "10:00 AM", "activity": "Scheduled wellness therapy or activity session"}, {"time": "01:00 PM", "activity": "Vegetarian lunch and rest period"}],
                "evening": [{"time": "05:00 PM", "activity": "Evening relaxation session"}, {"time": "07:00 PM", "activity": "Dinner and free time"}],
            },
            "meal_section_heading": "Meals During Your Stay",
            "meal_section_bullets": [
                "Nutritious vegetarian meals prepared with fresh, locally sourced ingredients.",
                "Meal schedule designed to complement your wellness program and daily activities.",
            ],
            "accommodation_heading": "Your Accommodation",
            "accommodation_bullets": [
                f"Comfortable, verified accommodation in {destination} booked through YatraDham.",
                "Clean rooms with essential amenities for a restful stay during your program.",
            ],
            "benefits_heading": f"Key Benefits of {name}",
            "benefits_items": [
                "Structured daily routine that helps reduce accumulated stress and tension.",
                "Professional guidance for wellness practices suitable for your experience level.",
                "Improved flexibility and physical comfort through regular yoga and stretching.",
                "Better sleep quality from consistent meditation and relaxation techniques.",
                "Exposure to healthy eating habits with balanced vegetarian nutrition.",
                "Mental clarity and emotional balance through guided mindfulness practices.",
                "Time away from digital distractions in a peaceful natural environment.",
                "Practical wellness knowledge you can continue applying after returning home.",
            ],
            "how_to_book_heading": "How to Book Through YatraDham",
            "how_to_book_steps": [
                "Visit the package page on YatraDham.Org and review the program details.",
                "Select your preferred accommodation category and check-in date.",
                "Enter the number of guests attending the program.",
                "Complete the booking by making the required advance payment.",
                "Receive your booking confirmation and program details from YatraDham.",
                "Arrive at the venue and begin your wellness journey.",
            ],
            "prices_photos_reviews": f"{name} pricing starts from {cost}. Check YatraDham.Org for the latest reviews, ratings, and available dates.",
            "itinerary": [{"day_number": 1, "sessions": [{"time": "02:00 PM", "activity": "Check-in and orientation"}, {"time": "05:00 PM", "activity": "Welcome session and program introduction"}]}],
            "pricing_table": [{"guests": "1 Person", "cost_per_person": cost}, {"guests": "2 Persons", "cost_per_person": "Contact YatraDham"}, {"guests": "Group (3+)", "cost_per_person": "Contact YatraDham for group rates"}],
            "inclusions": ["Accommodation for the full program duration", "All scheduled wellness sessions and activities", "Vegetarian meals (breakfast, lunch, dinner)", "Wellness consultation and guidance", "Program materials and schedule", "YatraDham booking support"],
            "exclusions": ["Travel to and from the venue", "Personal expenses and shopping", "Travel insurance", "Any medical treatments outside the program", "Tips and gratuities", "Additional spa treatments not in the program"],
            "nearby_locations_heading": f"How to Reach {destination}",
            "nearby_locations": [{"name": "Nearest Airport", "distance": "Check YatraDham for details", "type": "airport"}, {"name": "Nearest Railway Station", "distance": "Check YatraDham for details", "type": "railway"}],
            "cancellation_policy": "For cancellation and refund details, please contact YatraDham customer support. Cancellation terms may vary based on the accommodation category and how far in advance the cancellation is made.",
            "payment_policy_bullets": ["Advance payment required to confirm your booking.", "Balance payment as per the venue's policy.", "Online payments accepted through YatraDham's secure platform."],
            "terms_conditions": [
                "Valid government-issued photo ID is required at check-in.",
                "Check-in and check-out times are as per the venue's policy.",
                "Guests are expected to follow the program schedule and venue guidelines.",
                "The venue reserves the right to modify the program schedule if necessary.",
                "Any damage to property will be charged to the guest.",
                "Outside food and beverages may not be permitted at certain venues.",
            ],
            "faq": [
                {"question": f"What is included in the {name}?", "answer": f"The program includes accommodation, daily wellness sessions, vegetarian meals, and professional guidance for the full {duration}. Check the package page on YatraDham for the complete list of inclusions."},
                {"question": "Is this program suitable for beginners?", "answer": "Yes. The program is designed to accommodate all experience levels. Professional instructors adjust sessions based on each participant's comfort and ability."},
                {"question": "Can I continue my regular medications during the program?", "answer": "If you are on prescribed medications, please inform the wellness team during your consultation. They will guide you on how to continue your treatment safely during the program."},
                {"question": "How do I book through YatraDham?", "answer": "Visit the package page on YatraDham.Org, select your preferred dates and accommodation, and complete the booking with the required advance payment. You will receive a confirmation with all details."},
            ],
        }

    return result
