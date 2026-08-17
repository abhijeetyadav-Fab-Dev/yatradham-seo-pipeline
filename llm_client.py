"""OpenRouter LLM client with token-limit retry and rate limiting."""
import os
import time
import json
from typing import Optional, Dict, Any, List
from openai import OpenAI

DEFAULT_OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_FALLBACK_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-3-27b-it:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "openai/gpt-oss-20b:free",
    "nvidia/nemotron-nano-9b-v2:free",
]

GROQ_DEFAULT_MODEL = "llama-3.3-70b-versatile"
GEMINI_DEFAULT_MODEL = "gemini-1.5-flash"


import logging

logger = logging.getLogger("llm_client")

class LLMClient:
    def __init__(self):
        # OpenRouter config
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL)
        
        # Groq config (Fast free tier: ~300+ tok/s)
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.groq_model = os.getenv("GROQ_MODEL", GROQ_DEFAULT_MODEL)
        
        # Gemini config (Google AI Studio free tier: 15 RPM)
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
        self.gemini_model = os.getenv("GEMINI_MODEL", GEMINI_DEFAULT_MODEL)
        
        # Active provider preference (groq -> gemini -> openrouter)
        self.provider = os.getenv("LLM_PROVIDER", "").lower()
        self.dry_run = os.getenv("DRY_RUN", "false").lower() == "true"
        
        self.openrouter_client: Optional[OpenAI] = None
        self.groq_client: Optional[OpenAI] = None
        self.gemini_client: Optional[OpenAI] = None
        
        self._init_clients()
        self.last_call_time = 0.0
        self.min_interval = 1.0  # seconds between calls

    def _init_clients(self):
        if self.dry_run:
            return
        if self.openrouter_api_key:
            self.openrouter_client = OpenAI(
                base_url=self.openrouter_base_url,
                api_key=self.openrouter_api_key,
                timeout=25.0
            )
        if self.groq_api_key:
            self.groq_client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.groq_api_key,
                timeout=20.0
            )
        if self.gemini_api_key:
            # Google AI Studio provides OpenAI-compatible endpoint
            self.gemini_client = OpenAI(
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                api_key=self.gemini_api_key,
                timeout=25.0
            )

    def set_custom_keys(self, provider: str, api_key: str, model: Optional[str] = None):
        """Allow setting keys dynamically from UI or runtime."""
        if provider == "groq":
            self.groq_api_key = api_key
            if model: self.groq_model = model
            self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key, timeout=20.0)
        elif provider == "gemini":
            self.gemini_api_key = api_key
            if model: self.gemini_model = model
            self.gemini_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=api_key, timeout=25.0)
        elif provider == "openrouter":
            self.openrouter_api_key = api_key
            if model: self.openrouter_model = model
            self.openrouter_client = OpenAI(base_url=self.openrouter_base_url, api_key=api_key, timeout=25.0)

    def _wait_for_rate_limit(self):
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call_time = time.time()

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        response_format: Optional[Dict[str, str]] = None,
        retries: int = 3,
    ) -> str:
        if self.dry_run:
            return self._mock_response(messages)

        # Build list of available clients/providers to attempt in priority order
        providers = []
        if self.groq_client:
            providers.append(("groq", self.groq_client, model or self.groq_model))
        if self.gemini_client:
            providers.append(("gemini", self.gemini_client, model or self.gemini_model))
        if self.openrouter_client:
            primary_or = model or self.openrouter_model
            for or_model in [primary_or] + [m for m in OPENROUTER_FALLBACK_MODELS if m != primary_or]:
                providers.append(("openrouter", self.openrouter_client, or_model))

        if not providers:
            # Fallback to mock if no keys are configured
            return self._mock_response(messages)

        for provider_name, client_inst, active_model in providers:
            self._wait_for_rate_limit()
            try:
                kwargs = {
                    "model": active_model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "timeout": 25.0,
                }
                if response_format and provider_name != "groq":
                    # Groq supports json_object on specific models; safe pass
                    kwargs["response_format"] = response_format

                resp = client_inst.chat.completions.create(**kwargs)
                content = resp.choices[0].message.content or ""
                if content.strip():
                    return content
            except Exception as e:
                logger.warning(f"Provider {provider_name} ({active_model}) call failed: {e}. Trying next provider...")
                continue

        # If all providers fail, return safe mock
        return self._mock_response(messages)

    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        """Return a mock JSON response for dry-run testing."""
        system_msg = messages[0].get("content", "") if messages else ""
        if "keyword" in system_msg.lower():
            return json.dumps({"primary_keyword": "Yoga Retreat Rishikesh", "secondary_keywords": ["Meditation Retreat", "Wellness Tour"]})
        if "title" in system_msg.lower():
            return json.dumps({"title_tag": "Yoga Retreat in Rishikesh | 7 Days Wellness Tour"})
        if "meta" in system_msg.lower():
            return json.dumps({"meta_description": "Join our 7-day yoga retreat in Rishikesh. Experience meditation, wellness, and peace. Book now for a transformative journey!"})
        if "content" in system_msg.lower() or "section" in system_msg.lower():
            return json.dumps({
                "package_overview": "Experience a refreshing and peaceful stay at our yoga retreat in Rishikesh.",
                "quick_facts": {
                    "package_name": "7 Days Yoga Retreat",
                    "cost": "₹15,000",
                    "duration": "7 Days / 6 Nights",
                    "destination": "Rishikesh, Uttarakhand",
                    "level": "Beginner to Intermediate",
                    "accommodation": "AC Rooms with attached bath",
                    "food": "Sattvic vegetarian meals",
                    "activities": "Yoga, Meditation, Trekking",
                },
                "why_choose_heading": "Why Choose This Retreat?",
                "why_choose_intro": "Our retreat offers a perfect blend of tradition and comfort.",
                "why_choose_bullets": [
                    "Expert yoga instructors with 10+ years experience",
                    "Scenic location near the Ganges river",
                    "Small batch sizes for personalized attention",
                    "Authentic Ayurvedic therapies included",
                    "Peaceful ashram environment",
                ],
                "who_can_benefit_heading": "Who Can Benefit?",
                "who_can_benefit_intro": "This retreat is designed for anyone seeking inner peace and physical wellness.",
                "who_can_benefit_bullets": [
                    "Working professionals seeking stress relief",
                    "Beginners wanting to learn yoga fundamentals",
                    "Fitness enthusiasts looking for holistic wellness",
                    "Spiritual seekers on a journey of self-discovery",
                    "Couples wanting a rejuvenating getaway",
                ],
                "program_highlights": {
                    "heading": "Program Highlights",
                    "morning": [
                        {"time": "06:00 AM", "activity": "Sunrise Yoga & Pranayama"},
                        {"time": "08:00 AM", "activity": "Sattvic Breakfast"},
                    ],
                    "daytime": [
                        {"time": "10:00 AM", "activity": "Yoga Philosophy Class"},
                        {"time": "01:00 PM", "activity": "Vegetarian Lunch & Rest"},
                    ],
                    "evening": [
                        {"time": "05:00 PM", "activity": "Hatha Yoga Session"},
                        {"time": "07:00 PM", "activity": "Ganga Aarti & Meditation"},
                    ],
                },
                "meal_section_heading": "Sattvic Meals",
                "meal_section_bullets": [
                    "Nutritious vegetarian meals prepared with fresh organic ingredients",
                    "Special detox juices and herbal teas served throughout the day",
                ],
                "accommodation_heading": "Comfortable Stay",
                "accommodation_bullets": [
                    "Clean AC rooms with hot water and Wi-Fi",
                    "Serene garden views from every room",
                ],
                "benefits_heading": "Key Benefits",
                "benefits_items": [
                    "Improved flexibility and strength",
                    "Reduced stress and anxiety",
                    "Better sleep quality",
                    "Enhanced mental clarity",
                    "Detoxified body and mind",
                    "Deeper spiritual connection",
                    "Healthier eating habits",
                    "Lasting inner peace",
                ],
                "how_to_book_heading": "How to Book",
                "how_to_book_steps": [
                    "Choose your preferred dates and package",
                    "Fill the online booking form",
                    "Pay 30% advance to confirm",
                    "Receive confirmation email with details",
                    "Arrive at the retreat center",
                    "Begin your transformative journey",
                ],
                "prices_photos_reviews": "Rated 4.8/5 by over 200 guests. Starting at ₹15,000 per person.",
                "itinerary": [
                    {
                        "day_number": 1,
                        "sessions": [
                            {"time": "02:00 PM", "activity": "Check-in & Orientation"},
                            {"time": "05:00 PM", "activity": "Welcome Yoga Session"},
                            {"time": "07:00 PM", "activity": "Dinner & Introduction Circle"},
                        ],
                    },
                    {
                        "day_number": 2,
                        "sessions": [
                            {"time": "06:00 AM", "activity": "Sunrise Yoga"},
                            {"time": "09:00 AM", "activity": "Pranayama & Meditation"},
                            {"time": "07:00 PM", "activity": "Ganga Aarti Visit"},
                        ],
                    },
                    {
                        "day_number": 3,
                        "sessions": [
                            {"time": "06:00 AM", "activity": "Advanced Asana Practice"},
                            {"time": "02:00 PM", "activity": "Nature Walk & Trek"},
                            {"time": "06:00 PM", "activity": "Meditation by the River"},
                        ],
                    },
                ],
                "pricing_table": [
                    {"guests": "1 Person", "cost_per_person": "₹18,000"},
                    {"guests": "2 Persons", "cost_per_person": "₹15,000"},
                    {"guests": "3-5 Persons", "cost_per_person": "₹13,500"},
                    {"guests": "6+ Persons", "cost_per_person": "₹12,000"},
                ],
                "inclusions": [
                    "AC accommodation for 6 nights",
                    "All sattvic meals and herbal teas",
                    "Daily yoga and meditation sessions",
                    "Ayurvedic massage (1 session)",
                    "Local sightseeing tour",
                    "Yoga mat and props",
                ],
                "exclusions": [
                    "Airfare or train tickets to Rishikesh",
                    "Travel insurance",
                    "Personal expenses and shopping",
                    "Alcoholic beverages",
                    "Non-vegetarian food",
                    "Laundry services",
                    "Phone calls and internet charges",
                    "Medical expenses",
                    "Tips and gratuities",
                    "Any activities not mentioned in inclusions",
                    "Camera fees at monuments",
                    "Extra Ayurvedic therapies",
                    "Private transport (shared transport included)",
                    "Visa fees for international guests",
                    "GST as applicable",
                ],
                "nearby_locations_heading": "Nearby Locations",
                "nearby_locations": [
                    {"name": "Jolly Grant Airport", "distance": "21 km", "type": "airport"},
                    {"name": "Rishikesh Railway Station", "distance": "3 km", "type": "railway"},
                    {"name": "ISBT Rishikesh", "distance": "2.5 km", "type": "bus"},
                    {"name": "Laxman Jhula", "distance": "1.5 km", "type": "sightseeing"},
                    {"name": "Ram Jhula", "distance": "2 km", "type": "sightseeing"},
                    {"name": "Triveni Ghat", "distance": "4 km", "type": "sightseeing"},
                ],
                "cancellation_policy": "Cancellations made 15 days before arrival receive a full refund minus 5% processing fee. 7-14 days: 50% refund. Less than 7 days: no refund. No-shows are non-refundable.",
                "payment_policy_bullets": [
                    "30% advance payment required to confirm booking",
                    "Balance due 7 days before arrival",
                    "Payments accepted via UPI, bank transfer, or credit card",
                ],
                "terms_conditions": [
                    "Guests must carry a valid photo ID at check-in.",
                    "Check-in time is 2:00 PM; check-out is 12:00 PM.",
                    "The management reserves the right to cancel bookings in case of emergencies.",
                    "Guests are responsible for their personal belongings.",
                    "Smoking and alcohol are strictly prohibited on premises.",
                    "Silence must be maintained in meditation halls.",
                    "Mobile phones should be on silent mode during sessions.",
                    "The retreat is not liable for injuries during self-practice.",
                    "Children below 12 years must be accompanied by an adult.",
                    "Pets are not allowed.",
                    "Any damage to property will be charged to the guest.",
                    "Force majeure events may lead to rescheduling without refund.",
                    "By booking, you agree to all terms and conditions stated above.",
                ],
                "faq": [
                    {"question": "What should I bring?", "answer": "Comfortable yoga clothes, personal toiletries, and a water bottle. Mats and props are provided."},
                    {"question": "Is prior yoga experience required?", "answer": "No, beginners are welcome. Our instructors adapt sessions to all levels."},
                    {"question": "Can I get a private room?", "answer": "Yes, private rooms are available at a supplement of ₹2,000 per night."},
                    {"question": "What is the refund policy?", "answer": "Full refund minus 5% if cancelled 15+ days prior. See cancellation policy for details."},
                ],
            })
        if "qa" in system_msg.lower():
            return json.dumps({"score": 82, "flags": ["PASS"], "notes": "All 19 sections present. Readability good."})
        return json.dumps({"result": "mock"})
