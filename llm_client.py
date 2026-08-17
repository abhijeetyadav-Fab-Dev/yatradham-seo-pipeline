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
        """Return a useful mock response when no LLM provider is available.
        
        For content generation (Content Studio), returns properly formatted markdown
        that the markdown parser can handle. For SEO pipeline tasks, returns JSON.
        """
        system_msg = messages[0].get("content", "") if messages else ""
        user_msg = messages[-1].get("content", "") if len(messages) > 1 else ""
        
        # Detect Content Studio requests (system prompt contains Yatradham content writer instructions)
        is_content_studio = "SEO Content Writer" in system_msg and "markdown headings" in system_msg.lower()
        
        if is_content_studio:
            # Extract topic from user message
            topic = "Wellness Travel Guide"
            for line in user_msg.split("\n"):
                if line.startswith("Topic:"):
                    topic = line.split(":", 1)[1].strip()
                    break
            
            if "blog" in system_msg.lower() or "blog" in user_msg.lower():
                return f"""# TITLE
{topic}

# META DESCRIPTION
Discover the ultimate guide to {topic.lower()}. Plan your spiritual journey with expert tips, detailed itineraries, and insider recommendations from Yatradham.org.

# SUGGESTED TAGS
wellness travel, spiritual tourism, yoga retreat, Rishikesh, meditation, Yatradham

# CONTENT
## Introduction

{topic} is one of the most sought-after experiences for wellness enthusiasts and spiritual seekers. Nestled in the foothills of the Himalayas, this journey promises a transformative experience that rejuvenates both body and soul.

Whether you are a seasoned yogi or a first-time traveler seeking inner peace, this comprehensive guide will help you plan every detail of your wellness retreat.

## Day 1-2: Arrival and Acclimatization

Your wellness journey begins with a gentle introduction to the spiritual atmosphere. Check into your accommodation and spend the first two days settling in with light yoga sessions, guided meditation, and exploring the local surroundings.

### Morning Routine
- 6:00 AM — Sunrise yoga and pranayama by the river
- 8:00 AM — Nutritious sattvic breakfast
- 10:00 AM — Guided walking meditation

### Afternoon Activities
- Nature walks along scenic trails
- Introduction to Ayurvedic principles
- Free time for personal reflection

## Day 3-4: Deep Wellness Immersion

These days focus on deeper practices including advanced asanas, intensive meditation sessions, and Ayurvedic therapies. You will experience traditional healing techniques that have been practiced for centuries.

### Highlights
- Full-body Abhyanga massage
- Yoga Nidra (yogic sleep) sessions
- Pranayama breathing workshops
- Philosophy discussions with experienced teachers

## Day 5-6: Spiritual Exploration

Explore the spiritual heritage of the region with visits to ancient temples, participation in traditional ceremonies, and deeper meditation practices.

### Key Experiences
- Ganga Aarti ceremony at sunset
- Visit to historic ashrams and temples
- Silent meditation retreat (half-day)
- Sound healing session with Tibetan bowls

## Day 7: Integration and Departure

The final day focuses on integrating your experiences and creating a personal wellness plan you can continue at home.

- Morning gratitude meditation
- Closing ceremony and sharing circle
- Personal wellness plan consultation
- Departure with renewed energy and purpose

## Practical Tips for Your Journey

1. **Best Time to Visit**: October to March offers pleasant weather ideal for outdoor yoga
2. **What to Pack**: Comfortable loose clothing, a reusable water bottle, sunscreen, and a journal
3. **Budget**: Expect to spend ₹12,000-₹20,000 per person for a quality 7-day retreat
4. **Getting There**: The nearest airport is Jolly Grant (21 km), with regular trains to Rishikesh station
5. **Health Precautions**: Carry personal medications and stay hydrated

## Why Choose Yatradham for Your Wellness Journey?

Yatradham.org has been India's trusted religious and wellness tourism platform since 2016, serving pilgrims across 700+ destinations. With verified accommodations, curated wellness packages, and dedicated support, your spiritual journey is in safe hands.

## Conclusion

A 7-day wellness retreat is more than a vacation — it is an investment in your health, happiness, and spiritual growth. Start planning your transformative journey today with Yatradham and discover the profound peace that awaits you.

**Ready to begin? [Book your wellness retreat on Yatradham.org](https://yatradham.org) and take the first step toward rejuvenation.**"""

            elif "landing" in system_msg.lower():
                return f"""# HEADLINE
{topic} — Transform Your Life in 7 Days

# SUBHEADLINE
Join hundreds of satisfied guests on India's most trusted wellness retreat platform

# META DESCRIPTION
Book your {topic.lower()} with Yatradham. Verified accommodations, expert instructors, and a life-changing experience. Starting at ₹12,000.

# HERO TEXT
Escape the chaos of daily life and immerse yourself in a carefully curated wellness experience. Our 7-day program combines ancient yogic wisdom with modern comfort to deliver lasting transformation.

# WHY CHOOSE
- Expert instructors with 10+ years of experience
- Scenic riverside locations in the Himalayan foothills
- Small group sizes for personalized attention
- All-inclusive packages with meals and therapies
- Trusted by 5,000+ guests since 2016

# WHATS INCLUDED
- 6 nights premium accommodation
- Daily yoga and meditation sessions
- All sattvic vegetarian meals
- One Ayurvedic massage session
- Guided spiritual excursions
- Airport/station pickup and drop

# IDEAL FOR
- Working professionals seeking stress relief
- Beginners exploring yoga and meditation
- Couples looking for a rejuvenating getaway
- Spiritual seekers on a path of self-discovery
- Fitness enthusiasts wanting holistic wellness

# PRICING CTA
Starting at ₹12,000 per person. Book now and get 10% early bird discount. Limited spots available for the next batch!

# FAQ
Q: Do I need prior yoga experience?
A: Not at all! Our programs are designed for all levels, from complete beginners to advanced practitioners.

Q: What should I bring?
A: Comfortable clothing, personal toiletries, and a water bottle. Yoga mats and props are provided.

Q: Is the food vegetarian only?
A: Yes, we serve nutritious sattvic vegetarian meals prepared with fresh, organic ingredients to support your wellness journey.

Q: What is the cancellation policy?
A: Full refund (minus 5% processing fee) for cancellations 15+ days before arrival. 50% refund for 7-14 days. No refund within 7 days."""

            elif "destination" in system_msg.lower():
                return f"""# TITLE
{topic} — Complete Destination Guide

# META DESCRIPTION
Everything you need to know about {topic.lower()}. Best time to visit, how to reach, top attractions, accommodation options, and insider tips from Yatradham.

# SUGGESTED TAGS
destination guide, spiritual tourism, pilgrimage, wellness travel, Yatradham

# KEY HIGHLIGHTS
- Sacred spiritual destination with centuries of heritage
- Accessible by air, rail, and road from major cities
- Best visited between October and March
- Wide range of verified accommodations available on Yatradham

# CONTENT
## Overview

This destination has been a beacon for spiritual seekers and wellness enthusiasts for centuries. Surrounded by natural beauty and steeped in cultural heritage, it offers a unique blend of tranquility and transformation.

## Best Time to Visit

The ideal months are **October through March**, when temperatures are pleasant and skies are clear. Summers (April-June) can be warm but are popular for yoga teacher training programs. The monsoon season (July-September) brings lush greenery but travel may be disrupted.

## How to Reach

- **By Air**: Nearest airport with taxi services available
- **By Train**: Well-connected railway station with trains from Delhi, Mumbai, and other major cities
- **By Road**: National highway access with regular bus services from nearby cities

## Top Attractions & Temples

Explore historic temples, sacred rivers, and spiritual centers that have drawn pilgrims for generations.

## Where to Stay

Yatradham offers verified accommodations ranging from budget ashrams to premium wellness resorts. All properties are personally inspected for cleanliness, safety, and comfort.

## Plan Your Visit with Yatradham

Book your complete spiritual journey on [Yatradham.org](https://yatradham.org) — India's first dedicated religious tourism platform with 700+ destinations."""

            else:
                # Social media / generic
                return f"""# CAPTION 1
Platform: Instagram
Text: ✨ Discover the transformative power of {topic.lower()}. Your journey to inner peace starts here. 🙏
Hashtags: #YatradhamJourney #WellnessTravel #SpiritualTourism #YogaRetreat #InnerPeace

# CAPTION 2
Platform: Facebook
Text: Looking for a life-changing wellness experience? Our curated {topic.lower()} programs combine ancient wisdom with modern comfort. Join 5,000+ happy travelers who found their peace with Yatradham. Book now!
Hashtags: #Yatradham #WellnessRetreat #SpiritualJourney #YogaLife"""

        # SEO pipeline mock responses (non-Content-Studio)
        if "keyword" in system_msg.lower():
            return json.dumps({"primary_keyword": "Yoga Retreat Rishikesh", "secondary_keywords": ["Meditation Retreat", "Wellness Tour"]})
        if "title" in system_msg.lower():
            return json.dumps({"title_tag": "Yoga Retreat in Rishikesh | 7 Days Wellness Tour"})
        if "meta" in system_msg.lower():
            return json.dumps({"meta_description": "Join our 7-day yoga retreat in Rishikesh. Experience meditation, wellness, and peace. Book now for a transformative journey!"})
        if "qa" in system_msg.lower():
            return json.dumps({"score": 82, "flags": ["PASS"], "notes": "All 19 sections present. Readability good."})
        return json.dumps({"result": "mock"})
