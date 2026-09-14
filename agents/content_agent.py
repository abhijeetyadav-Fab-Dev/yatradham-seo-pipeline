"""Content agent: generates all 19 structured sections from scraped page data."""
import json
import re
import logging
from typing import Dict, Any
from llm_client import LLMClient
from anti_ai_guardrails import de_slop_and_humanize, GOOGLE_HELPFUL_CONTENT_GUARDRAILS

logger = logging.getLogger("content_agent")


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
    cost = package_data.get('cost', '')
    url = package_data.get('url', '')
    category = package_data.get('category', 'auto')

    user_msg = f"""Generate all 19 sections for this package. EXTRACT real details from the raw text below.

Package Name: {name}
Category: {category}
URL: {url}
Destination: {destination}
Duration: {duration}
Starting Cost / Price: {cost}
Primary Keyword: {primary_keyword}


--- RAW PAGE TEXT (extract real pricing, activities, accommodation, meals, FAQs from this) ---
{raw_text}
-----------

IMPORTANT REMINDERS:
- Follow the domain rules for {category.upper()}: No Darshan/Aarti/cabs for Wellness Retreats, and no fake therapies for Pilgrimage Tours.
- For `package_overview`: Seamlessly integrate the retreat name and destination without awkward repetitive phrasing (e.g. NEVER write 'with the 7 Days at 7 Days' or repeat city names consecutively). Keep sentences crisp (12-18 words each), natural, and engaging.
- Extract ACTUAL pricing from the text (e.g. Rs., ₹, per person, per night).
- Extract ACTUAL destination city and state (not the package name).
- Extract ACTUAL accommodation type (ashram, resort, dharamshala, hotel).
- Extract ACTUAL meal type (Sattvik, vegetarian, Ayurvedic, organic).
- Output ONLY valid JSON."""



    try:
        content = client.chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=2200,
            temperature=0.5,
            response_format={"type": "json_object"},
        )
        result = _extract_json_from_response(content)
        # Ensure all required sections are non-empty
        required_fields = ["package_overview", "quick_facts", "why_choose_bullets", "inclusions", "exclusions", "faq"]
        if any(not result.get(f) for f in required_fields):
            fb = get_category_aware_fallback(package_data, primary_keyword)
            for f in required_fields:
                if not result.get(f):
                    result[f] = fb[f]
            if not (result.get("quick_facts") or {}).get("cost"):
                result["quick_facts"]["cost"] = fb["quick_facts"]["cost"]
            if not (result.get("quick_facts") or {}).get("destination"):
                result["quick_facts"]["destination"] = fb["quick_facts"]["destination"]
    except Exception as e:
        logger.warning(f"Content agent execution failed: {e}. Generating category-aware fallback.")
        result = get_category_aware_fallback(package_data, primary_keyword)

    return result


def get_category_aware_fallback(package_data: Dict[str, Any], primary_keyword: str = "") -> Dict[str, Any]:
    """Generates complete, enterprise-grade 19 sections strictly adhering to category domain rules."""
    name = package_data.get('name', 'Sacred Pilgrimage Service')
    destination = package_data.get('destination') or 'India'
    duration = package_data.get('duration') or '3 Days & 2 Nights'
    cost = package_data.get('cost') or 'Starting From ₹ Contact for Pricing'
    raw_text = package_data.get('raw_text', '')
    cat = (package_data.get('category') or 'tour').lower()

    if not cost or 'contact' in cost.lower() or 'null' in cost.lower():
        cost_match = re.search(r'(?:Rs\.?|INR|₹)\s*[\d,]+', raw_text)
        if cost_match:
            cost = f"Starting From ₹ {cost_match.group(0)}"

    if cat == 'puja':
        return {
            "package_overview": f"{name} in {destination} is a sacred Vedic ritual service conducted through YatraDham.Org. Performed by experienced temple priests according to authentic scriptures, this holy seva includes personalized gotra sankalp, sacred samagri, and divine blessings for spiritual well-being.",
            "quick_facts": {
                "package_name": name,
                "cost": cost,
                "duration": duration if duration and duration != 'Flexible Duration' else "As per ritual timings",
                "destination": destination,
                "level": "For all devotees and families",
                "accommodation": "Temple vicinity stay assistance available",
                "food": "Blessed Temple Prasad offerings",
                "activities": f"Vedic chanting, sankalp, havan, and {name} rituals",
                "center_name": package_data.get("center_name") or f"Verified Temple Trust ({destination})",
                "yoga_sessions": "Spiritual darshan and prayer"
            },
            "why_choose_heading": f"Why Book {name} Through YatraDham?",
            "why_choose_intro": "YatraDham.Org connects devotees with verified temple priests for authentic, transparent, and hassle-free puja ceremonies.",
            "why_choose_bullets": [
                f"Authentic Vedic rituals performed strictly according to traditional scriptures in {destination}.",
                "Experienced, verified temple pandits ensuring correct mantras, gotra sankalp, and procedures.",
                "Complete arrangement of pure puja samagri, fresh flowers, and sacred ritual essentials.",
                "Transparent dakshina and service charges with no hidden fees or middlemen.",
                "Dedicated YatraDham support coordinator assisting your pilgrimage and darshan arrangements.",
            ],
            "who_can_benefit_heading": "Who Can Participate in This Sacred Puja?",
            "who_can_benefit_intro": f"{name} is recommended for devotees seeking divine grace, overcoming obstacles, and commemorating auspicious family occasions.",
            "who_can_benefit_bullets": [
                "Devotees and families seeking divine blessings for health, prosperity, and peace of mind.",
                "Individuals performing dosha nivaran, birthday, wedding anniversary, or memorial rituals.",
                "Pilgrims visiting holy shrines who wish to perform pre-booked, hassle-free temple sevas.",
                "Devotees unable to travel physically who wish to perform sankalp puja remotely with prasad delivery.",
                "Anyone wishing to express gratitude and devotion through authentic Vedic ceremonies.",
            ],
            "program_highlights": {
                "heading": "Puja & Ritual Schedule",
                "morning": [{"time": "07:00 AM", "activity": "Priest meeting, gotra sankalp, and purification rituals"}, {"time": "08:30 AM", "activity": f"Main {name} recitation, mantra chanting, and sacred offerings"}],
                "daytime": [{"time": "11:00 AM", "activity": "Maha Aarti, purnahuti, and blessed prasad distribution"}, {"time": "12:30 PM", "activity": "Temple darshan and personal prayers"}],
                "evening": [{"time": "06:30 PM", "activity": "Evening temple aarti attendance and spiritual reflection"}],
            },
            "meal_section_heading": "Temple Prasad & Satvik Offerings",
            "meal_section_bullets": [
                "Sacred temple prasad prepared in accordance with traditional temple sanctum guidelines.",
                "Satvik meal arrangements and guidance available for participating devotees in the temple complex.",
            ],
            "accommodation_heading": "Pilgrim Accommodation in Temple Vicinity",
            "accommodation_bullets": [
                f"Comfortable, clean dharamshalas and ashram rooms available in {destination} through YatraDham.",
                "Conveniently located near the temple complex for easy morning and evening ritual access.",
            ],
            "benefits_heading": f"Spiritual Benefits of {name}",
            "benefits_items": [
                "Invokes divine grace and positive spiritual vibrations for personal and family harmony.",
                "Alleviates planetary doshas and negative influences through authentic scriptural remedies.",
                "Promotes mental tranquility, spiritual focus, and inner peace during your pilgrimage.",
                "Ensures traditional Vedic procedures are carried out with utmost devotion and purity.",
                "Preserves sacred family traditions and commemorates important life milestones authentically.",
                "Brings spiritual fulfillment through righteous temple seva and selfless prayer.",
                "Provides the comfort of having expert Vedic priests manage all ritual complexities.",
                "Connects devotees directly with the sacred spiritual heritage of ancient pilgrimage shrines.",
            ],
            "how_to_book_heading": "How to Book Puja Through YatraDham",
            "how_to_book_steps": [
                "Select your preferred date and ritual type on the YatraDham.Org puja portal.",
                "Provide your family details, gotra, and sankalp intentions during checkout.",
                "Confirm the booking through YatraDham's secure online payment gateway.",
                "Receive your instant booking voucher and priest contact details via SMS and email.",
                "Arrive at the temple counter or join remotely as per your selected service format.",
                "Receive blessed prasad and the completion certificate of your sacred puja.",
            ],
            "prices_photos_reviews": f"{name} seva starts from {cost}. Check YatraDham.Org for authentic devotee reviews, photos, and live ritual timings.",
            "itinerary": [
                {"day_number": 1, "sessions": [{"time": "07:00 AM", "activity": "Sankalp & purification"}, {"time": "08:30 AM", "activity": "Main Puja rituals"}, {"time": "11:30 AM", "activity": "Aarti and Prasad distribution"}]}
            ],
            "pricing_table": [
                {"guests": "Single Devotee", "cost_per_person": cost},
                {"guests": "Family Sankalp (Up to 4)", "cost_per_person": cost},
                {"guests": "Extended Group / Special Seva", "cost_per_person": "Contact YatraDham for custom arrangements"}
            ],
            "inclusions": [
                "Complete Vedic Pandit Ji dakshina and ritual coordination",
                "All essential sacred puja samagri, havan wood, and holy offerings",
                "Personalized gotra and family name sankalp during the ceremony",
                "Temple darshan guidance and queue assistance",
                "Sanctified temple prasad packaging for the devotee",
                "24/7 dedicated YatraDham pilgrimage support"
            ],
            "exclusions": [
                "Personal travel and transport to and from the temple complex",
                "Accommodation charges unless booked together in stay package",
                "Personal donations outside the fixed package inclusions",
                "Special gold or silver jewelry offerings at temple counter"
            ],
            "nearby_locations_heading": f"How to Reach {destination}",
            "nearby_locations": [
                {"name": "Nearest Major Railway Station", "distance": "Convenient access from city center", "type": "railway"},
                {"name": "Nearest Domestic / International Airport", "distance": "Connecting flights available", "type": "airport"}
            ],
            "cancellation_policy": "Puja bookings can be rescheduled up to 48 hours prior to the scheduled ritual time. For cancellation and refund requests, our YatraDham helpdesk is available 24/7 to assist you.",
            "payment_policy_bullets": [
                "Advance online payment required to reserve priest schedule and fresh samagri.",
                "All major UPI, credit/debit cards, and net banking accepted securely.",
                "Transparent pricing with no additional cash demands at the temple."
            ],
            "terms_conditions": [
                "Devotees are requested to maintain traditional Indian attire during sacred rituals.",
                "Please report to the temple designated spot 15 minutes before the scheduled time.",
                "Gotra and devotee names should be verified accurately during booking submission.",
                "Photography may be restricted inside the inner sanctum as per temple trust rules.",
                "Prasad for remote bookings will be dispatched via registered courier within 3 working days.",
                "Ritual timings may adjust slightly during major festivals and eclipses."
            ],
            "faq": [
                {"question": f"Can family members join the {name}?", "answer": "Yes. Family members are warmly welcome to participate together in the sankalp and rituals. You can provide names of all family members during booking."},
                {"question": "What items or samagri do I need to bring?", "answer": "All necessary ritual items, sacred herbs, gangajal, and samagri are completely arranged by the pandit ji through YatraDham. You only need to bring devotion and traditional attire."},
                {"question": "What is the recommended dress code?", "answer": "Traditional Indian attire is recommended (dhoti/kurta for men and saree/salwar suit for women). Leather items are strictly prohibited inside the temple premises."},
                {"question": "How do I receive the prasad?", "answer": "Attending devotees receive the blessed prasad immediately following the aarti. For devotees booking remote puja, sanctified dry prasad is packaged and dispatched via courier."}
            ]
        }
    elif cat == 'stay':
        return {
            "package_overview": f"{name} provides clean, verified, and peaceful accommodation in {destination} through YatraDham.Org. Located conveniently near major shrines and transport hubs, this property offers pilgrims secure rooms, courteous service, and essential amenities for a restful spiritual stay.",
            "quick_facts": {
                "package_name": name,
                "cost": cost,
                "duration": duration if duration and duration != 'Flexible Duration' else "Per Night Booking",
                "destination": destination,
                "level": "Family & Pilgrim Friendly",
                "accommodation": "Clean AC & Non-AC rooms with attached bath",
                "food": "Satvik vegetarian food available nearby",
                "activities": "Temple darshan assistance, morning/evening prayers",
                "center_name": name,
                "yoga_sessions": "Spiritual prayer hall available"
            },
            "why_choose_heading": f"Why Stay at {name}?",
            "why_choose_intro": "Book your stay with peace of mind through YatraDham.Org, ensuring verified property standards and honest pricing.",
            "why_choose_bullets": [
                f"Prime location in {destination} with easy transit access to revered pilgrimage temples.",
                "Verified hygiene and sanitation standards with clean bed linen and purified drinking water.",
                "Secure, family-friendly atmosphere suitable for elderly pilgrims, children, and groups.",
                "Affordable and transparent tariff with no hidden surcharges at reception check-in.",
                "Prompt customer support from YatraDham to assist with booking modifications and pilgrimage guidance.",
            ],
            "who_can_benefit_heading": "Who Can Benefit From Staying Here?",
            "who_can_benefit_intro": f"{name} is ideal for pilgrims, families, and travel groups seeking reliable, comfortable lodging in {destination}.",
            "who_can_benefit_bullets": [
                "Pilgrims visiting sacred shrines who prioritize cleanliness, safety, and proximity to temples.",
                "Families traveling with senior citizens who require elevator access and ground-floor amenities.",
                "Devotional groups and bhajan mandalis requiring multi-bed rooms and dormitories.",
                "Solo travelers and spiritual seekers looking for peaceful, alcohol-free, and satvik environments.",
                "Budget-conscious travelers seeking maximum value with verified authentic booking vouchers.",
            ],
            "program_highlights": {
                "heading": "Stay & Pilgrimage Schedule",
                "morning": [{"time": "06:00 AM", "activity": "Morning temple aarti access and fresh breakfast"}, {"time": "08:00 AM", "activity": "Temple darshan and local sacred sightseeing"}],
                "daytime": [{"time": "01:00 PM", "activity": "Satvik lunch and afternoon rest at property"}, {"time": "04:00 PM", "activity": "Local pilgrimage shopping and heritage walk"}],
                "evening": [{"time": "07:00 PM", "activity": "Evening temple darshan, dinner, and restful night"}],
            },
            "meal_section_heading": "Dining & Satvik Food Options",
            "meal_section_bullets": [
                "Pure vegetarian satvik food options available either in-house or within immediate walking distance.",
                "Clean dining environment respecting traditional dietary values without onion and garlic on request.",
            ],
            "accommodation_heading": "Room Amenities & Facilities",
            "accommodation_bullets": [
                f"Well-maintained rooms with comfortable beds, fresh linen, and attached bathrooms in {destination}.",
                "Hot water geyser facility, 24-hour water supply, and clean room maintenance.",
            ],
            "benefits_heading": f"Key Benefits of Booking {name}",
            "benefits_items": [
                "Convenient walking or short auto-rickshaw distance to central temples and bathing ghats.",
                "Guaranteed room reservation with pre-paid YatraDham confirmation voucher.",
                "Pure satvik, alcohol-free, and smoke-free spiritual environment throughout the premises.",
                "Helpful local desk staff assisting with local auto tariffs and temple opening timings.",
                "Peace of mind knowing your booking is supported by India's trusted pilgrimage platform.",
                "Safety for solo women travelers and elderly family members.",
                "Clean western and Indian style restrooms with daily housekeeping.",
                "Luggage storage facility for pilgrims arriving before standard check-in time.",
            ],
            "how_to_book_heading": "How to Book Room Through YatraDham",
            "how_to_book_steps": [
                "Select your check-in and check-out dates on YatraDham.Org.",
                "Choose your preferred room type (AC, Non-AC, or Family Suite).",
                "Enter guest details and any special accessibility requirements.",
                "Complete the instant advance payment via our secure payment gateway.",
                "Download your confirmed booking voucher with complete property address and map link.",
                "Present your voucher and photo ID at reception for swift check-in.",
            ],
            "prices_photos_reviews": f"{name} room rates start from {cost}. Check YatraDham.Org for guest photos, verified reviews, and availability.",
            "itinerary": [
                {"day_number": 1, "sessions": [{"time": "12:00 PM", "activity": "Standard check-in and room allocation"}, {"time": "06:00 PM", "activity": "Evening temple darshan"}, {"time": "10:00 AM", "activity": "Check-out on departure day"}]}
            ],
            "pricing_table": [
                {"guests": "Double Bed Room (2 Guests)", "cost_per_person": cost},
                {"guests": "Triple Bed Room (3 Guests)", "cost_per_person": cost},
                {"guests": "Family Suite (4-6 Guests)", "cost_per_person": "Contact YatraDham for family room rates"}
            ],
            "inclusions": [
                "Room accommodation with attached bathroom",
                "24-hour clean water supply and hot water facilities",
                "Daily housekeeping and fresh bed linen",
                "Reception assistance for pilgrimage guidance and transport",
                "YatraDham confirmed booking guarantee and support"
            ],
            "exclusions": [
                "Personal laundry and room service orders",
                "Temple entrance passes and VIP darshan tickets",
                "Cab and transport services unless specifically arranged",
                "Early check-in and late check-out outside standard policy"
            ],
            "nearby_locations_heading": f"Key Landmarks in {destination}",
            "nearby_locations": [
                {"name": "Central Pilgrimage Temple", "distance": "Within 5-15 mins walking distance", "type": "sightseeing"},
                {"name": "Local Bus Stand / Auto Stand", "distance": "Quick transit access", "type": "bus"}
            ],
            "cancellation_policy": "Cancellations made 72 hours prior to check-in date are eligible for refund per property terms. Contact YatraDham customer care for immediate booking modifications.",
            "payment_policy_bullets": [
                "Advance online payment required to secure confirmed room allocation.",
                "Standard check-in requires government-issued photo ID for all adult guests.",
                "Transparent tariff with no unexpected service surcharges."
            ],
            "terms_conditions": [
                "Valid Aadhaar card, Passport, or Voter ID required for all staying guests.",
                "Standard check-in time is 12:00 PM and check-out time is 10:00 AM.",
                "Consumption of alcohol, smoking, and non-vegetarian food is strictly prohibited.",
                "Unmarried couples may not be permitted as per traditional trust policy.",
                "Extra mattress available upon request with nominal additional charges.",
                "Management reserves right of admission to maintain peaceful devotional atmosphere."
            ],
            "faq": [
                {"question": "What are the standard check-in and check-out times?", "answer": "Standard check-in is usually 12:00 PM and check-out is 10:00 AM. If you arrive early, the property staff can safely store your luggage while you visit the temple."},
                {"question": "Is hot water available in the rooms?", "answer": "Yes, rooms are equipped with geysers or scheduled solar hot water supply for morning bath."},
                {"question": "Are pure vegetarian meals available?", "answer": "Yes, pure satvik vegetarian dining is readily accessible either in-house or in the immediate surroundings of the property."},
                {"question": "How close is the property to the main temple?", "answer": f"The property is conveniently situated in {destination} to allow quick and easy walking or short auto-rickshaw access to the main temple complex."}
            ]
        }
    elif cat == 'tour':
        return {
            "package_overview": f"{name} is a comprehensive {duration} pilgrimage tour across {destination} organized by YatraDham.Org. Designed for devotees and families, this package features verified hotel accommodation, satvik vegetarian meals, comfortable vehicle transfers, and expert coordination for a spiritually uplifting yatra.",
            "quick_facts": {
                "package_name": name,
                "cost": cost,
                "duration": duration,
                "destination": destination,
                "level": "All age groups welcome",
                "accommodation": "Verified hotel & dharamshala stays",
                "food": "Satvik vegetarian meals included",
                "activities": "Temple darshan, scenic transfer, holy dip, aarti",
                "center_name": "YatraDham Tour Operations",
                "yoga_sessions": "Morning prayer and meditation"
            },
            "why_choose_heading": f"Why Choose {name}?",
            "why_choose_intro": "Experience a seamless sacred journey with verified logistics, experienced drivers, and dedicated pilgrimage coordinators.",
            "why_choose_bullets": [
                f"Carefully curated {duration} itinerary maximizing spiritual darshan across {destination}.",
                "Clean, comfortable accommodation pre-booked at verified pilgrimage hotels and dharamshalas.",
                "Reliable, sanitized vehicles with experienced mountain and highway drivers.",
                "Nutritious pure vegetarian meals provided throughout the pilgrimage route.",
                "Continuous on-ground and telephonic support from YatraDham's pilgrimage assistance desk.",
            ],
            "who_can_benefit_heading": "Who Can Join This Yatra?",
            "who_can_benefit_intro": f"This yatra is tailored for families, seniors, and groups seeking a safe, well-managed spiritual pilgrimage.",
            "who_can_benefit_bullets": [
                "Families with elderly parents looking for comfortable transport and paced travel.",
                "Devotees undertaking sacred yatra who prefer pre-arranged logistics over stressful on-the-spot negotiations.",
                "Pilgrims seeking authentic satvik dining and verified safe accommodations.",
                "First-time visitors to holy shrines who benefit from guided itinerary planning.",
                "Devotional groups wishing to travel together with unified transport and lodging.",
            ],
            "program_highlights": {
                "heading": "Yatra Itinerary Highlights",
                "morning": [{"time": "06:00 AM", "activity": "Morning departure and scenic pilgrimage journey"}, {"time": "09:00 AM", "activity": "Breakfast stop at verified satvik restaurant"}],
                "daytime": [{"time": "01:00 PM", "activity": "Arrival at holy destination, hotel check-in, and lunch"}, {"time": "03:30 PM", "activity": "Temple visit and sacred kund darshan"}],
                "evening": [{"time": "06:30 PM", "activity": "Evening temple aarti and restful overnight stay"}],
            },
            "meal_section_heading": "Satvik Meals on the Yatra",
            "meal_section_bullets": [
                "Fresh, hygienic vegetarian breakfast and meals served at clean en-route stops.",
                "Nutritious satvik menu designed to keep pilgrims energized and refreshed during travel.",
            ],
            "accommodation_heading": "Verified En-Route Stays",
            "accommodation_bullets": [
                f"Comfortable hotel and dharamshala rooms in {destination} inspected by YatraDham.",
                "Equipped with hot water, clean bedding, and private attached washrooms.",
            ],
            "benefits_heading": f"Key Benefits of {name}",
            "benefits_items": [
                "Stress-free pilgrimage with vehicle, fuel, driver allowances, and tolls fully covered.",
                "Experienced drivers well-versed with regional pilgrimage roads and safety standards.",
                "Priority guidance for temple opening timings, aarti schedules, and puja passes.",
                "Balanced travel pace ensuring adequate rest and spiritual contemplation.",
                "Assistance with elderly family members and special pilgrimage requirements.",
                "Comprehensive coverage of major and secondary holy spots along the route.",
                "Transparent billing with guaranteed departure schedules.",
                "Memorable devotional bonding experience for your entire family.",
            ],
            "how_to_book_heading": "How to Book Your Yatra",
            "how_to_book_steps": [
                "Select your preferred yatra departure date on YatraDham.Org.",
                "Choose your vehicle type (Sedan, Innova, Tempo Traveller, or Bus).",
                "Enter number of passengers and room occupancy preferences.",
                "Pay the advance confirmation deposit via our secure payment gateway.",
                "Receive your detailed day-wise itinerary, driver contact, and stay vouchers.",
                "Embark on your sacred pilgrimage journey with total peace of mind.",
            ],
            "prices_photos_reviews": f"{name} packages start from {cost}. Check YatraDham.Org for traveler reviews, itinerary details, and photos.",
            "itinerary": [
                {"day_number": 1, "sessions": [{"time": "07:00 AM", "activity": "Departure from pickup hub"}, {"time": "01:00 PM", "activity": "Check-in and lunch"}, {"time": "05:00 PM", "activity": "Evening temple darshan and aarti"}]}
            ],
            "pricing_table": [
                {"guests": "Twin Sharing (Per Person)", "cost_per_person": cost},
                {"guests": "Triple Sharing (Per Person)", "cost_per_person": cost},
                {"guests": "Child With Bed", "cost_per_person": "Contact YatraDham for family discount"}
            ],
            "inclusions": [
                f"Accommodation for {duration} in verified pilgrimage hotels and dharamshalas",
                "Daily vegetarian breakfast and satvik dining as per itinerary",
                "Dedicated sanitized vehicle for transfers and sightseeing",
                "Toll tax, parking fees, driver allowance, and state road taxes",
                "Assistance at temple complexes and major sacred checkpoints",
                "24/7 dedicated YatraDham pilgrimage coordinator support"
            ],
            "exclusions": [
                "Train or flight tickets to initial boarding point",
                "Personal pony, doli, helicopter, or porter charges",
                "Special VIP darshan tickets and personal puja charges",
                "Personal expenses, laundry, and telephone calls"
            ],
            "nearby_locations_heading": f"Transit Hubs for {destination}",
            "nearby_locations": [
                {"name": "Major Pickup Hub / Railway Junction", "distance": "Designated meeting point", "type": "railway"},
                {"name": "Regional Airport", "distance": "Direct cab transfer available", "type": "airport"}
            ],
            "cancellation_policy": "Yatra packages can be cancelled with partial refund up to 15 days prior to travel date. Rescheduling requests are handled on priority basis by YatraDham tour desk.",
            "payment_policy_bullets": [
                "30% advance deposit to secure vehicle and hotel reservations.",
                "Balance amount payable 7 days prior to departure or at check-in.",
                "Multiple secure online payment methods supported."
            ],
            "terms_conditions": [
                "All travelers must carry valid government photo identification.",
                "Itinerary may adjust in case of natural roadblocks or weather disruptions.",
                "AC will be switched off in mountain climbing sections for vehicle safety.",
                "Consumption of alcohol and non-vegetarian food is strictly forbidden during yatra.",
                "Luggage allowance as per vehicle trunk capacity.",
                "Devotees are advised to carry adequate personal medicines and warm clothing."
            ],
            "faq": [
                {"question": "Is this yatra suitable for senior citizens?", "answer": "Yes. The itinerary is designed with comfortable driving breaks, moderate walking distances, and clean rests to accommodate senior citizens comfortably."},
                {"question": "What type of vehicles are provided?", "answer": "Depending on your group size, we provide well-maintained commercial vehicles such as Dzire, Innova Crysta, or Tempo Travellers with experienced drivers."},
                {"question": "Are meals pure vegetarian?", "answer": "Yes, all included meals are strictly 100% pure vegetarian, prepared hygienically in satvik pilgrim restaurants."},
                {"question": "How are temple darshans coordinated?", "answer": "Our driver and local coordinators guide you on the best darshan timings, ticket counters, and route navigation to minimize waiting times."}
            ]
        }
    else:  # wellness
        return {
            "package_overview": f"{name} is a {duration} wellness retreat in {destination} offered through YatraDham.Org. Designed for holistic rejuvenation, this program integrates authentic Ayurvedic therapies, guided yoga and meditation, and nutritious satvik meals in a tranquil natural sanctuary.",
            "quick_facts": {
                "package_name": name,
                "cost": cost,
                "duration": duration,
                "destination": destination,
                "level": "All experience levels welcome",
                "accommodation": "Verified wellness resort stay through YatraDham",
                "food": "Custom Ayurvedic satvik meals included",
                "activities": f"Yoga, meditation, and therapies as per {name} schedule",
                "center_name": package_data.get("center_name") or f"Verified Wellness Center ({destination})",
                "yoga_sessions": "Daily morning & evening sessions"
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
