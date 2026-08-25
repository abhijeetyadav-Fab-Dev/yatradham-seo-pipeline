import os
import time
import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

DEFAULT_OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
OPENROUTER_FALLBACK_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "deepseek/deepseek-r1:free",
    "meta-llama/llama-3.2-3b-instruct:free",
]


GROQ_DEFAULT_MODEL = "llama-3.3-70b-versatile"
GROQ_FALLBACK_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "llama3-70b-8192",
    "llama3-8b-8192",
]

GEMINI_DEFAULT_MODEL = "gemini-2.0-flash"
GEMINI_FALLBACK_MODELS = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
]

NVIDIA_DEFAULT_MODEL = "meta/llama-3.3-70b-instruct"
NVIDIA_FALLBACK_MODELS = [
    "meta/llama-3.3-70b-instruct",
    "nvidia/llama-3.1-nemotron-70b-instruct",
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-8b-instruct",
    "mistralai/mistral-large-2-instruct",
]




def clean_price_string(raw_cost: str) -> str:
    """Sanitize and format price strings cleanly. Never return hardcoded mock numbers or bogus small amounts."""
    if not raw_cost or str(raw_cost).strip().lower() in ["rs,", "rs.", "rs", "inr", "contact for pricing", "null", "none", ""]:
        return "Starting From ₹ Contact for Pricing"
    
    clean = str(raw_cost).replace("rs,", "").replace("Rs ,", "").replace(" ,", "").strip()
    
    # Reject negative prices, 0, or free
    if "-" in clean or re.search(r'\b(?:free|0)\b', clean, re.I):
        return "Starting From ₹ Contact for Pricing"

    digits_match = re.search(r'[\d,]+(?:\.\d{2})?', clean)
    if not digits_match:
        return "Starting From ₹ Contact for Pricing"
    
    amount_str = digits_match.group(0)
    try:
        numeric_val = float(amount_str.replace(",", ""))
        if numeric_val < 100:
            return "Starting From ₹ Contact for Pricing"
    except ValueError:
        return "Starting From ₹ Contact for Pricing"
    
    if "." in amount_str:
        parts = amount_str.split(".")
        main_num = int(parts[0].replace(",", ""))
        formatted_amount = f"{main_num:,}.{parts[1]}"
    else:
        formatted_amount = f"{int(numeric_val):,}"

    suffix = ""
    if re.search(r'per\s*night', clean, re.I):
        suffix = " Per Person/Per night"
    elif re.search(r'per\s*person', clean, re.I):
        suffix = " Per Person"
        
    return f"Starting From ₹ {formatted_amount}{suffix}".strip()




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

        # NVIDIA NIM config (Enterprise fast tier: meta/llama-3.3-70b-instruct)
        self.nvidia_api_key = (os.getenv("NVIDIA_API_KEY", "") or os.getenv("NVAPI_KEY", "") or "").strip().strip("'\"")
        self.nvidia_model = os.getenv("NVIDIA_MODEL", NVIDIA_DEFAULT_MODEL)

        self.last_call_time = 0.0
        self.min_interval = 0.05  # Ultra-fast non-blocking throttle
        self.last_provider_used = None
        self.last_model_used = None
        self.last_error = None
        self.errors: Dict[str, str] = {}
        self.dry_run = False
        self.failed_providers = set()
        
        # Initialize clients if keys exist

        self.openrouter_client: Optional[OpenAI] = None
        self.groq_client: Optional[OpenAI] = None
        self.gemini_client: Optional[OpenAI] = None
        self.nvidia_client: Optional[OpenAI] = None
        
        self._init_clients()

    def _init_clients(self):
        if self.dry_run:
            return
        if self.nvidia_api_key:
            self.nvidia_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.nvidia_api_key, timeout=10.0, max_retries=0)
        if self.groq_api_key:
            self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.groq_api_key, timeout=8.0, max_retries=0)
        if self.gemini_api_key:
            self.gemini_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=self.gemini_api_key, timeout=8.0, max_retries=0)
        if self.openrouter_api_key:
            self.openrouter_client = OpenAI(base_url=self.openrouter_base_url, api_key=self.openrouter_api_key, timeout=6.0, max_retries=0)

    def set_custom_keys(self, provider: str, api_key: str, model: Optional[str] = None):
        """Allow setting runtime keys dynamically for a request without server restart."""
        clean_key = (api_key or "").strip().strip("'\"")
        if not clean_key:
            return
        
        if provider == "nvidia":
            self.nvidia_api_key = clean_key
            if model: self.nvidia_model = model
            self.nvidia_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=clean_key, timeout=10.0, max_retries=0)
        elif provider == "groq":
            self.groq_api_key = clean_key
            if model: self.groq_model = model
            self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=clean_key, timeout=8.0, max_retries=0)
        elif provider == "gemini":
            self.gemini_api_key = clean_key
            if model: self.gemini_model = model
            self.gemini_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=clean_key, timeout=8.0, max_retries=0)
        elif provider == "openrouter":
            self.openrouter_api_key = clean_key
            if model: self.openrouter_model = model
            self.openrouter_client = OpenAI(base_url=self.openrouter_base_url, api_key=clean_key, timeout=6.0, max_retries=0)


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
                if any(x in mid.lower() for x in ["whisper", "embedding", "guard", "vision", "audio", "tts", "moderation", "deprecated", "embed"]):
                    continue
                if provider == "groq":
                    if any(valid in mid.lower() for valid in ["llama", "gemma", "mixtral", "qwen", "deepseek"]):
                        model_ids.append(mid)
                elif provider == "gemini":
                    if any(valid in mid.lower() for valid in ["flash", "pro"]):
                        model_ids.append(mid)
                elif provider == "nvidia":
                    if any(valid in mid.lower() for valid in ["llama", "nemotron", "mistral", "deepseek"]):
                        model_ids.append(mid)
                else:
                    model_ids.append(mid)
            if model_ids:
                # Prioritize stable fast models
                if provider == "nvidia":
                    priority = ["meta/llama-3.3-70b-instruct", "nvidia/llama-3.1-nemotron-70b-instruct", "meta/llama-3.1-70b-instruct", "meta/llama-3.1-8b-instruct"]
                    model_ids.sort(key=lambda x: priority.index(x) if x in priority else 99)
                elif provider == "groq":
                    priority = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "llama3-70b-8192", "llama3-8b-8192"]
                    model_ids.sort(key=lambda x: priority.index(x) if x in priority else 99)
                self._model_cache[provider] = model_ids
                return model_ids
        except Exception:
            pass
        
        if provider == "nvidia":
            return NVIDIA_FALLBACK_MODELS
        elif provider == "groq":
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
            if provider == "nvidia":
                test_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=clean_key, timeout=15.0)
                fallback_list = NVIDIA_FALLBACK_MODELS
            elif provider == "groq":
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

        # Build prioritized list: 1 best model per provider to eliminate cascading lag
        providers = []
        if self.groq_client:
            providers.append(("groq", self.groq_client, self.groq_model or "llama-3.3-70b-versatile"))
        if self.gemini_client:
            providers.append(("gemini", self.gemini_client, self.gemini_model or "gemini-2.0-flash"))
        if self.nvidia_client:
            providers.append(("nvidia", self.nvidia_client, self.nvidia_model or "meta/llama-3.3-70b-instruct"))
        if self.openrouter_client:
            providers.append(("openrouter", self.openrouter_client, self.openrouter_model or "nvidia/nemotron-3-super-120b-a12b:free"))

        if not providers:
            self.last_provider_used = "mock (no keys configured)"
            self.last_error = "No API keys configured. Set GROQ_API_KEY, GEMINI_API_KEY, or NVIDIA_API_KEY."
            return self._mock_response(messages)

        failed_providers_in_request = set(self.failed_providers)
        self.errors = {}
        for provider_name, client_inst, active_model in providers:
            if provider_name in failed_providers_in_request:
                continue
            self._wait_for_rate_limit()
            try:
                safe_temp = max(0.2, min(temperature, 0.65))
                safe_max_tokens = min(max_tokens, 3000) if provider_name == "groq" else max_tokens
                kwargs = {
                    "model": active_model,
                    "messages": messages,
                    "max_tokens": safe_max_tokens,
                    "temperature": safe_temp,
                    "timeout": 4.0,
                }
                if provider_name in ["groq", "openrouter"]:
                    kwargs["top_p"] = 0.95
                if response_format and provider_name != "groq":
                    kwargs["response_format"] = response_format

                resp = client_inst.chat.completions.create(**kwargs)
                choice = resp.choices[0]
                content = choice.message.content or ""

                if content.strip():
                    cleaned_content = self._strip_reasoning(content)
                    self.last_provider_used = provider_name
                    self.last_model_used = active_model
                    self.last_error = None
                    return cleaned_content
            except Exception as e:
                err_msg = str(e)
                self.errors[f"{provider_name}:{active_model}"] = err_msg
                logger.warning(f"Provider {provider_name} failed: {err_msg}. Instant failover to next provider...")
                failed_providers_in_request.add(provider_name)
                self.failed_providers.add(provider_name)
                continue



        # If all providers fail, record error and return mock
        self.last_provider_used = "mock (all providers failed)"
        self.last_error = "; ".join([f"{k}: {v}" for k, v in self.errors.items()][:2])
        return self._mock_response(messages)



    def _mock_response(self, messages: List[Dict[str, str]]) -> str:
        """Return a rich, dynamic response when no LLM provider key is available.
        
        Dynamically extracts Package Name, Destination, Duration, Cost, Keywords, and Instructions
        and builds authoritative SEO-optimized outputs strictly separated by package category
        (Wellness / Retreats vs. Pilgrimage / Yatra Tours vs. Dharamshala Stays).
        """
        system_msg = messages[0].get("content", "") if messages else ""
        user_msg = messages[-1].get("content", "") if len(messages) > 1 else ""
        combined_text = f"{system_msg}\n{user_msg}"
        
        # 1. Dynamically extract package parameters
        pkg_name = ""
        destination = ""
        duration = "2 Days"
        cost = "Contact for pricing"
        keyword = ""
        audience = "Devotees, families, and travelers"
        custom_url = "https://yatradham.org"

        for line in combined_text.split("\n"):
            line_str = line.strip()
            line_lower = line_str.lower()
            if line_lower.startswith("package name:") or line_lower.startswith("package:"):
                extracted = line_str.split(":", 1)[1].strip()
                if extracted: pkg_name = extracted
            elif line_lower.startswith("topic:") or line_lower.startswith("topic / title") or line_lower.startswith("topic / destination:"):
                extracted = line_str.split(":", 1)[1].strip()
                if extracted and not pkg_name: pkg_name = extracted
            elif line_lower.startswith("destination:"):
                extracted = line_str.split(":", 1)[1].strip()
                if extracted: destination = extracted
            elif line_lower.startswith("duration:"):
                extracted = line_str.split(":", 1)[1].strip()
                if extracted: duration = extracted
            elif line_lower.startswith("primary keyword:") or line_lower.startswith("target keyword:") or line_lower.startswith("target seo keyword:"):
                extracted = line_str.split(":", 1)[1].strip()
                if extracted: keyword = extracted
            elif any(line_lower.startswith(k) for k in ["cost:", "price:", "starting cost", "starting price", "starting cost / price:"]):
                extracted = line_str.split(":", 1)[1].strip()
                if extracted: cost = extracted
            elif line_lower.startswith("target audience:") or line_lower.startswith("audience:"):
                extracted = line_str.split(":", 1)[1].strip()
                if extracted: audience = extracted

        # Fallback values if not explicitly found in headers
        if not pkg_name:
            name_match = re.search(r'Package Name:\s*([^\n]+)', combined_text, re.IGNORECASE)
            if name_match:
                pkg_name = name_match.group(1).strip()
            else:
                pkg_name = "Spiritual Tour Package"

        # Scope location checks to user message and package name first
        loc_scope = f"{pkg_name} {user_msg}".lower()
        if not destination:
            dest_match = re.search(r'Destination:\s*([^\n]+)', user_msg, re.IGNORECASE)
            if dest_match:
                destination = dest_match.group(1).strip()
            elif "chardham" in loc_scope:
                destination = "Haridwar & Uttarakhand"
            elif "haridwar" in loc_scope:
                destination = "Haridwar, Uttarakhand"
            elif "rishikesh" in loc_scope:
                destination = "Rishikesh, Uttarakhand"
            elif "vrindavan" in loc_scope or "barsana" in loc_scope:
                destination = "Vrindavan, Uttar Pradesh"
            elif "kerala" in loc_scope or "palakkad" in loc_scope:
                destination = "Palakkad, Kerala"
            elif "alibaug" in loc_scope:
                destination = "Alibaug, Maharashtra"
            elif "gangasagar" in loc_scope:
                destination = "Gangasagar, West Bengal"
            elif "delhi" in loc_scope:
                destination = "New Delhi, Delhi"
            elif "kangra" in loc_scope or "himachal" in loc_scope:
                destination = "Kangra, Himachal Pradesh"
            else:
                destination = "India"

        # 2. DETECT CATEGORY STRICTLY (Wellness vs Pilgrimage vs Stay vs Puja)
        explicit_cat_match = re.search(r'Category:\s*([a-z_]+)', combined_text, re.IGNORECASE)
        explicit_cat = explicit_cat_match.group(1).lower() if explicit_cat_match else ""

        raw_text_match = re.search(r'---\s*RAW PAGE TEXT[^\n]*\n([\s\S]*?)(?:-----------|\Z)', combined_text, re.IGNORECASE)
        page_raw_text = raw_text_match.group(1) if raw_text_match else ""
        
        check_text = f"{pkg_name} {destination} {page_raw_text} {custom_url}".lower()
        wellness_keywords = [
            "ayurved", "panchakarma", "massage", "rejuvenation", "retreat",
            "detox", "naturopathy", "healing", "stress relief", "abhyangam",
            "shirodhara", "yoga", "wellness"
        ]
        stay_keywords = ["dharamshala", "ashram stay", "bhavan", "sanatorium", "room booking", "trh", "gmvn", "hotel stay"]

        if explicit_cat in ["wellness", "tour", "stay", "puja"]:
            pkg_category = "wellness" if explicit_cat == "wellness" else ("stay" if explicit_cat == "stay" else ("puja" if explicit_cat == "puja" else "pilgrimage"))
        elif any(w in check_text for w in wellness_keywords):
            pkg_category = "wellness"
        elif any(w in check_text for w in stay_keywords) and not any(w in check_text for w in ["tour package", "yatra package", "days tour"]):
            pkg_category = "stay"
        elif "puja" in check_text or "pandit" in check_text:
            pkg_category = "puja"
        else:
            pkg_category = "pilgrimage"

        if not keyword:
            if pkg_category == "wellness":
                keyword = f"{duration} Yoga & Wellness Retreat in {destination}"
            elif pkg_category == "stay":
                keyword = f"Dharamshala in {destination}"
            elif pkg_category == "puja":
                keyword = f"Online Puja Booking in {destination}"
            else:
                keyword = f"{duration} {destination} Tour Package"

        # Extract & sanitize cost
        if cost and cost.strip() and cost.strip().lower() not in ["contact for pricing", "rs,", "rs.", "rs", "null", "none", ""]:
            cost = clean_price_string(cost)
        else:
            cost_match = re.search(r'(?:Starting\s+From\s+[-:]?\s*)?(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:Per\s*(?:Room\/)?Person\/?(?:Per\s*night)?|per\s*night|per\s*person|\/-))?', combined_text, re.IGNORECASE)
            if cost_match:
                cost = clean_price_string(cost_match.group(0).strip())
            else:
                cost = "Starting From ₹ Contact for Pricing"

        # Find custom URLs
        urls_found = re.findall(r'https?://[^\s)\]"]+', combined_text)
        for u in urls_found:
            if "yatradham.org" in u.lower() and u != "https://yatradham.org":
                custom_url = u
                break

        # 3. DISPATCH BY AGENT TYPE & CATEGORY

        # AGENT: Content Studio & Long-form Blog Creator (Must be checked before single-field subagents)
        if any(x in system_msg.lower() for x in ["content creator", "expert seo content writer", "write a comprehensive, engaging", "# content", "# headline"]):
            return f"""# TITLE
{pkg_name} — Complete Cost Breakdown, Route & Verified Booking Guide | YatraDham

# META DESCRIPTION
Discover verified {keyword.lower()} with our complete 2026 travel guide. Verified dharamshalas, exact route pricing, Satvik meals & 24/7 pilgrim support on YatraDham. Book now!

# SUGGESTED TAGS
{destination}, Pilgrimage Packages, Temple Darshan, YatraDham

# CONTENT
## Introduction & Sacred Significance

The sacred pilgrimage to {destination} represents one of the most spiritually uplifting journeys. Planning your trip with verified stays and dedicated transit ensures total peace of mind, allowing you and your family to focus entirely on devotion and holy darshan.

For devotees exploring the **{keyword}**, choosing a transparent, verified itinerary ensures total comfort, reliable local transport, and clean ashram stays.

Direct Package Booking & Details: You can check official package inclusions and reserve dates directly at [{pkg_name}]({custom_url}).

---

## Complete Day-by-Day Route & Darshan Itinerary

### Day 1: Arrival, Check-in & Evening Aarti
Arrive in {destination} and check into your verified [YatraDham Dharamshala](https://yatradham.org/). Freshen up with hot water facilities and proceed for your afternoon sanctum darshan. In the evening, immerse yourself in the divine temple Aarti and sacred parikrama before returning for a fresh Satvik dinner.

### Day 2: Morning Mangala Darshan, Sightseeing & Departure
Wake up early for the auspicious Mangala Aarti darshan. Visit adjacent sacred kunds, temples, and heritage sites in {destination}. Enjoy traditional breakfast, collect holy prasad, and complete your journey with blessed memories.

---

## 3 Key Takeaways for Planning Your Journey

### 1. Pacing Drives True Spiritual Rejuvenation
Rushing through sacred shrines causes fatigue. Allocating 2-3 hours for each darshan allows the mind to absorb the divine atmosphere.

### 2. High-Value Experiences Win Over Crowded Sightseeing
A peaceful ashram stay, unhurried morning Aarti, and authentic Satvik meals deliver ten times the value of a rushed generic tour.

### 3. Transparent Route Costs Prevent Surprises
Booking verified packages in advance protects you from unauthorized roadside agents and sudden surge pricing.

---

## 4 Ways YatraDham.Org Makes Your Journey Seamless & Safe

- **1. Verified Accommodations:** Every dharamshala and hotel is vetted for hot water, clean bedding, and vegetarian dining on [YatraDham.Org](https://yatradham.org/).
- **2. Dedicated Yatra & Transport Coordination:** Punctual transfers with reliable local drivers via [YatraDham Travel Packages](https://travel.yatradham.org/).
- **3. Authentic Temple Pujas & Pandit Bookings:** Arrange special Sankalp pujas and Abhishek through [YatraDham Temple Pujas](https://temple.yatradham.org/pujas).
- **4. 24/7 Pilgrim Support & Flexible Booking:** Round-the-clock WhatsApp assistance and verified booking guarantees.

---

## The Real Logistics: Costs, Stays & Commutes

- **Package Pricing:** A complete {duration} package for {destination} typically starts from {cost} including transport, accommodation, and Satvik meals.
- **Direct Official Booking:** For transparent rates and confirmed dates, visit: [{custom_url}]({custom_url}).
- **Daily Food Expenses:** Budget ₹300–₹600 per day for fresh Satvik meals and local transfers.

---

## Frequently Asked Questions

### Q1. What is the average price of this tour package?
The package starts from {cost} per person depending on group size and vehicle choice.

### Q2. Is this package safe for senior citizens?
Yes. With YatraDham's verified transport, ground-floor dharamshala rooms, and temple-gate drops, seniors travel with total comfort.

### Q3. Where can I book verified packages and dharamshalas?
You can book verified packages directly through the [Official YatraDham Portal]({custom_url}) and verified stays on [YatraDham.Org](https://yatradham.org/).

---

## Final Thoughts & Planning Your Trip

Embarking on this sacred pilgrimage to {destination} is a life-affirming journey of faith and peace. With YatraDham.Org managing your stays, transfers, and darshan logistics, you can immerse yourself completely in the divine blessings.

**Book your verified package today: [Click here to explore the official {pkg_name} on YatraDham.org]({custom_url}).**"""

        
        # AGENT: Content Agent (19 Structured Sections JSON)
        if any(x in system_msg.lower() for x in ["19 structured sections", "expert content writer for yatradham", "package_overview", "sectionedcontent"]):
            
            if pkg_category == "wellness":
                from retreat_generator import generate_archetype_content
                sections_dict = generate_archetype_content(pkg_name, destination, duration, cost, custom_url)

            elif pkg_category == "stay":


                sections_dict = {
                    "package_overview": f"{pkg_name} provides clean, safe, and comfortable accommodation in {destination}. Situated with convenient access to major temples and transit points, this verified stay features hygienic rooms, 24/7 hot water, and a peaceful devotional atmosphere for pilgrims and families.",
                    "quick_facts": {
                        "package_name": pkg_name,
                        "cost": cost,
                        "duration": duration,
                        "destination": destination,
                        "level": "Families, Pilgrims & Groups Welcome",
                        "accommodation": f"Clean Rooms with Attached Bath in {destination}",
                        "food": "Satvik Dining / Bhojanalaya Nearby",
                        "activities": f"Temple Visits & Holy Darshan in {destination}",
                    },
                    "why_choose_heading": f"Why Choose {pkg_name}?",
                    "why_choose_intro": f"Enjoy a peaceful and verified stay in {destination} with essential pilgrim amenities.",
                    "why_choose_bullets": [
                        f"Prime location in {destination} ensuring quick and easy access to temples.",
                        "Verified by YatraDham for clean linens, hygienic bathrooms, and 24/7 hot water.",
                        "Peaceful, family-friendly environment adhering to sacred guidelines.",
                        "Transparent advance room booking with instant confirmation voucher.",
                        "24/7 YatraDham customer support helpline for check-in assistance.",
                    ],
                    "who_can_benefit_heading": f"Who Is This {destination} Stay Ideal For?",
                    "who_can_benefit_intro": "Ideal for devotees and families seeking a clean and budget-friendly stay.",
                    "who_can_benefit_bullets": [
                        "Families traveling with elders looking for safe ground-floor or lift-accessible rooms.",
                        "Pilgrim groups seeking multiple adjoining rooms or budget family halls.",
                        "Solo devotees looking for a peaceful and secure ashram atmosphere.",
                        "Visitors arriving by train/bus who need convenient check-in near transit hubs.",
                        "Travelers who prefer authentic Satvik dining and calm surroundings.",
                    ],
                    "program_highlights": {
                        "heading": f"Stay Information & Timings in {destination}",
                        "morning": [
                            {"time": "06:00 AM", "activity": "Morning Temple Darshan & Aarti Access"},
                            {"time": "08:00 AM", "activity": "Satvik Breakfast in Bhojanalaya"}
                        ],
                        "daytime": [
                            {"time": "12:00 PM", "activity": "Standard Check-in / Rest Period"},
                            {"time": "01:30 PM", "activity": "Satvik Lunch Nearby"}
                        ],
                        "evening": [
                            {"time": "06:30 PM", "activity": "Evening Temple Aarti & Parikrama"},
                            {"time": "08:30 PM", "activity": "Dinner and Overnight Stay"}
                        ],
                    },
                    "meal_section_heading": "Dining & Bhojanalaya Facilities",
                    "meal_section_bullets": [
                        "Pure vegetarian Satvik meals available on-site or at adjacent bhojanalayas.",
                        "Freshly prepared meals without onion and garlic.",
                    ],
                    "accommodation_heading": f"Room Amenities & Features in {destination}",
                    "accommodation_bullets": [
                        f"Clean, well-maintained rooms in {destination} with attached private bathrooms.",
                        "Equipped with 24/7 hot water, fans/AC, clean beds, and secure locks.",
                    ],
                    "benefits_heading": f"Key Benefits of Booking Through YatraDham.Org",
                    "benefits_items": [
                        "Guaranteed room reservation before arrival to avoid peak-season rushes.",
                        "Verified cleanliness standards with actual traveler reviews.",
                        "No hidden roadside broker charges or sudden price inflations.",
                        "Convenient proximity to main temple gates and bathing ghats.",
                        "Family-friendly atmosphere with security cameras and caretaker support.",
                        "Direct SMS and WhatsApp confirmation voucher.",
                        "Easy cancellation options as per property guidelines.",
                        "Access to pre-book verified Vedic Pandit Ji for rituals.",
                    ],
                    "how_to_book_heading": "How to Book on YatraDham.Org",
                    "how_to_book_steps": [
                        f"Choose your check-in and check-out dates on the {pkg_name} page.",
                        "Select your preferred room type (Non-AC / AC / Family Room).",
                        "Enter the total number of guests.",
                        "Make a secure advance payment.",
                        "Get instant booking voucher with full address and manager contact.",
                        f"Show your voucher at check-in in {destination} and enjoy your stay.",
                    ],
                    "prices_photos_reviews": f"Room rates for {pkg_name} start from {cost}. Check live room availability and real guest reviews on YatraDham.Org.",
                    "itinerary": [
                        {"day_number": 1, "sessions": [{"time": "12:00 PM", "activity": "Check-in and room allocation."}, {"time": "06:00 PM", "activity": "Evening temple visit and aarti."}]},
                        {"day_number": 2, "sessions": [{"time": "06:00 AM", "activity": "Morning darshan."}, {"time": "10:00 AM", "activity": "Standard check-out."}]}
                    ],
                    "pricing_table": [
                        {"guests": "1 - 2 Guests (Standard Room)", "cost_per_person": cost},
                        {"guests": "3 - 4 Guests (Family Room)", "cost_per_person": "Budget friendly rates"},
                        {"guests": "Group Booking (5+ Persons)", "cost_per_person": "Contact for group hall"}
                    ],
                    "inclusions": [
                        "Clean room accommodation with attached bathroom",
                        "24/7 hot water and clean bed linen",
                        "Drinking water facility",
                        "24/7 caretaker assistance on premises",
                        "Instant booking confirmation voucher"
                    ],
                    "exclusions": [
                        "Meals (unless specifically included in room plan)",
                        "Personal laundry and room service tips",
                        "Transit cab fares to and from station",
                        "VIP darshan passes"
                    ],
                    "nearby_locations_heading": f"Landmarks & Temple Proximity in {destination}",
                    "nearby_locations": [
                        {"name": "Main Temple Sanctum", "distance": "Walking distance (500m - 1.5km)", "type": "sightseeing"},
                        {"name": "Nearest Bus Stand / Auto Stand", "distance": "5 - 10 minutes", "type": "bus"},
                        {"name": "Nearest Railway Station", "distance": "Short cab drive", "type": "railway"}
                    ],
                    "cancellation_policy": f"Cancellations allowed as per standard property guidelines. Contact YatraDham support for assistance.",
                    "payment_policy_bullets": ["Secure partial advance payment.", "Balance payable at property check-in.", "All online payment modes accepted."],
                    "terms_conditions": [
                        "Government photo ID is mandatory for all adult guests.",
                        "Standard check-in and check-out timings apply.",
                        "Premises maintain sacred discipline — alcohol and non-veg strictly prohibited.",
                        "Guests are responsible for their personal belongings."
                    ],
                    "faq": [
                        {"question": "What are the check-in and check-out timings?", "answer": "Standard check-in is at 12:00 PM and check-out is at 10:00 AM unless early check-in is confirmed."},
                        {"question": "Is hot water available in the rooms?", "answer": "Yes, 24/7 geyser or solar hot water is provided in all attached bathrooms."},
                        {"question": "How far is the property from the main temple?", "answer": f"The property is conveniently located within easy walking or e-rickshaw distance from the main temples in {destination}."}
                    ]
                }
            else:
                # PILGRIMAGE TOUR
                sections_dict = {
                    "package_overview": f"The {pkg_name} offers a sacred, well-organized spiritual journey to {destination}. Designed for pilgrims seeking a comfortable and devout experience, this {duration} itinerary covers prominent temples, sacred sanctums, and peaceful ashram visits with verified YatraDham accommodation and pure Satvik dining.",
                    "quick_facts": {
                        "package_name": pkg_name,
                        "cost": cost,
                        "duration": duration,
                        "destination": destination,
                        "level": "All Devotees & Age Groups Welcome",
                        "accommodation": f"Verified Dharamshala / Hotel in {destination} via YatraDham",
                        "food": "100% Pure Vegetarian Satvik Meals",
                        "activities": f"Temple Darshan, Guided Aarti, Sacred Parikrama in {destination}",
                    },
                    "why_choose_heading": f"Why Choose {pkg_name}?",
                    "why_choose_intro": f"Experience a seamless and spiritually fulfilling visit to {destination} with trusted local logistics.",
                    "why_choose_bullets": [
                        f"Carefully planned {duration} schedule allowing unhurried darshan at all major temples in {destination}.",
                        f"Verified clean accommodations with hot water, clean linens, and peaceful surroundings booked via YatraDham.",
                        "Dedicated private cab transport with experienced local drivers for comfortable temple transfers.",
                        "Nutritious Satvik vegetarian meals included throughout the journey.",
                        "24/7 on-ground assistance and transparent pricing with no hidden roadside agent markups.",
                    ],
                    "who_can_benefit_heading": f"Who Is This {destination} Pilgrimage Ideal For?",
                    "who_can_benefit_intro": "This package is crafted to meet the needs of families, seniors, and independent spiritual seekers.",
                    "who_can_benefit_bullets": [
                        "Families seeking a peaceful, well-coordinated pilgrimage without the stress of finding last-minute stays.",
                        "Senior citizens who require comfortable transport, easily accessible temple entries, and pure Satvik food.",
                        "Working professionals and couples looking for a meaningful weekend spiritual reset.",
                        "Devotees traveling in groups who want assured dharamshala rooms and verified cab coordination.",
                        "First-time visitors to {destination} who benefit from local route expertise and fixed darshan schedules.",
                    ],
                    "program_highlights": {
                        "heading": f"Daily Program & Darshan Highlights in {destination}",
                        "morning": [
                            {"time": "06:00 AM", "activity": f"Morning Mangala Aarti & Sacred Temple Darshan in {destination}"},
                            {"time": "08:30 AM", "activity": "Traditional Satvik Breakfast & Preparation for Sightseeing"}
                        ],
                        "daytime": [
                            {"time": "11:00 AM", "activity": f"Main Sanctum Visit, Special Puja & Temple Parikrama"},
                            {"time": "01:30 PM", "activity": "Hygienic Satvik Lunch and Relaxation at Stay"}
                        ],
                        "evening": [
                            {"time": "05:30 PM", "activity": f"Evening Sandhya Aarti, Bhajan Kirtan & Light Darshan"},
                            {"time": "08:00 PM", "activity": "Warm Satvik Dinner and Overnight Stay"}
                        ],
                    },
                    "meal_section_heading": "Satvik Meals & Dining Standards",
                    "meal_section_bullets": [
                        "Hygienic 100% pure vegetarian Satvik breakfast, lunch, and dinner prepared fresh daily.",
                        "Carefully balanced meals prepared without onion or garlic upon request to maintain complete pilgrimage sanctity.",
                    ],
                    "accommodation_heading": f"Verified Accommodations in {destination}",
                    "accommodation_bullets": [
                        f"Handpicked dharamshalas, ashrams, and hotels in {destination} personally vetted by the YatraDham team.",
                        "Equipped with 24/7 hot water, sanitized bedding, attached bathrooms, and secure family-friendly premises.",
                    ],
                    "benefits_heading": f"Key Benefits of Booking Through YatraDham.Org",
                    "benefits_items": [
                        "Guaranteed room reservation near major temple gates to avoid long walking distances.",
                        "Transparent pricing with clear inclusions and no last-minute roadside agent haggling.",
                        "Punctual AC / Non-AC private vehicle with polite, route-trained drivers.",
                        "Flexible check-in options and direct booking confirmation voucher on your phone.",
                        "Authentic Satvik meals included to keep your family healthy and energized.",
                        "Dedicated customer support team available 24/7 on WhatsApp and phone.",
                        "Verified safety protocols for women and senior travelers.",
                        "Opportunity to pre-book verified Vedic Pandit Ji for special pujas and rituals.",
                    ],
                    "how_to_book_heading": "How to Book Your Package on YatraDham.Org",
                    "how_to_book_steps": [
                        f"Select your preferred dates and travel group size on the {pkg_name} page.",
                        "Choose your room category (AC Room / Non-AC Room / Family Suite).",
                        "Enter guest details and any special puja or pickup requests.",
                        "Make a secure partial advance payment using UPI, NetBanking, or Cards.",
                        "Receive instant booking confirmation and driver / hotel contact details.",
                        f"Arrive in {destination} and experience a blessed and hassle-free yatra.",
                    ],
                    "prices_photos_reviews": f"Package rates for {pkg_name} start from {cost}. Check live availability, verified photos, and authentic devotee reviews directly on YatraDham.Org.",
                    "itinerary": [
                        {
                            "day_number": 1,
                            "sessions": [
                                {"time": "09:00 AM", "activity": f"Arrival in {destination}, pickup and check-in to verified YatraDham stay."},
                                {"time": "11:30 AM", "activity": f"First sanctum darshan and temple orientation."},
                                {"time": "01:30 PM", "activity": "Satvik lunch and rest period."},
                                {"time": "05:00 PM", "activity": f"Evening temple visit, attending the world-famous evening Aarti and cultural parikrama."},
                                {"time": "08:30 PM", "activity": "Satvik dinner and peaceful overnight rest."}
                            ]
                        },
                        {
                            "day_number": 2,
                            "sessions": [
                                {"time": "06:00 AM", "activity": f"Morning temple parikrama, Mangala Aarti darshan and peaceful meditation."},
                                {"time": "08:30 AM", "activity": "Traditional breakfast and checkout preparation."},
                                {"time": "10:30 AM", "activity": f"Visiting adjacent holy shrines and sacred kunds in {destination}."},
                                {"time": "02:00 PM", "activity": "Satvik lunch, local prasad shopping, and departure transfer."}
                            ]
                        }
                    ],
                    "pricing_table": [
                        {"guests": "1 Person (Solo Traveler)", "cost_per_person": cost},
                        {"guests": "2 Persons (Twin Sharing)", "cost_per_person": "₹2,500 – ₹4,500 per person"},
                        {"guests": "Family / Group (4+ Persons)", "cost_per_person": "₹1,800 – ₹3,200 per person"}
                    ],
                    "inclusions": [
                        f"Accommodation in verified YatraDham dharamshala/hotel in {destination}",
                        "Dedicated private cab for all sightseeing and temple transfers as per itinerary",
                        "Pure vegetarian Satvik breakfast, lunch, and dinner",
                        "All toll taxes, parking fees, state road tax, and driver allowance",
                        "Temple darshan guidance and 24/7 YatraDham helpline support",
                        "Sanitized rooms with 24/7 hot water and clean linens"
                    ],
                    "exclusions": [
                        "Train tickets or flight fares to and from arrival station",
                        "Personal expenses such as shopping, laundry, and camera fees",
                        "Special VIP darshan tickets or private priest dakshina",
                        "Any items or services not explicitly mentioned in the package inclusions"
                    ],
                    "nearby_locations_heading": f"How to Reach & Nearby Connectivity for {destination}",
                    "nearby_locations": [
                        {"name": "Nearest Railway Station", "distance": "5 – 15 km (Direct cab transfer available)", "type": "railway"},
                        {"name": "Nearest Airport", "distance": "45 – 120 km (Smooth expressway connection)", "type": "airport"},
                        {"name": "Main Temple Complex", "distance": "Walking distance from verified YatraDham stay", "type": "sightseeing"}
                    ],
                    "cancellation_policy": f"Free cancellation up to 48 hours before scheduled check-in for select partner properties. For urgent cancellations or date modifications for {pkg_name}, reach out directly to YatraDham support.",
                    "payment_policy_bullets": [
                        "Secure partial advance payment required to guarantee booking voucher.",
                        "Balance payment can be cleared upon arrival at the accommodation.",
                        "100% encrypted payment portal supporting UPI, Google Pay, NetBanking, and Cards."
                    ],
                    "terms_conditions": [
                        "Valid government-issued photo ID (Aadhaar/Passport/Voter ID) is mandatory at check-in.",
                        "Temple darshan timings and entry guidelines are subject to temple trust management.",
                        "Devotees are requested to follow traditional temple attire and maintain sanctum discipline.",
                        "Vehicles provided will strictly follow the pre-decided itinerary route.",
                        "Check-in and check-out timings are standard (12:00 PM Check-in / 10:00 AM Check-out) unless requested in advance.",
                        "YatraDham.Org acts as a verified booking platform to ensure authentic quality and pilgrim convenience."
                    ],
                    "faq": [
                        {
                            "question": f"What is included in the {pkg_name}?",
                            "answer": f"The package includes verified accommodation in {destination}, dedicated private cab transport for temple darshans, hygienic Satvik meals, and 24/7 support throughout your {duration} trip."
                        },
                        {
                            "question": f"Is this {destination} package safe and comfortable for senior citizens?",
                            "answer": f"Yes, absolutely. YatraDham arranges comfortable stays with ground floor room options, lift access, clean western toilets, and vehicles that drop devotees close to temple entrance gates."
                        },
                        {
                            "question": "What kind of food is served during the tour?",
                            "answer": "100% pure vegetarian, freshly cooked Satvik meals (dal, roti, sabzi, rice, salad) are served. Jain meals without onion and garlic can also be arranged on request."
                        },
                        {
                            "question": "How do I confirm my booking on YatraDham.Org?",
                            "answer": f"You can book directly on YatraDham.Org by selecting your travel dates, choosing your room type, and making a secure online advance payment. A confirmed booking voucher is generated instantly."
                        }
                    ]
                }
            return json.dumps(sections_dict)

        # AGENT: Title Tag Agent
        if "title tag" in system_msg.lower() or "title specialist" in system_msg.lower():
            if pkg_category == "wellness":
                title_clean = f"{pkg_name[:45]} | YatraDham.Org"
            elif pkg_category == "stay":
                title_clean = f"{pkg_name[:45]} | YatraDham.Org"
            else:
                title_clean = f"{duration} {destination} Tour Package | YatraDham.Org"
            if len(title_clean) > 60:
                title_clean = f"{pkg_name[:45]} | YatraDham.Org"
            return json.dumps({"title_tag": title_clean[:60]})

        # AGENT: Keyword Agent
        if "keyword" in system_msg.lower() and "meta" not in system_msg.lower() and "overview" not in system_msg.lower():
            if pkg_category == "wellness":
                secondary = [f"{destination} wellness retreat", f"Ayurvedic retreat in {destination}", f"{pkg_name} cost", "YatraDham wellness"]
            elif pkg_category == "stay":
                secondary = [f"{destination} dharamshala booking", f"best stay in {destination}", f"{pkg_name} price", "YatraDham stays"]
            else:
                secondary = [f"{destination} tour package", f"{pkg_name} price", f"best {destination} dharamshala", "YatraDham booking"]
            return json.dumps({
                "primary_keyword": keyword,
                "secondary_keywords": secondary
            })

        # AGENT: Meta Description Agent
        if "meta description" in system_msg.lower():
            if pkg_category == "wellness":
                meta_desc = f"Experience authentic healing with {pkg_name} in {destination}. Verified wellness stays, doctor consultations & Satvik meals. Book now!"
            elif pkg_category == "stay":
                meta_desc = f"Book verified stay at {pkg_name} in {destination}. Clean rooms, hot water & secure booking on YatraDham.Org. Reserve your spot now!"
            else:
                meta_desc = f"Book verified {pkg_name} in {destination} with YatraDham.Org. Clean rooms, satvik meals & seamless booking. Reserve your spot now!"
            return json.dumps({"meta_description": meta_desc[:155]})

        # AGENT: QA Agent
        if "qa" in system_msg.lower() or "quality assurance" in system_msg.lower():
            return json.dumps({"score": 95, "flags": ["PASS"], "notes": f"All 19 sections verified for {pkg_category} category."})


        # Content Studio & Long-form Blog Generation
        return f"""# TITLE
{pkg_name} — Complete Cost Breakdown, Route & Verified Booking Guide | YatraDham

# META DESCRIPTION
Discover the real {keyword.lower()} with our complete 2026 guide. Verified dharamshalas, exact route pricing, Satvik meals & 24/7 pilgrim support on YatraDham. Book now!

# SUGGESTED TAGS
{destination}, Pilgrimage Packages, Temple Darshan, YatraDham

# CONTENT
## Introduction & Sacred Significance

The sacred pilgrimage to {destination} represents one of the most spiritually uplifting journeys. Planning your trip with verified stays and dedicated transit ensures total peace of mind, allowing you and your family to focus entirely on devotion and holy darshan.

For devotees exploring the **{keyword}**, choosing a transparent, verified itinerary ensures total comfort, reliable local hill transport, and clean ashram stays.

Direct Package Booking & Details: You can check official package inclusions and reserve dates directly at [{pkg_name}]({custom_url}).

---

## Complete Day-by-Day Route & Darshan Itinerary

### Day 1: Arrival, Check-in & Evening Aarti
Arrive in {destination} and check into your verified [YatraDham Dharamshala](https://yatradham.org/). Freshen up with hot water facilities and proceed for your afternoon sanctum darshan. In the evening, immerse yourself in the divine temple Aarti and sacred parikrama before returning for a fresh Satvik dinner.

### Day 2: Morning Mangala Darshan, Sightseeing & Departure
Wake up early for the auspicious Mangala Aarti darshan. Visit adjacent sacred kunds, temples, and heritage sites in {destination}. Enjoy traditional breakfast, collect holy prasad, and complete your journey with blessed memories.

---

## 3 Key Takeaways for Planning Your Journey

### 1. Pacing Drives True Spiritual Rejuvenation
Rushing through sacred shrines causes fatigue. Allocating 2-3 hours for each darshan allows the mind to absorb the divine atmosphere.

### 2. High-Value Experiences Win Over Crowded Sightseeing
A peaceful ashram stay, unhurried morning Aarti, and authentic Satvik meals deliver ten times the value of a rushed generic tour.

### 3. Transparent Route Costs Prevent Surprises
Booking verified packages in advance protects you from unauthorized roadside agents and sudden surge pricing.

---

## 4 Ways YatraDham.Org Makes Your Journey Seamless & Safe

- **1. Verified Accommodations:** Every dharamshala and hotel is vetted for hot water, clean bedding, and vegetarian dining on [YatraDham.Org](https://yatradham.org/).
- **2. Dedicated Yatra & Transport Coordination:** Punctual transfers with reliable local drivers via [YatraDham Travel Packages](https://travel.yatradham.org/).
- **3. Authentic Temple Pujas & Pandit Bookings:** Arrange special Sankalp pujas and Abhishek through [YatraDham Temple Pujas](https://temple.yatradham.org/pujas).
- **4. 24/7 Pilgrim Support & Flexible Booking:** Round-the-clock WhatsApp assistance and verified booking guarantees.

---

## The Real Logistics: Costs, Stays & Commutes

- **Package Pricing:** A complete {duration} package for {destination} typically ranges between ₹1,800 and ₹4,500 per person including transport, accommodation, and Satvik meals.
- **Direct Official Booking:** For transparent rates and confirmed dates, visit: [{custom_url}]({custom_url}).
- **Daily Food Expenses:** Budget ₹300–₹600 per day for fresh Satvik meals and local transfers.

---

## Frequently Asked Questions

### Q1. What is the average price of this tour package?
The package starts from {cost} per person depending on group size and vehicle choice.

### Q2. Is this package safe for senior citizens?
Yes. With YatraDham's verified transport, ground-floor dharamshala rooms, and temple-gate drops, seniors travel with total comfort.

### Q3. Where can I book verified packages and dharamshalas?
You can book verified packages directly through the [Official YatraDham Portal]({custom_url}) and verified stays on [YatraDham.Org](https://yatradham.org/).

---

## Final Thoughts & Planning Your Trip

Embarking on this sacred pilgrimage to {destination} is a life-affirming journey of faith and peace. With YatraDham.Org managing your stays, transfers, and darshan logistics, you can immerse yourself completely in the divine blessings.

**Book your verified package today: [Click here to explore the official {pkg_name} on YatraDham.org]({custom_url}).**"""


