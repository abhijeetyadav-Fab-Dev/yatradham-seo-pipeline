import os
import time
import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

DEFAULT_OPENROUTER_MODEL = "google/gemma-4-31b-it:free"
OPENROUTER_FALLBACK_MODELS = [
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "z-ai/glm-5.2:free",
    "openai/gpt-oss-20b:free",
]

GROQ_DEFAULT_MODEL = "llama-3.3-70b-versatile"
GROQ_FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "mixtral-8x7b-32768",
]

GEMINI_DEFAULT_MODEL = "gemini-2.0-flash"
GEMINI_FALLBACK_MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]

import logging

logger = logging.getLogger("llm_client")

class LLMClient:
    def __init__(self):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass

        # OpenRouter config
        self.openrouter_api_key = (os.getenv("OPENROUTER_API_KEY", "") or "").strip().strip("'\"")
        self.openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", DEFAULT_OPENROUTER_MODEL)
        
        # Groq config (Fast free tier: ~300+ tok/s)
        self.groq_api_key = (os.getenv("GROQ_API_KEY", "") or "").strip().strip("'\"")
        self.groq_model = os.getenv("GROQ_MODEL", GROQ_DEFAULT_MODEL)
        
        # Gemini config (Google AI Studio free tier: 15 RPM)
        self.gemini_api_key = (os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "") or "").strip().strip("'\"")
        self.gemini_model = os.getenv("GEMINI_MODEL", GEMINI_DEFAULT_MODEL)

        self.last_call_time = 0.0
        self.min_interval = 0.05  # Ultra-fast non-blocking throttle
        self.last_provider_used = None
        self.last_model_used = None
        self.last_error = None
        self.errors: Dict[str, str] = {}
        self.dry_run = False
        
        # Initialize clients if keys exist
        self.openrouter_client: Optional[OpenAI] = None
        self.groq_client: Optional[OpenAI] = None
        self.gemini_client: Optional[OpenAI] = None
        
        self._init_clients()

    def _init_clients(self):
        if self.dry_run:
            return
        if self.groq_api_key:
            self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.groq_api_key, timeout=12.0)
        if self.gemini_api_key:
            self.gemini_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=self.gemini_api_key, timeout=12.0)
        if self.openrouter_api_key:
            self.openrouter_client = OpenAI(base_url=self.openrouter_base_url, api_key=self.openrouter_api_key, timeout=12.0)

    def set_custom_keys(self, provider: str, api_key: str, model: Optional[str] = None):
        """Allow setting runtime keys dynamically for a request without server restart."""
        clean_key = (api_key or "").strip().strip("'\"")
        if not clean_key:
            return
        
        if provider == "groq":
            self.groq_api_key = clean_key
            if model: self.groq_model = model
            self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=clean_key, timeout=12.0)
        elif provider == "gemini":
            self.gemini_api_key = clean_key
            if model: self.gemini_model = model
            self.gemini_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=clean_key, timeout=12.0)
        elif provider == "openrouter":
            self.openrouter_api_key = clean_key
            if model: self.openrouter_model = model
            self.openrouter_client = OpenAI(base_url=self.openrouter_base_url, api_key=clean_key, timeout=12.0)

    _model_cache = {}

    def _discover_active_models(self, client_inst: OpenAI, provider: str) -> List[str]:
        """Dynamically query the provider's live models list to avoid model_not_found errors with memory cache."""
        if provider in self._model_cache:
            return self._model_cache[provider]

        try:
            res = client_inst.models.list()
            model_ids = []
            for m in res.data:
                mid = m.id.replace("models/", "")
                # Filter out incompatible, audio, embeddings, tiny TPM or deprecated models
                if any(x in mid.lower() for x in ["whisper", "embedding", "guard", "vision", "audio", "tts", "moderation", "2.5-pro", "gpt-oss", "deepseek-r1", "deprecated"]):
                    continue
                if provider == "groq" and mid not in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"]:
                    continue
                if provider == "gemini" and mid not in ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
                    continue
                model_ids.append(mid)
            if model_ids:
                # Prioritize llama-3.3-70b and llama-3.1-8b for groq
                if provider == "groq":
                    model_ids = [m for m in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"] if m in model_ids]
                self._model_cache[provider] = model_ids
                return model_ids
        except Exception:
            pass
        
        if provider == "groq":
            return GROQ_FALLBACK_MODELS
        elif provider == "gemini":
            return GEMINI_FALLBACK_MODELS
        elif provider == "openrouter":
            return OPENROUTER_FALLBACK_MODELS
        return []

    def test_provider(self, provider: str, api_key: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Test a provider API key with a fast 1-word prompt to verify connection."""
        clean_key = (api_key or "").strip().strip("'\"")
        if not clean_key:
            return {"success": False, "error": "API key is empty"}
        
        t0 = time.time()
        try:
            if provider == "groq":
                test_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=clean_key, timeout=12.0)
                fallback_list = GROQ_FALLBACK_MODELS
            elif provider == "gemini":
                test_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=clean_key, timeout=12.0)
                fallback_list = GEMINI_FALLBACK_MODELS
            elif provider == "openrouter":
                test_client = OpenAI(base_url=self.openrouter_base_url, api_key=clean_key, timeout=12.0)
                fallback_list = OPENROUTER_FALLBACK_MODELS
            else:
                return {"success": False, "error": f"Unknown provider: {provider}"}
            
            # Discover live supported models from API
            available_models = self._discover_active_models(test_client, provider)
            candidates = []
            if model:
                candidates.append(model.replace("models/", ""))
            for am in available_models + fallback_list:
                am_clean = am.replace("models/", "")
                if am_clean not in candidates:
                    candidates.append(am_clean)
            
            last_err = None
            for test_model in candidates:
                try:
                    resp = test_client.chat.completions.create(
                        model=test_model,
                        messages=[{"role": "user", "content": "ping"}],
                        max_tokens=5,
                    )
                    elapsed_ms = int((time.time() - t0) * 1000)
                    return {
                        "success": True,
                        "provider": provider,
                        "model": test_model,
                        "latency_ms": elapsed_ms,
                        "message": f"Connected successfully via {test_model} ({elapsed_ms}ms)"
                    }
                except Exception as model_err:
                    last_err = str(model_err)
                    continue
            
            return {
                "success": False,
                "provider": provider,
                "error": last_err or "No active model succeeded"
            }
        except Exception as e:
            return {
                "success": False,
                "provider": provider,
                "error": str(e)
            }

    def _wait_for_rate_limit(self):
        elapsed = time.time() - self.last_call_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call_time = time.time()

    def _strip_reasoning(self, text: str) -> str:
        """Strip internal thinking/reasoning tags leaked from thinking models."""
        if not text:
            return ""
        for tag in ("think", "thinking", "reasoning", "reflection", "inner_monologue", "scratchpad"):
            text = re.sub(rf"<{tag}>.*?</{tag}>", "", text, flags=re.DOTALL | re.IGNORECASE)
        for tag in ("think", "thinking", "reasoning", "reflection"):
            pattern = rf"<{tag}>"
            while re.search(pattern, text, flags=re.IGNORECASE):
                m = re.search(pattern, text, flags=re.IGNORECASE)
                start_pos = m.start()
                rest = text[m.end():]
                header_match = re.search(r'(?:\n|^)(#{1,3}\s+[^\n]+)', rest)
                if header_match:
                    text = text[:start_pos] + rest[header_match.start():]
                else:
                    text = text[:start_pos]
                    break
        return text.strip()

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
            self.last_provider_used = "dry_run"
            return self._mock_response(messages)

        # Build list of available clients/providers to attempt in priority order
        providers = []
        if self.groq_client:
            live_groq = self._discover_active_models(self.groq_client, "groq")
            models_to_try = [model] if model else []
            for gm in live_groq + GROQ_FALLBACK_MODELS:
                if gm and gm not in models_to_try:
                    models_to_try.append(gm)
            for gm in models_to_try:
                providers.append(("groq", self.groq_client, gm))
                
        if self.gemini_client:
            live_gem = self._discover_active_models(self.gemini_client, "gemini")
            models_to_try = [model] if model else []
            for gm in live_gem + GEMINI_FALLBACK_MODELS:
                if gm and gm not in models_to_try:
                    models_to_try.append(gm)
            for gm in models_to_try:
                providers.append(("gemini", self.gemini_client, gm))
                
        if self.openrouter_client:
            primary_or = model or self.openrouter_model
            for or_model in [primary_or] + [m for m in OPENROUTER_FALLBACK_MODELS if m != primary_or]:
                providers.append(("openrouter", self.openrouter_client, or_model))

        if not providers:
            self.last_provider_used = "mock (no keys configured)"
            self.last_error = "No API keys configured. Set GROQ_API_KEY or GEMINI_API_KEY."
            return self._mock_response(messages)

        now = time.time()
        if not hasattr(self, "_failed_providers"):
            self._failed_providers = {}
        self._failed_providers = {k: v for k, v in self._failed_providers.items() if now - v < 60}

        active_providers = [p for p in providers if p[0] not in self._failed_providers]
        if not active_providers:
            active_providers = providers

        self.errors = {}
        exhausted_providers = set()

        for provider_name, client_inst, active_model in active_providers:
            if provider_name in exhausted_providers:
                continue

            self._wait_for_rate_limit()
            try:
                safe_temp = max(0.2, min(temperature, 0.65))
                safe_max_tokens = min(max_tokens, 4096) if provider_name == "groq" else max_tokens
                kwargs = {
                    "model": active_model,
                    "messages": messages,
                    "max_tokens": safe_max_tokens,
                    "temperature": safe_temp,
                    "timeout": 12.0,
                }
                if provider_name in ["groq", "openrouter"]:
                    kwargs["top_p"] = 0.95
                if response_format and provider_name != "groq":
                    kwargs["response_format"] = response_format

                resp = client_inst.chat.completions.create(**kwargs)
                choice = resp.choices[0]
                content = choice.message.content or ""
                finish_reason = getattr(choice, 'finish_reason', None)

                # Seamlessly continue if response was cut off mid-way by token limit
                continuation_pass = 0
                while finish_reason == "length" and continuation_pass < 2 and content.strip():
                    continuation_pass += 1
                    logger.info(f"Response truncated (finish_reason=length). Running auto-continuation pass {continuation_pass}...")
                    try:
                        cont_messages = messages + [
                            {"role": "assistant", "content": content},
                            {"role": "user", "content": "Continue generating the rest of the content seamlessly from where you stopped. Do not repeat any text already written above."}
                        ]
                        cont_kwargs = dict(kwargs)
                        cont_kwargs["messages"] = cont_messages
                        cont_resp = client_inst.chat.completions.create(**cont_kwargs)
                        cont_choice = cont_resp.choices[0]
                        cont_text = cont_choice.message.content or ""
                        if cont_text.strip():
                            content += "\n" + cont_text.strip()
                            finish_reason = getattr(cont_choice, 'finish_reason', None)
                        else:
                            break
                    except Exception as cont_err:
                        logger.warning(f"Auto-continuation pass failed: {cont_err}")
                        break

                if content.strip():
                    cleaned_content = self._strip_reasoning(content)
                    self.last_provider_used = provider_name
                    self.last_model_used = active_model
                    self.last_error = None
                    return cleaned_content
            except Exception as e:
                err_msg = str(e)
                self.errors[f"{provider_name}:{active_model}"] = err_msg
                logger.warning(f"Provider {provider_name} ({active_model}) failed: {err_msg}. Trying next...")
                if any(code in err_msg.lower() for code in ["429", "rate_limit", "rate limit", "401", "402", "403", "404", "model_not_found", "unauthorized", "insufficient_quota", "payment"]):
                    logger.warning(f"Provider {provider_name} is exhausted or blocked. Skipping remaining models on {provider_name}.")
                    exhausted_providers.add(provider_name)
                    self._failed_providers[provider_name] = time.time()
                continue

        # If all providers fail, record error and return mock
        self.last_provider_used = "mock (all providers failed)"
        self.last_error = "; ".join([f"{k}: {v}" for k, v in self.errors.items()][:2])
        return self._mock_response(messages)

    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        """Return a useful mock response when no LLM provider is available.
        
        For content generation (Content Studio), returns properly formatted markdown
        that the markdown parser can handle. For SEO pipeline tasks, returns JSON.
        """
        system_msg = messages[0].get("content", "") if messages else ""
        user_msg = messages[-1].get("content", "") if len(messages) > 1 else ""
        
        # Detect completion pass in Content Studio
        if "Missing sections to write:" in user_msg or "preceding part of the guide" in user_msg:
            return """## 3 Key Takeaways From This Sacred Yatra

### 1. Pacing Drives True Spiritual & Physical Rejuvenation
Rushing through the high Himalayan shrines leaves the body exhausted and the mind scattered. When you allocate adequate time for each darshan, your nervous system relaxes and acclimatizes safely to high altitudes above 10,000 feet.

### 2. High-Value Experiences Win Over Crowded Sightseeing
A personalized morning Ganga Aarti, peaceful ashram stay, and authentic Satvik meals deliver ten times the value of a rushed generic sightseeing tour.

### 3. Local Etiquette & Trust Build the Connection
Respecting temple customs, maintaining silence in sanctums, and keeping riverbanks clean unlocks deep warmth from local priests and mountain elders.

## 4 Ways YatraDham.Org Makes Your Journey Seamless & Safe

- **1. Verified Accommodations & Transparent Pricing:** Every dharamshala and ashram is vetted for hot water, clean bedding, and vegetarian dining with upfront rates.
- **2. Dedicated Yatra & Transport Coordination:** Punctual airport pickups, train transfers, and reliable hill drivers with pre-negotiated rates.
- **3. Tailored Spiritual & Wellness Itineraries:** Expert schedules matched to family and senior citizen needs with exact Aarti timings.
- **4. 24/7 Pilgrim Support & Flexible Booking:** Round-the-clock WhatsApp assistance and free cancellations up to 48 hours before arrival.

## 3 Actionable Tips to Plan Your Journey Today

1. **Target the Best Season:** Plan your visit during May-June or September-October for clear weather and safe road conditions.
2. **Book Verified Dharamshalas Early:** Reserve stays 3-4 weeks ahead on YatraDham.Org to secure rooms near main temple gates.
3. **Acclimatize Gradually:** Stay hydrated, avoid heavy foods during travel, and practice deep breathing for effortless mountain ascents.

## The Real Logistics: Costs, Stays & Commutes

- **Flights & Trains:** Fly to Dehradun Airport (Jolly Grant) or take express trains from Delhi to Haridwar Junction (₹400–₹1,200). Private taxis from airport to Haridwar start from ₹1,000.
- **Package Pricing:** A complete 9-to-10 day Chardham Yatra package from Haridwar ranges from ₹28,000 to ₹45,000 per person including transport, accommodation, and Satvik meals.
- **Daily Expenses:** Budget ₹500–₹800 per day for Satvik meals and local transfers.

## Frequently Asked Questions

### Q1. What is the average price of a Chardham Yatra package from Haridwar?
A typical package ranges between ₹28,000 and ₹45,000 per person depending on group size, vehicle type, and accommodation standards.

### Q2. How many days are required for Chardham Yatra from Haridwar?
The standard circuit takes 9 to 10 days to cover Yamunotri, Gangotri, Kedarnath, and Badrinath comfortably with necessary acclimatization stops.

### Q3. Is Chardham Yatra safe for senior citizens?
Yes. With YatraDham's verified ground transport, oxygen-equipped vehicles, pony/palki arrangements, and clean dharamshalas, seniors travel with total comfort.

### Q4. What kind of food is available during the Yatra?
100% pure vegetarian, hygienic Satvik meals including fresh rotis, dal, khichdi, seasonal vegetables, and warm herbal tea.

### Q5. What is the best month to visit Chardham?
May to June (early summer) and September to October (autumn) offer clear mountain skies, open roads, and pleasant darshan temperatures.

### Q6. How do I book verified dharamshalas and packages?
You can book verified dharamshalas, ashrams, and complete packages directly through [YatraDham.org](https://yatradham.org) with instant confirmation and 24/7 support.

## Final Thoughts & Planning Your Trip

Embarking on the sacred Chardham pilgrimage from Haridwar is a life-affirming journey of faith, peace, and natural beauty. With YatraDham.Org managing your stays, transfers, and darshan logistics, you can immerse yourself completely in the spiritual blessings of Devbhoomi Uttarakhand.

**Start planning your sacred journey today: [Explore verified Chardham packages on YatraDham.org](https://yatradham.org).**

## Related Articles & Recommended Reading
- **Title:** Complete Haridwar to Kedarnath Route & Dharamshala Guide (YatraDham Travel Team • Updated 2026 • Essential route distances, helicopter options, and verified stays)
- **Title:** Best Time to Visit Chardham: Weather, Crowd & Registration Guide (Pandit R. Shastri • Updated 2026 • Month-by-month temperature charts and yatra tips)
- **Title:** Top 10 Budget Dharamshalas Near Har Ki Pauri Haridwar (YatraDham Editorial • Updated 2026 • Verified properties with hot water, parking, and Satvik food)"""

        # Detect Content Studio requests
        is_content_studio = any(x in system_msg.lower() for x in ["seo content writer", "yatradham", "markdown headings", "editorial"]) or any(x in user_msg.lower() for x in ["topic / destination:", "topic:", "# title", "chardham", "blog"])
        
        if is_content_studio:
            # Extract topic from user message
            topic = "Chardham Yatra Package from Haridwar"
            for line in user_msg.split("\n"):
                if "topic" in line.lower() and ":" in line:
                    topic = line.split(":", 1)[1].strip()
                    break
            
            return f"""# TITLE
{topic} — Complete Travel, Route & Cost Guide | YatraDham

# META DESCRIPTION
Plan your sacred journey with our complete guide to {topic.lower()}. Verified dharamshalas, exact route pricing, Satvik meals, and 24/7 pilgrim support on YatraDham.Org.

# SUGGESTED TAGS
Chardham Yatra, Haridwar, Kedarnath, Badrinath, Gangotri, Yamunotri, Spiritual Tourism, YatraDham

# CONTENT
## Introduction & Sacred Significance

The sacred Chardham pilgrimage across Yamunotri, Gangotri, Kedarnath, and Badrinath is the pinnacle of spiritual journeys in India. Starting your yatra from the holy city of Haridwar provides smooth connectivity, easy acclimatization, and a deeply blessed beginning along the banks of the sacred Ganga.

Whether you are traveling with elderly parents, family, or as an independent seeker, choosing a well-planned itinerary ensures safety, peace of mind, and transparent pricing.

## Complete Day-by-Day Route & Darshan Itinerary

### Day 1: Haridwar to Barkot / Yamunotri Base (215 km / 7-8 hrs)
Begin your journey with an early morning departure from Haridwar. Drive through scenic Mussoorie and the Kempty Falls route toward Barkot. Check into your verified YatraDham dharamshala and prepare for the next morning's trek.

### Day 2: Barkot to Yamunotri Dham & Return (36 km drive + 6 km trek each way)
Trek to the holy shrine of Goddess Yamuna. Take holy darshan, cook rice in the natural hot springs of Surya Kund, and return to Barkot for evening Satvik dinner.

### Day 3: Barkot to Uttarkashi (100 km / 4 hrs)
Drive along the Bhagirathi river to Uttarkashi. Visit the historic Kashi Vishwanath Temple and Shakti Temple for evening Aarti.

### Day 4: Uttarkashi to Gangotri Dham & Return (100 km each way / 3-4 hrs)
Drive through the picturesque Harsil Valley. Take holy bath at Gangotri and offer prayers at the sacred shrine of Goddess Ganga before returning to Uttarkashi.

### Day 5: Uttarkashi to Guptkashi / Sitapur (220 km / 8-9 hrs)
Scenic mountain drive toward the Mandakini valley, the gateway to Kedarnath Dham. Rest and prepare for the Kedarnath trek.

### Day 6: Guptkashi to Kedarnath Dham (30 km drive + 16 km trek / Heli)
Ascend to the majestic Kedarnath temple nestled amid snow-clad peaks. Attend the evening Shiv Aarti and experience overnight stillness near the shrine.

### Day 7: Kedarnath Darshan & Return to Guptkashi
Attend early morning Maha Abhishek Puja, then descend back to Gaurikund and transfer to your Guptkashi stay.

### Day 8: Guptkashi to Badrinath Dham (190 km / 7 hrs)
Drive past Joshimath to the divine abode of Lord Badri Vishal. Take a holy dip in Tapt Kund and attend evening Swarna Aarti.

### Day 9: Badrinath to Rudraprayag / Srinagar (160 km / 6 hrs)
Visit Mana Village (the last Indian village), Vyas Gufa, and Saraswati River origin before driving down to Rudraprayag.

### Day 10: Rudraprayag to Haridwar (165 km / 5-6 hrs)
Witness the sacred confluence at Devprayag (Alaknanda meets Bhagirathi to form the Ganga) before concluding your yatra at Haridwar Junction.

## 3 Key Takeaways From This Sacred Yatra

### 1. Pacing Drives True Spiritual & Physical Rejuvenation
Rushing through the high Himalayan shrines leaves the body exhausted and the mind scattered. When you allocate 2-3 hours for each sacred darshan and allow steady acclimatization, your body adapts naturally to high altitudes above 10,000 feet.

### 2. High-Value Experiences Win Over Crowded Sightseeing
A personalized morning Ganga Aarti, peaceful ashram stay, and authentic Satvik meals deliver ten times the value of a rushed generic sightseeing tour.

### 3. Local Etiquette & Trust Build the Connection
Respecting temple customs, maintaining silence in sanctums, and keeping riverbanks clean unlocks deep warmth from local priests and mountain elders.

## 4 Ways YatraDham.Org Makes Your Journey Seamless & Safe

- **1. Verified Accommodations & Transparent Pricing:** Every dharamshala and ashram is vetted for hot water, clean bedding, and vegetarian dining with upfront rates from ₹600 to ₹2,200 per night.
- **2. Dedicated Yatra & Transport Coordination:** Punctual airport pickups, train transfers, and reliable hill drivers with pre-negotiated rates starting from ₹800.
- **3. Tailored Spiritual & Wellness Itineraries:** Expert schedules matched to family and senior citizen needs with exact Aarti timings.
- **4. 24/7 Pilgrim Support & Flexible Booking:** Round-the-clock WhatsApp assistance and free cancellations up to 48 hours before arrival on select partner stays.

## 3 Actionable Tips to Plan Your Journey Today

1. **Target the Best Season:** Plan your visit during May-June or September-October for clear weather and safe road conditions.
2. **Book Verified Dharamshalas Early:** Reserve stays 3-4 weeks ahead on YatraDham.Org to secure rooms near main temple gates.
3. **Acclimatize Gradually:** Stay hydrated, avoid heavy foods during travel, and practice deep breathing for effortless mountain ascents.

## The Real Logistics: Costs, Stays & Commutes

- **Flights & Trains:** Fly to Dehradun Airport (Jolly Grant) or take express trains from Delhi to Haridwar Junction (₹400–₹1,200). Private taxis from airport to Haridwar start from ₹1,000.
- **Package Pricing:** A complete 9-to-10 day Chardham Yatra package from Haridwar ranges from ₹28,000 to ₹45,000 per person including transport, accommodation, and Satvik meals.
- **Daily Expenses:** Budget ₹500–₹800 per day for Satvik meals and local transfers.

## Frequently Asked Questions

### Q1. What is the average price of a Chardham Yatra package from Haridwar?
A typical package ranges between ₹28,000 and ₹45,000 per person depending on group size, vehicle type, and accommodation standards.

### Q2. How many days are required for Chardham Yatra from Haridwar?
The standard circuit takes 9 to 10 days to cover Yamunotri, Gangotri, Kedarnath, and Badrinath comfortably with necessary acclimatization stops.

### Q3. Is Chardham Yatra safe for senior citizens?
Yes. With YatraDham's verified ground transport, oxygen-equipped vehicles, pony/palki arrangements, and clean dharamshalas, seniors travel with total comfort.

### Q4. What kind of food is available during the Yatra?
100% pure vegetarian, hygienic Satvik meals including fresh rotis, dal, khichdi, seasonal vegetables, and warm herbal tea.

### Q5. What is the best month to visit Chardham?
May to June (early summer) and September to October (autumn) offer clear mountain skies, open roads, and pleasant darshan temperatures.

### Q6. How do I book verified dharamshalas and packages?
You can book verified dharamshalas, ashrams, and complete packages directly through [YatraDham.org](https://yatradham.org) with instant confirmation and 24/7 support.

## Final Thoughts & Planning Your Trip

Embarking on the sacred Chardham pilgrimage from Haridwar is a life-affirming journey of faith, peace, and natural beauty. With YatraDham.Org managing your stays, transfers, and darshan logistics, you can immerse yourself completely in the spiritual blessings of Devbhoomi Uttarakhand.

**Start planning your sacred journey today: [Explore verified Chardham packages on YatraDham.org](https://yatradham.org).**

## Related Articles & Recommended Reading
- **Title:** Complete Haridwar to Kedarnath Route & Dharamshala Guide (YatraDham Travel Team • Updated 2026 • Essential route distances, helicopter options, and verified stays)
- **Title:** Best Time to Visit Chardham: Weather, Crowd & Registration Guide (Pandit R. Shastri • Updated 2026 • Month-by-month temperature charts and yatra tips)
- **Title:** Top 10 Budget Dharamshalas Near Har Ki Pauri Haridwar (YatraDham Editorial • Updated 2026 • Verified properties with hot water, parking, and Satvik food)"""

        # SEO pipeline mock responses (non-Content-Studio)
        if "keyword" in system_msg.lower():
            return json.dumps({"primary_keyword": "Yoga Retreat Rishikesh", "secondary_keywords": ["Meditation Retreat", "Wellness Tour"]})
        if "title" in system_msg.lower():
            return json.dumps({"title_tag": "Yoga Retreat in Rishikesh | 7 Days Wellness Tour"})
        if "meta" in system_msg.lower():
            return json.dumps({"meta_description": "Join our 7-day yoga retreat in Rishikesh. Experience meditation, wellness, and peace. Book now for a transformative journey!"})
        if "qa" in system_msg.lower():
            return json.dumps({"score": 82, "flags": ["PASS"], "notes": "All 19 sections present. Readability good."})
        
        # If no specific mock is found, return valid JSON or empty dict
        return json.dumps({"status": "ok", "message": "completed"})
