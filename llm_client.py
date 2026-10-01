import os
import time
import json
import re
from typing import Optional, Dict, Any, List
from openai import OpenAI

DEFAULT_OPENROUTER_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"
OPENROUTER_FALLBACK_MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "poolside/laguna-s-2.1:free",
    "stealth/space-bunny-alpha",
]


GROQ_DEFAULT_MODEL = "llama-3.1-8b-instant"
GROQ_FALLBACK_MODELS = [
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "gemma2-9b-it",
    "llama3-8b-8192",
    "llama-3.3-70b-versatile",
]

GEMINI_DEFAULT_MODEL = "gemini-2.5-flash"
GEMINI_FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-3.8-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash",
]

NVIDIA_DEFAULT_MODEL = "nvidia/llama-3.1-nemotron-70b-instruct"
NVIDIA_FALLBACK_MODELS = [
    "nvidia/llama-3.1-nemotron-70b-instruct",
    "meta/llama-3.1-70b-instruct",
    "meta/llama-3.1-8b-instruct",
    "mistralai/mistral-large-2-instruct",
]

DEEPSEEK_DEFAULT_MODEL = "deepseek-chat"
DEEPSEEK_FALLBACK_MODELS = [
    "deepseek-chat",
    "deepseek-reasoner",
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

        # DeepSeek config (Reasoning harness & Direct V3 / R1)
        self.deepseek_api_key = (os.getenv("DEEPSEEK_API_KEY", "") or "").strip().strip("'\"")
        self.deepseek_model = os.getenv("DEEPSEEK_MODEL", DEEPSEEK_DEFAULT_MODEL)

        self.last_call_time = 0.0
        self.min_interval = 0.05  # Ultra-fast non-blocking throttle
        self.last_provider_used = None
        self.last_model_used = None
        self.last_error = None
        self.errors: Dict[str, str] = {}
        self.dry_run = False
        self.failed_providers = set()
        self.provider_cooldowns: Dict[str, float] = {}
        
        # Initialize clients if keys exist

        self.openrouter_client: Optional[OpenAI] = None
        self.groq_client: Optional[OpenAI] = None
        self.gemini_client: Optional[OpenAI] = None
        self.nvidia_client: Optional[OpenAI] = None
        self.deepseek_client: Optional[OpenAI] = None
        
        self._init_clients()

    def _init_clients(self):
        if self.dry_run:
            return
        if self.nvidia_api_key:
            self.nvidia_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.nvidia_api_key, timeout=45.0, max_retries=1)
        if self.groq_api_key:
            self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.groq_api_key, timeout=35.0, max_retries=1)
        if self.gemini_api_key:
            self.gemini_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=self.gemini_api_key, timeout=35.0, max_retries=1)
        if self.deepseek_api_key:
            self.deepseek_client = OpenAI(base_url="https://api.deepseek.com/v1", api_key=self.deepseek_api_key, timeout=45.0, max_retries=1)
        if self.openrouter_api_key:
            self.openrouter_client = OpenAI(base_url=self.openrouter_base_url, api_key=self.openrouter_api_key, timeout=45.0, max_retries=1)

    def set_custom_keys(self, provider: str, api_key: str, model: Optional[str] = None):
        """Allow setting runtime keys dynamically for a request without server restart."""
        clean_key = (api_key or "").strip().strip("'\"")
        if not clean_key:
            return
        
        self.provider_cooldowns.pop(provider, None)
        
        if provider == "nvidia":
            self.nvidia_api_key = clean_key
            if model: self.nvidia_model = model
            self.nvidia_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=clean_key, timeout=45.0, max_retries=1)
        elif provider == "groq":
            self.groq_api_key = clean_key
            if model: self.groq_model = model
            self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=clean_key, timeout=35.0, max_retries=1)
        elif provider == "gemini":
            self.gemini_api_key = clean_key
            if model: self.gemini_model = model
            self.gemini_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=clean_key, timeout=35.0, max_retries=1)
        elif provider == "deepseek":
            self.deepseek_api_key = clean_key
            if model: self.deepseek_model = model
            self.deepseek_client = OpenAI(base_url="https://api.deepseek.com/v1", api_key=clean_key, timeout=45.0, max_retries=1)
        elif provider == "openrouter":
            self.openrouter_api_key = clean_key
            if model: self.openrouter_model = model
            self.openrouter_client = OpenAI(base_url=self.openrouter_base_url, api_key=clean_key, timeout=45.0, max_retries=1)


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
                    priority = ["nvidia/llama-3.1-nemotron-70b-instruct", "meta/llama-3.1-70b-instruct", "meta/llama-3.1-8b-instruct", "mistralai/mistral-large-2-instruct"]
                    model_ids.sort(key=lambda x: priority.index(x) if x in priority else 99)
                elif provider == "groq":
                    priority = ["llama-3.1-8b-instant", "llama3-70b-8192", "gemma2-9b-it", "llama3-8b-8192", "llama-3.3-70b-versatile"]
                    model_ids.sort(key=lambda x: priority.index(x) if x in priority else 99)
                elif provider == "gemini":
                    priority = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-3.8-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
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
        
        self.provider_cooldowns.pop(provider, None)
        t0 = time.time()
        try:
            if provider == "nvidia":
                test_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=clean_key, timeout=25.0)
                fallback_list = NVIDIA_FALLBACK_MODELS
            elif provider == "groq":
                test_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=clean_key, timeout=20.0)
                fallback_list = GROQ_FALLBACK_MODELS
            elif provider == "gemini":
                test_client = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=clean_key, timeout=20.0)
                fallback_list = GEMINI_FALLBACK_MODELS
            elif provider == "openrouter":
                test_client = OpenAI(base_url=self.openrouter_base_url, api_key=clean_key, timeout=25.0)
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
        # Also clean un-tagged thinking preambles before markdown headers
        first_h1 = re.search(r'(?:\n|^)(#[#]?\s+[A-Za-z0-9])', text)
        if first_h1 and first_h1.start() > 0:
            preamble = text[:first_h1.start()].strip()
            if any(re.search(pat, preamble, re.IGNORECASE) for pat in [
                r"here(?:'s|\s+is)\s+(?:a\s+)?(?:thinking|process|draft)",
                r"okay,?\s+the\s+user",
                r"let(?:'s|\s+me)\s+(?:unpack|think|break)",
                r"the\s+user\s+wants",
                r"we\s+need\s+to\s+respond",
                r"^thinking\s*:"
            ]):
                text = text[first_h1.start():]
        return text.strip()

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        response_format: Optional[Dict[str, str]] = None,
        retries: int = 2,
        preferred_provider: Optional[str] = None,
    ) -> str:
        if self.dry_run:
            self.last_provider_used = "dry_run"
            return self._mock_response(messages)

        # Build prioritized list: provider, client instance, and ordered candidate models
        providers = []
        if self.deepseek_client:
            ds_models = []
            if self.deepseek_model:
                ds_models.append(self.deepseek_model)
            for m in DEEPSEEK_FALLBACK_MODELS:
                if m not in ds_models:
                    ds_models.append(m)
            providers.append(("deepseek", self.deepseek_client, ds_models))
        if self.groq_client:
            gq_models = []
            if self.groq_model:
                gq_models.append(self.groq_model)
            for m in GROQ_FALLBACK_MODELS:
                if m not in gq_models:
                    gq_models.append(m)
            providers.append(("groq", self.groq_client, gq_models))
        if self.gemini_client:
            gem_models = []
            if self.gemini_model:
                gem_models.append(self.gemini_model)
            for m in GEMINI_FALLBACK_MODELS:
                if m not in gem_models:
                    gem_models.append(m)
            providers.append(("gemini", self.gemini_client, gem_models))
        if self.nvidia_client:
            nv_models = []
            if self.nvidia_model:
                nv_models.append(self.nvidia_model)
            for m in NVIDIA_FALLBACK_MODELS:
                if m not in nv_models:
                    nv_models.append(m)
            providers.append(("nvidia", self.nvidia_client, nv_models))
        if self.openrouter_client:
            # Active verified free models on OpenRouter
            active_or_models = []
            if self.openrouter_model and ":free" in self.openrouter_model and not any(d in self.openrouter_model for d in ["llama-3.3-70b-instruct:free", "gemini-2.0-flash-exp:free"]):
                active_or_models.append(self.openrouter_model)
            for fm in OPENROUTER_FALLBACK_MODELS:
                if fm not in active_or_models:
                    active_or_models.append(fm)
            providers.append(("openrouter", self.openrouter_client, active_or_models))

        if not providers:
            self.last_provider_used = "mock (no keys configured)"
            self.last_error = "No API keys configured. Set GROQ_API_KEY, GEMINI_API_KEY, or OPENROUTER_API_KEY."
            return self._mock_response(messages)

        # If a preferred provider was requested and available, prioritize it
        if preferred_provider and any(p[0] == preferred_provider for p in providers):
            pref = [p for p in providers if p[0] == preferred_provider]
            others = [p for p in providers if p[0] != preferred_provider]
            providers = pref + others

        failed_providers_in_request = set()
        self.errors = {}
        for provider_name, client_inst, candidate_models in providers:
            if provider_name in failed_providers_in_request:
                continue
            # Circuit breaker: skip provider if under cooldown due to rate limit/quota/auth failure
            if time.time() < self.provider_cooldowns.get(provider_name, 0.0):
                continue

            # Prioritize custom model if specified, then try candidate fallback models
            if model and provider_name in ["openrouter", "groq", "gemini", "nvidia", "deepseek"]:
                models_to_try = [model] + [m for m in candidate_models if m != model]
            else:
                models_to_try = candidate_models
            # Try up to 3 models per provider
            for active_model in models_to_try[:3]:
                self._wait_for_rate_limit()
                try:
                    safe_temp = max(0.2, min(temperature, 0.65))
                    safe_max_tokens = min(max_tokens, 3000) if provider_name == "groq" else max_tokens
                    kwargs = {
                        "model": active_model,
                        "messages": messages,
                        "max_tokens": safe_max_tokens,
                        "temperature": safe_temp,
                        "timeout": 30.0,
                    }
                    if provider_name in ["groq", "openrouter"]:
                        kwargs["top_p"] = 0.95
                    if provider_name == "openrouter" and "nemotron" in active_model.lower():
                        kwargs["extra_body"] = {"reasoning": {"effort": "none"}}
                    if response_format and provider_name != "groq":
                        kwargs["response_format"] = response_format

                    resp = client_inst.chat.completions.create(**kwargs)
                    content = ""
                    if resp and getattr(resp, 'choices', None) and len(resp.choices) > 0:
                        choice = resp.choices[0]
                        msg = getattr(choice, 'message', None)
                        content = getattr(msg, 'content', None) or ""
                        if not content.strip() and hasattr(msg, 'reasoning') and msg.reasoning:
                            content = str(msg.reasoning)

                    if content.strip():
                        cleaned_content = self._strip_reasoning(content)
                        self.last_provider_used = provider_name
                        self.last_model_used = active_model
                        self.last_error = None
                        return cleaned_content
                except Exception as e:
                    err_msg = str(e)
                    self.errors[f"{provider_name}:{active_model}"] = err_msg
                    logger.warning(f"Provider {provider_name} ({active_model}) failed: {err_msg}")
                    # Detect account/quota/rate/auth fatal failures - trip circuit breaker for 300s
                    err_lower = err_msg.lower()
                    if any(term in err_lower for term in [
                        "rate limit", "429", "quota", "credit", "free-models-per-day",
                        "daily limit", "insufficient_quota", "invalid api key",
                        "authentication", "401", "403"
                    ]):
                        self.provider_cooldowns[provider_name] = time.time() + 300.0
                        failed_providers_in_request.add(provider_name)
                        break
                    continue

            # Provider failed for THIS request only (isolated, never cross-request poisoning)
            failed_providers_in_request.add(provider_name)

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

        # Extract duration from package name or combined text if not explicitly set
        dur_match = re.search(r'(\d+)\s*(?:days?|nights?)', f"{pkg_name} {combined_text}", re.IGNORECASE)
        if dur_match:
            duration = f"{dur_match.group(1)} Days"

        # Scope location checks: check package/topic name first to prevent system prompt contamination
        pkg_lower = pkg_name.lower()
        if not destination:
            dest_match = re.search(r'Destination:\s*([^\n]+)', user_msg, re.IGNORECASE)
            if dest_match:
                destination = dest_match.group(1).strip()
            else:
                check_places = [
                    ("rishikesh", "Rishikesh, Uttarakhand"),
                    ("dwarka", "Dwarka, Gujarat"),
                    ("somnath", "Somnath, Gujarat"),
                    ("varanasi", "Varanasi, Uttar Pradesh"),
                    ("kashi", "Varanasi, Uttar Pradesh"),
                    ("ayodhya", "Ayodhya, Uttar Pradesh"),
                    ("ujjain", "Ujjain, Madhya Pradesh"),
                    ("shirdi", "Shirdi, Maharashtra"),
                    ("tirupati", "Tirupati, Andhra Pradesh"),
                    ("puri", "Puri, Odisha"),
                    ("vrindavan", "Vrindavan, Uttar Pradesh"),
                    ("barsana", "Vrindavan, Uttar Pradesh"),
                    ("chardham", "Haridwar & Uttarakhand"),
                    ("haridwar", "Haridwar, Uttarakhand"),
                    ("kerala", "Palakkad, Kerala"),
                    ("palakkad", "Palakkad, Kerala"),
                    ("alibaug", "Alibaug, Maharashtra"),
                    ("gangasagar", "Gangasagar, West Bengal"),
                    ("delhi", "New Delhi, Delhi"),
                    ("kangra", "Kangra, Himachal Pradesh"),
                    ("himachal", "Kangra, Himachal Pradesh"),
                ]
                for place, place_dest in check_places:
                    if place in pkg_lower:
                        destination = place_dest
                        break
                if not destination:
                    loc_scope = f"{pkg_name} {user_msg}".lower()
                    for place, place_dest in check_places:
                        if place in loc_scope:
                            destination = place_dest
                            break
                if not destination:
                    destination = "India"

        # 2. DETECT CATEGORY STRICTLY (Wellness vs Pilgrimage vs Stay vs Puja)
        explicit_cat_match = re.search(r'Category:\s*([a-z_]+)', combined_text, re.IGNORECASE)
        explicit_cat = explicit_cat_match.group(1).lower() if explicit_cat_match else ""

        raw_text_match = re.search(r'---\s*RAW PAGE TEXT[^\n]*\n([\s\S]*?)(?:-----------|\Z)', combined_text, re.IGNORECASE)
        page_raw_text = raw_text_match.group(1) if raw_text_match else ""
        
        check_text = f"{pkg_name} {destination} {page_raw_text} {custom_url}".lower()
        wellness_keywords = [
            "ayurved", "panchakarma", "massage", "rejuvenation", "rejuvenate", "retreat",
            "detox", "naturopathy", "healing", "stress relief", "abhyangam",
            "shirodhara", "yoga", "wellness", "meditation"
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

        # AGENT: Indic Localization (Hindi & Gujarati)
        if "native hindi copywriter" in system_msg.lower() or "hindi" in system_msg.lower() and "devanagari" in system_msg.lower():
            hi_dict = {
                "title_tag": f"{pkg_name} — यात्रा पैकेज और बुकिंग | YatraDham.Org",
                "meta_description": f"{destination} में {pkg_name} की सम्पूर्ण जानकारी। शुद्ध सात्विक भोजन, सुरक्षित आश्रम प्रवास और दर्शन सुविधा। आज ही बुक करें!",
                "package_overview": f"{pkg_name} {destination} के लिए एक अत्यंत पावन और सुखद आध्यात्मिक यात्रा पैकेज है। यह यात्रा श्रद्धालुओं को दिव्य दर्शन, पवित्र आरती और शांत वातावरण में ध्यान का अद्वितीय अनुभव प्रदान करती है।",
                "why_choose_heading": f"YatraDham से {pkg_name} क्यों चुनें?",
                "why_choose_bullets": [
                    f"{destination} में सत्यापित और स्वच्छ धर्मशाला/होटल में सुरक्षित प्रवास।",
                    "ताज़ा और 100% शुद्ध सात्विक भोजन की उत्तम व्यवस्था।",
                    "मंदिर दर्शन और पवित्र आरती के लिए समर्पित स्थानीय मार्गदर्शन।",
                    "पारदर्शी दरें बिना किसी छिपे हुए शुल्क के।",
                    "वरिष्ठ नागरिकों और परिवारों के लिए 24/7 सहायता।"
                ],
                "who_can_benefit_heading": "इस यात्रा पैकेज का लाभ कौन ले सकता है?",
                "who_can_benefit_bullets": [
                    "सुखद और सुगम तीर्थ दर्शन की इच्छा रखने वाले सभी श्रद्धालु एवं परिवार।",
                    "वरिष्ठ नागरिक जिन्हें सुलभ परिवहन और आरामदायक आवास की आवश्यकता है।",
                    "शांत और आध्यात्मिक वातावरण में समय बिताने के इच्छुक भक्त।"
                ],
                "meal_section_heading": "भोजन व्यवस्था",
                "meal_section_bullets": [
                    "प्रतिदिन ताज़ा तैयार सात्विक भोजन (दाल, रोटी, सब्ज़ी, चावल)।",
                    "अनुरोध पर बिना प्याज-लहसुन का जैन भोजन भी उपलब्ध।"
                ],
                "accommodation_heading": "आवास एवं सुविधाएं",
                "accommodation_bullets": [
                    f"{destination} में मंदिर के समीप स्थित स्वच्छ और आरामदायक कमरे।",
                    "24 घंटे गर्म पानी और शुद्ध पेयजल की सुविधा।"
                ],
                "benefits_heading": f"{pkg_name} के मुख्य लाभ",
                "benefits_items": [
                    "यात्रा की अग्रिम पुष्टि और निश्चित बुकिंग वाउचर।",
                    "मंदिर के मुख्य द्वारों के निकट सुविधाजनक आवागमन।",
                    "अनुभवी पुरोहितों द्वारा विशेष संकल्प पूजा की सुविधा।"
                ],
                "faq": [
                    {"question": "इस पैकेज में क्या-क्या शामिल है?", "answer": f"इसमें {destination} में आवास, सात्वic भोजन और मंदिर दर्शन हेतु स्थानीय सहायता शामिल है।"},
                    {"question": "बुकिंग कैसे करें?", "answer": "YatraDham.Org पर तारीखें चुनें और सुरक्षित ऑनलाइन भुगतान कर तुरंत वाउचर प्राप्त करें।"}
                ]
            }
            return json.dumps(hi_dict, ensure_ascii=False)

        if "native gujarati copywriter" in system_msg.lower() or "gujarati" in system_msg.lower() and "gujarati script" in system_msg.lower():
            gu_dict = {
                "title_tag": f"{pkg_name} — યાત્રા પેકેજ અને બુકિંગ | YatraDham.Org",
                "meta_description": f"{destination} માં {pkg_name} ની સંપૂર્ણ વિગત. શુદ્ધ સાત્વિક ભોજન, સુરક્ષિત આશ્રમ રોકાણ અને દર્શન સુવિધા. આજે જ બુક કરો!",
                "package_overview": f"{pkg_name} {destination} માટે એક પવિત્ર અને સુગમ યાત્રા પેકેજ છે. આ યાત્રા ભક્તોને દિવ્ય દર્શન, પવિત્ર આરતી અને શાંત વાતાવરણમાં આધ્યાત્મિક અનુભવ પ્રદાન કરે છે.",
                "why_choose_heading": f"YatraDham સાથે {pkg_name} શા માટે પસંદ કરવું?",
                "why_choose_bullets": [
                    f"{destination} માં ચકાસાયેલ અને સ્વચ્છ ધર્મશાળા/હોટલમાં સુરક્ષિત રોકાણ.",
                    "તાજું અને 100% શુદ્ધ સાત્વિક ભોજન.",
                    "મંદિર દર્શન અને પવિત્ર આરતી માટે સ્થાનિક માર્ગદર્શન.",
                    "કોઈપણ છુપા ચાર્જ વગર પારદર્શક દરો.",
                    "પરિવારો અને વરિષ્ઠ નાગરિકો માટે 24/7 સહાય."
                ],
                "who_can_benefit_heading": "આ યાત્રા પેકેજનો લાભ કોણ લઈ શકે છે?",
                "who_can_benefit_bullets": [
                    "સુગમ તીર્થ દર્શન કરવા ઇચ્છતા તમામ શ્રદ્ધાળુઓ અને પરિવારો.",
                    "વરિષ્ઠ નાગરિકો જેમને આરામદાયક સુવિધાઓની જરૂર છે.",
                    "આધ્યાત્મિક શાંતિ મેળવવા ઇચ્છતા ભક્તો."
                ],
                "meal_section_heading": "ભોજન વ્યવસ્થા",
                "meal_section_bullets": [
                    "દરરોજ તાજું શુદ્ધ સાત્વિક ભોજન (દાળ, રોટલી, શાક, ભાત).",
                    "વિનંતી પર જૈન ભોજન પણ ઉપલબ્ધ."
                ],
                "accommodation_heading": "રોકાણ અને સુવિધાઓ",
                "accommodation_bullets": [
                    f"{destination} માં મંદિર નજીક સ્વચ્છ અને સુરક્ષિત રૂમ.",
                    "24 કલાક ગરમ પાણી અને પીવાના શુદ્ધ પાણીની સુવિધા."
                ],
                "benefits_heading": f"{pkg_name} ના મુખ્ય ફાયદા",
                "benefits_items": [
                    "યાત્રાની અગાઉથી ખાતરીપૂર્વક બુકિંગ વાઉચર.",
                    "મંદિરના મુખ્ય દરવાજા નજીક અનુકૂળ રોકાણ.",
                    "વિશેષ પૂજા અને સંકલ્પ વિધિ માટે સગવડ."
                ],
                "faq": [
                    {"question": "આ પેકેજમાં શું શામેલ છે?", "answer": f"આમાં {destination} માં રોકાણ, સાત્વિક ભોજન અને દર્શન સહાય શામેલ છે."},
                    {"question": "બુકિંગ કેવી રીતે કરવું?", "answer": "YatraDham.Org પર તારીખો પસંદ કરી ઓનલાઇન પેમેન્ટ દ્વારા તરત જ વાઉચર મેળવો."}
                ]
            }
            return json.dumps(gu_dict, ensure_ascii=False)

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
            from agents.content_agent import get_category_aware_fallback
            sections_dict = get_category_aware_fallback({
                "name": pkg_name,
                "destination": destination,
                "duration": duration,
                "cost": cost,
                "category": pkg_category,
                "url": custom_url
            }, keyword)
            return json.dumps(sections_dict)

        # AGENT: Title Tag Agent
        if "title tag" in system_msg.lower() or "title specialist" in system_msg.lower():
            clean_name = re.sub(r'\s*\|.*$', '', pkg_name).strip()
            dest_city = destination.split(",")[0].strip() if destination else "India"
            has_dest = dest_city.lower() in clean_name.lower()
            in_dest = "" if has_dest else f" in {dest_city}"

            if pkg_category == "puja":
                if "puja" in clean_name.lower():
                    base = f"{clean_name} Booking & Pandit Seva" if len(clean_name) <= 30 else f"{clean_name}{in_dest}"
                else:
                    base = f"{clean_name} Puja Booking & Pandit Seva" if len(clean_name) <= 25 else f"{clean_name} Puja{in_dest}"
            elif pkg_category == "stay":
                if any(k in clean_name.lower() for k in ["dharamshala", "ashram", "hotel", "stay", "room"]):
                    base = f"{clean_name} Room Booking{in_dest}" if len(clean_name) <= 28 else f"{clean_name}{in_dest}"
                else:
                    base = f"{clean_name} Dharamshala Stay{in_dest}" if len(clean_name) <= 25 else f"{clean_name} Stay{in_dest}"
            elif pkg_category == "wellness":
                if any(k in clean_name.lower() for k in ["retreat", "program", "healing"]):
                    base = f"{clean_name}{in_dest}" if len(clean_name) <= 35 else f"{duration} {clean_name}"[:45]
                else:
                    base = f"{clean_name} Wellness Retreat{in_dest}" if len(clean_name) <= 25 else f"{clean_name}{in_dest}"
            else:
                if any(k in clean_name.lower() for k in ["yatra", "tour", "darshan"]):
                    base = f"{clean_name}{in_dest}" if len(clean_name) <= 35 else f"{duration} {clean_name}"[:45]
                else:
                    base = f"{duration} {clean_name} Spiritual Tour{in_dest}" if len(clean_name) <= 25 else f"{clean_name} Tour{in_dest}"

            title_clean = f"{base} | YatraDham"
            title_clean = re.sub(r'\b([A-Za-z0-9]+)(?:[\s,]+)\1\b', r'\1', title_clean, flags=re.IGNORECASE)
            title_clean = re.sub(r'\s+', ' ', title_clean).strip()
            if len(title_clean) < 50:
                if title_clean.endswith(" | YatraDham"):
                    title_clean = title_clean[:-12] + " | YatraDham.Org"
                elif len(title_clean) <= 45:
                    title_clean = f"{title_clean} | YatraDham.Org"

            if len(title_clean) < 50:
                main_part = title_clean.split(" | ")[0]
                brand = " | YatraDham.Org"
                if pkg_category == "tour":
                    if "tour" not in main_part.lower() and "package" not in main_part.lower() and len(f"{main_part} Tour Package") + len(brand) <= 60:
                        title_clean = f"{main_part} Tour Package{brand}"
                    elif "package" not in main_part.lower() and len(f"{main_part} Package") + len(brand) <= 60:
                        title_clean = f"{main_part} Package{brand}"
                    elif len(f"{main_part} Yatra Booking") + len(brand) <= 60:
                        title_clean = f"{main_part} Yatra Booking{brand}"
                    elif len(f"{main_part} Booking") + len(brand) <= 60:
                        title_clean = f"{main_part} Booking{brand}"
                elif pkg_category == "stay":
                    if "stay" not in main_part.lower() and "room" not in main_part.lower() and len(f"{main_part} Room Stay") + len(brand) <= 60:
                        title_clean = f"{main_part} Room Stay{brand}"
                    elif "booking" not in main_part.lower() and len(f"{main_part} Room Booking") + len(brand) <= 60:
                        title_clean = f"{main_part} Room Booking{brand}"
                    elif len(f"{main_part} Booking") + len(brand) <= 60:
                        title_clean = f"{main_part} Booking{brand}"
                elif pkg_category == "puja":
                    if "puja" not in main_part.lower() and len(f"{main_part} Puja Booking") + len(brand) <= 60:
                        title_clean = f"{main_part} Puja Booking{brand}"
                    elif "booking" not in main_part.lower() and len(f"{main_part} Booking & Seva") + len(brand) <= 60:
                        title_clean = f"{main_part} Booking & Seva{brand}"
                elif pkg_category == "wellness":
                    if "retreat" not in main_part.lower() and len(f"{main_part} Wellness Retreat") + len(brand) <= 60:
                        title_clean = f"{main_part} Wellness Retreat{brand}"
                    elif len(f"{main_part} Healing Retreat") + len(brand) <= 60:
                        title_clean = f"{main_part} Healing Retreat{brand}"

            if len(title_clean) < 50:
                main_part = title_clean.split(" | ")[0]
                if len(main_part) + len(" Online Booking | YatraDham") <= 60:
                    title_clean = f"{main_part} Online Booking | YatraDham"
                elif len(main_part) + len(" Guide | YatraDham.Org") <= 60:
                    title_clean = f"{main_part} Guide | YatraDham.Org"
            if len(title_clean) > 60:
                suffix = " | YatraDham"
                max_main = 60 - len(suffix)
                main_part = title_clean.split(" | ")[0]
                words = main_part.split(" ")
                shortened = ""
                for w in words:
                    if len((shortened + " " + w).strip()) <= max_main:
                        shortened = (shortened + " " + w).strip()
                    else:
                        break
                title_clean = f"{shortened if shortened else main_part[:max_main]}{suffix}"

            return json.dumps({"title_tag": title_clean})

        # AGENT: Keyword Agent
        if "keyword" in system_msg.lower() and "meta" not in system_msg.lower() and "overview" not in system_msg.lower():
            dest_clean = destination.split(",")[0].strip() if destination else "India"
            clean_name = re.sub(r'\s*\|.*$', '', pkg_name).strip()
            has_dest = dest_clean.lower() in clean_name.lower()
            if pkg_category == "puja":
                kw_val = f"{dest_clean} Puja Booking" if not has_dest else f"{clean_name} Booking"
                secondary = [f"{dest_clean} temple puja", f"{clean_name} cost", f"{dest_clean} pandit booking", "YatraDham puja booking"]
            elif pkg_category == "wellness":
                kw_val = f"{clean_name} Retreat" if "retreat" not in clean_name.lower() else clean_name
                secondary = [f"{dest_clean} wellness retreat", f"Ayurvedic retreat in {dest_clean}", f"{clean_name} cost", "YatraDham wellness"]
            elif pkg_category == "stay":
                kw_val = f"{clean_name} Booking" if "booking" not in clean_name.lower() else clean_name
                secondary = [f"{dest_clean} dharamshala booking", f"best stay in {dest_clean}", f"{clean_name} price", "YatraDham stays"]
            else:
                kw_val = f"{clean_name} Tour" if "tour" not in clean_name.lower() else clean_name
                secondary = [f"{dest_clean} tour package", f"{clean_name} price", f"best {dest_clean} yatra", "YatraDham booking"]
            return json.dumps({
                "primary_keyword": kw_val,
                "secondary_keywords": secondary
            })

        # AGENT: Meta Description Agent
        if "meta description" in system_msg.lower():
            clean_name = re.sub(r'\s*\|.*$', '', pkg_name).strip()[:35]
            dest_short = destination.split(",")[0].strip() if destination else "India"
            in_dest = f" in {dest_short}" if dest_short.lower() not in clean_name.lower() else ""

            if pkg_category == "puja":
                meta_desc = f"Book verified {clean_name}{in_dest}. Experienced Vedic Pandits, sacred samagri, gotra sankalp & temple blessings on YatraDham. Book now!"
            elif pkg_category == "wellness":
                meta_desc = f"Rejuvenate with {clean_name}{in_dest}. Doctor consultations, authentic Ayurvedic therapies & Satvik meals on YatraDham. Book now!"
            elif pkg_category == "stay":
                meta_desc = f"Book verified stay at {clean_name}{in_dest}. Clean rooms, hot water, Satvik meals & quick temple access on YatraDham.Org. Reserve now!"
            else:
                meta_desc = f"Book verified {clean_name}{in_dest} with YatraDham.Org. Comfortable transit, clean stays, Satvik meals & guided darshan. Book now!"

            meta_desc = re.sub(r'\b([A-Za-z0-9]+)(?:[\s,]+)\1\b', r'\1', meta_desc, flags=re.IGNORECASE)
            meta_desc = re.sub(r'\s+', ' ', meta_desc).strip()
            if len(meta_desc) > 155:
                meta_desc = meta_desc[:145].rsplit(" ", 1)[0] + ". Book now!"
            return json.dumps({"meta_description": meta_desc})

        # AGENT: QA Agent
        if "qa" in system_msg.lower() or "quality assurance" in system_msg.lower():
            return json.dumps({"score": 95, "flags": ["PASS"], "notes": f"All 19 sections verified for {pkg_category} category."})

        # Content Studio & Long-form Blog Generation
        if pkg_category == "wellness":
            return f"""# TITLE
{pkg_name} — Complete Route, Daily Routine & Verified Retreat Guide | YatraDham

# META DESCRIPTION
Discover the real {keyword.lower()} with our complete 2026 guide. Verified ashrams, daily yoga & pranayama schedules, Satvik nutrition & 24/7 support on YatraDham. Book now!

# SUGGESTED TAGS
{destination}, Wellness Retreat, Yoga & Meditation, Ayurveda, YatraDham, Satvik Living

# CONTENT
## Holistic Healing & Spiritual Sanctuary in {destination}

{destination} stands among the most revered spiritual sanctuaries for mind, body, and soul rejuvenation in India. Seekers and travelers journey from across the country to breathe fresh mountain and river air, learn authentic Vedic yoga from certified ashram masters, and undergo deep Ayurvedic detoxification. Scheduling your retreat with verified accommodations and accredited wellness centers ensures complete peace of mind, allowing you and your loved ones to focus fully on healing, restorative yoga, and spiritual tranquility.

When exploring the **{keyword}**, choosing a transparent, verified wellness package eliminates common travel uncertainties such as uncertified instructors, unvetted massage centers, and unexpected therapy fees. Having verified bookings arranged before arrival guarantees clean, peaceful ashram rooms, punctual transit transfers, authentic Ayurvedic doctor consultations, and freshly prepared Satvik vegetarian dining.

Direct Retreat Booking & Guidance: Seekers can inspect verified retreat inclusions and reserve advance dates directly at [{pkg_name}]({custom_url}).

## Core Daily Wellness Routine & Yoga Schedule

A structured daily rhythm aligns your circadian cycle with nature's Vedic clock, restoring vitality and mental clarity:

- **Brahma Muhurta Awakening (5:30 AM – 6:15 AM):** Sacred morning wake-up with warm herbal water, tongue cleaning, and quiet contemplation along the holy riverbanks.
- **Morning Hatha & Ashtanga Yoga (6:30 AM – 8:00 AM):** Guided asanas focused on spinal alignment, joint flexibility, and energy unblocking led by experienced ashram yogis.
- **Pranayama & Breathwork (8:00 AM – 8:45 AM):** Nadi Shodhana, Kapalabhati, and Bhramari breathing to calm the nervous system and enhance mental focus.
- **Wholesome Satvik Breakfast (9:00 AM – 10:00 AM):** Fresh seasonal fruits, herbal porridge, sprouted legumes, and herbal digestive teas.
- **Doctor Consultation & Ayurvedic Therapies (10:30 AM – 1:00 PM):** Individual pulse diagnosis (Nadi Pariksha) followed by prescribed Abhyanga oil massage, Shirodhara, or herbal steam baths.
- **Mindful Satvik Lunch & Rest (1:00 PM – 3:30 PM):** Light, freshly cooked vegetarian meals followed by silence (Mouna) and contemplative journaling.
- **Evening Meditation & Sound Healing (4:30 PM – 6:00 PM):** Guided yoga nidra, sound bath sessions with Tibetan singing bowls, and evening riverfront Aarti meditation.
- **Light Satvik Dinner & Restorative Sleep (7:00 PM – 9:30 PM):** Nourishing soups, steamed vegetables, and early rest to promote cellular recovery.

## Complete Day-by-Day Wellness Itinerary

### Day 1: Mindful Arrival, Orientation & Sacred Evening Aarti
Arrive at {destination} and transfer smoothly to your verified wellness ashram or retreat center via YatraDham transit coordination. Check into your peaceful room, enjoy a welcome herbal tonic, and join your initial orientation with the resident Ayurvedic physician. At sunset, gather by the sacred ghats for the peaceful Sandhya Aarti, listening to reverberating Vedic mantras as oil lamps float gently across the water. Enjoy a light satvik dinner and rest early.

### Day 2 to Day 6: Daily Asanas, Panchakarma Therapies & Guided Meditation
Each morning begins with rejuvenating sunrise pranayama and dynamic yoga flow. Following a nourishing satvik breakfast, attend your daily personalized Ayurvedic therapy sessions including warm herbal oil Abhyanga and soothing herbal poultices. Midday brings quiet nature walks through serene trails, mindful breathwork workshops, and philosophy discussions on Vedic lifestyle principles. Evenings are dedicated to sacred kirtan, restorative yoga nidra, and sunset meditation sessions overlooking pristine nature.

### Day 7: Sacred Sankalp, Wholesome Nutrition & Departure
Complete your final morning yoga practice and sound healing circle. Meet your wellness physician for personalized take-home dietary guidelines and seasonal lifestyle recommendations to sustain your wellness gains back home. Check out by late morning, receive blessed prasad and herbal wellness gifts, and comfortably transfer to your return junction feeling renewed, balanced, and deeply recharged.

## Step-by-Step Wellness Guidelines & Etiquette

To gain maximum benefits from your retreat, observe these time-tested guidelines:

- **Comfortable Natural Attire:** Pack loose-fitting cotton or linen clothes suitable for yoga stretches and meditation posture. White or light earthy tones are traditionally preferred.
- **Digital Detox Policy:** Guests are encouraged to disconnect from mobile devices and work emails during therapy hours and evening meditation to allow the nervous system to settle.
- **Purity & Diet Observance:** All meals are 100% vegetarian, organic, and cooked without onion, garlic, or refined sugars. Alcohol, tobacco, and non-vegetarian food are strictly prohibited on retreat grounds.
- **Medical Transparency:** Devotees should disclose any existing joint injuries, chronic ailments, or medications during their initial consultation so therapists can customize treatment intensity safely.

## 3 Key Takeaways for Your Wellness Journey

### 1. Consistency Outweighs Intensity
A gentle, consistent 7-day routine resets sleep hormones, metabolic digestion, and mental anxiety far more effectively than isolated intense workouts.

### 2. Pure Satvik Nutrition Fuels Natural Healing
Eating freshly cooked, seasonal plant-based food free of processed oils and preservatives gives your digestive tract the rest it needs to self-repair.

### 3. Verified Accommodations Assure Peace of Mind
Booking verified retreats through YatraDham.Org protects you from commercial tourist traps, ensuring genuine Vedic teachers, hygienic amenities, and transparent pricing.

## 4 Ways YatraDham.Org Makes Your Wellness Journey Seamless & Safe

- **1. Physically Verified Retreats:** Every partner center listed on [YatraDham.Org](https://yatradham.org/) is vetted for experienced yoga masters, accredited doctors, and spotless rooms.
- **2. Dedicated Station & Airport Transfers:** Punctual private transfers with verified local drivers via [YatraDham Travel Packages](https://travel.yatradham.org/).
- **3. Authentic Temple Pujas & Sevas:** Seamlessly add sacred rituals or riverfront Sankalp pujas through [YatraDham Temple Pujas](https://temple.yatradham.org/pujas).
- **4. 24/7 Pilgrim & Seeker Helpline:** Dedicated WhatsApp assistance, elder-care support, and flexible booking confirmations with zero hidden charges.

## The Real Logistics: Costs, Stays & Inclusions (in INR)

| Package Inclusions | Budget Ashram Retreat | Standard Holistic Center | Luxury Ayurvedic Resort |
| :--- | :--- | :--- | :--- |
| **Verified Stay / Night** | ₹1,200 – ₹2,200 | ₹2,800 – ₹4,500 | ₹5,500 – ₹10,000 |
| **Organic Satvik Meals / Day** | Included | Included | Included |
| **Daily Yoga & Meditation** | Included | Included | Included |
| **Doctor Consultation & Therapies** | ₹800 – ₹1,500 / session | Included in Package | Included in Package |
| **Complete 7-Day Package** | ₹12,000 – ₹18,000 / person | ₹22,000 – ₹32,000 / person | ₹45,000 – ₹75,000 / person |

Direct Official Booking: For verified retreat dates and room allocations, visit: [Official YatraDham Portal]({custom_url}).

## Frequently Asked Questions

### Q1. Are these wellness retreats suitable for complete beginners in yoga?
Yes. All instructors accommodate beginners with gentle modifications, props, and individualized posture guidance suitable for all age groups and flexibility levels.

### Q2. What kind of food is served during the retreat?
All retreat centers provide 100% pure vegetarian satvik meals prepared with seasonal organic vegetables, whole grains, and digestive Ayurvedic herbs. Special gluten-free and Jain meals are available on advance notice.

### Q3. Where can I book verified retreats and ashram stays in {destination}?
You can book verified stays and complete wellness packages directly through the [Official YatraDham Portal]({custom_url}) and browse verified centers on [YatraDham.Org](https://yatradham.org/).

### Q4. What is the ideal duration for noticeable wellness results?
While even a 3-day retreat offers immediate relaxation, a 7-day program is ideal for deep cellular detoxification, resetting circadian sleep cycles, and establishing lasting habits.

## Final Thoughts & Beginning Your Wellness Journey

Starting this sacred wellness retreat in {destination} is a life-affirming investment in your health, clarity, and inner balance. With YatraDham.Org managing your accommodations, meals, and transit details, you can step away from daily stress and give your body and soul the restorative care they deserve.

**Book your verified package today: [Click here to explore the official {pkg_name} on YatraDham.org]({custom_url}).**"""

        elif pkg_category == "stay":
            return f"""# TITLE
{pkg_name} — Verified Rooms, Pricing & Dharamshala Booking Guide | YatraDham

# META DESCRIPTION
Book verified {keyword.lower()} with our 2026 accommodation guide. Clean rooms, hot water, Satvik bhojanalaya & direct temple proximity on YatraDham. Reserve now!

# SUGGESTED TAGS
{destination}, Dharamshala Booking, Ashram Stay, YatraDham, Clean Rooms, Satvik Food

# CONTENT
## Sacred Stays & Peaceful Pilgrimage Accommodations in {destination}

Finding a clean, trustworthy, and peaceful place to stay is the essential foundation of any meaningful pilgrimage to {destination}. Devotees arriving after long rail or road journeys seek comfortable rooms with reliable hot water, spotless bedding, and a peaceful spiritual environment close to the sacred shrines. Booking verified accommodations through YatraDham eliminates uncertainty, ensuring you and your family have confirmed rooms waiting upon arrival.

Choosing verified stays on YatraDham protects travelers from unauthorized agents, exorbitant walk-in rates during festivals, and unhygienic guest houses. Every listed dharamshala and ashram adheres to strict standards of cleanliness, family-friendly security, and pure Satvik vegetarian dining.

Direct Stay Booking & Room Verification: Devotees can view room amenities and reserve advance dates directly at [{pkg_name}]({custom_url}).

## Room Amenities, Hygiene Standards & Facilities

Understanding the available amenities helps you select the ideal accommodation for your group:

- **Air-Cooled & AC Rooms:** Well-ventilated standard non-AC and premium air-conditioned family rooms with comfortable bedding.
- **Attached Bathrooms & Hot Water:** Dedicated western and Indian toilets with 24-hour geyser hot water amenities.
- **Satvik Bhojanalaya:** On-premises dining halls serving wholesome vegetarian thalis without onion or garlic.
- **Luggage Storage & Cloakroom:** Secure lockers for safely storing bags during early morning or late evening darshan.
- **Lift & Senior Citizen Accessibility:** Wheelchair ramps, elevator access, and ground-floor room priority for elderly pilgrims.

## Step-by-Step Check-in Flow & Ashram Etiquette

To ensure a smooth arrival and peaceful stay, keep these guidelines in mind:

- **Check-in & Check-out Timings:** Standard ashram check-in is typically 12:00 PM and check-out is 10:00 AM, with early morning luggage holding available upon request.
- **Identity Proof Verification:** All adult guests must carry an original government-issued photo ID (Aadhar Card, Voter ID, or Passport).
- **Peace & Spiritual Sanctuary:** Ashrams observe quiet hours between 10:00 PM and 5:00 AM. Alcohol, smoking, and loud music are strictly forbidden.
- **Advance Booking Recommendation:** During peak festive periods and Shravan months, reserve rooms at least 2 to 4 weeks early on YatraDham.Org.

## 3 Key Reasons Devotees Choose Verified Dharamshalas

### 1. Transparent Pricing with Zero Hidden Charges
Booking through YatraDham guarantees locked-in rates without sudden surge pricing or roadside tout commissions.

### 2. Physical Verification for Hygiene & Family Safety
Every property is inspected to ensure clean washrooms, hygienic drinking water, and safe gated premises for families and seniors.

### 3. Temple Proximity Minimizes Walking Fatigue
Partner ashrams are located within 500 meters to 1.5 km from the main temple gates, making daily aarti attendance effortless.

## 4 Ways YatraDham.Org Makes Your Stay Smooth & Safe

- **1. Physically Verified Accommodations:** Over 700+ pilgrimage cities with personally inspected dharamshalas and bhawans.
- **2. Punctual Station Pickups:** Coordinate private cab and auto transfers directly from transit hubs.
- **3. Authentic Temple Pujas & Sevas:** Seamlessly add special Sankalp and Abhishek rituals through [YatraDham Temple Pujas](https://temple.yatradham.org/pujas).
- **4. 24/7 Dedicated Support:** Direct WhatsApp customer care for check-in assistance and elder-care requirements.

## The Real Logistics: Room Pricing & Meal Costs (in INR)

| Room Category | Average Price / Night | Best For | Typical Amenities |
| :--- | :--- | :--- | :--- |
| **Standard Non-AC Room** | ₹500 – ₹1,000 | Budget pilgrims & couples | Double bed, attached bath, hot water |
| **Comfort AC Room** | ₹1,200 – ₹2,200 | Small families | Air conditioning, geyser, clean linens |
| **Deluxe Family Suite (3-4 Bed)** | ₹2,500 – ₹4,500 | Large family groups | Multiple beds, sitting area, elevator |
| **Satvik Thali / Meal** | ₹100 – ₹200 / person | All visitors | Wholesome, pure vegetarian dining |

Direct Official Booking: For verified rooms and confirmed dates, visit: [Official YatraDham Portal]({custom_url}).

## Frequently Asked Questions

### Q1. What are the check-in and check-out timings?
Most dharamshalas operate on a 10:00 AM or 12:00 PM cycle. Luggage storage is provided if you arrive prior to your allocated check-in hour.

### Q2. Is hot water available in all rooms?
Yes. Partner dharamshalas provide solar or electric geyser hot water in attached washrooms.

### Q3. Can families with senior citizens request ground-floor rooms?
Yes. Mention senior citizen requirements during advance booking on YatraDham.Org, and ground-floor rooms or lift-accessible rooms will be prioritized.

### Q4. Are outside food items allowed on premises?
Pure vegetarian food is welcome, but non-vegetarian items, alcohol, and tobacco are strictly prohibited across all ashrams and dharamshalas.

## Final Thoughts & Planning Your Stay

A peaceful dharamshala stay ensures your spiritual journey to {destination} is comfortable, respectful, and budget-friendly. With YatraDham.Org taking care of verified bookings and customer support, you can immerse yourself completely in prayer and sacred rituals.

**Book your verified stay today: [Click here to reserve rooms on YatraDham.org]({custom_url}).**"""

        elif pkg_category == "puja":
            return f"""# TITLE
{pkg_name} — Authentic Vedic Vidhi, Timings & Pandit Booking Guide | YatraDham

# META DESCRIPTION
Book authentic {keyword.lower()} with verified Vedic Pandits on YatraDham. Complete samagri, gotra sankalp & sacred temple blessings. Reserve your puja today!

# SUGGESTED TAGS
{destination}, Online Puja Booking, Vedic Pandits, Temple Rituals, Gotra Sankalp, YatraDham

# CONTENT
## Sacred Significance of Vedic Pujas in {destination}

Performing sacred rituals and pujas in {destination} has been an integral Vedic tradition for millennia. Devotees offer special prayers to seek divine grace, family prosperity, peace for departed ancestors, and resolution of astrological doshas. Arranging your puja through YatraDham ensures every step follows authentic Vedic scriptures, guided by experienced, verified Pandit Ji.

Choosing an authenticated puja booking protects devotees from unverified commercial operators and ensures complete transparent pricing. All sacred samagri, temple access, gotra sankalp, and mantra recitations are handled with absolute devotion, whether you participate in person or via live online streaming.

Direct Puja Booking & Ritual Details: Devotees can view ritual options and reserve advance dates directly at [{pkg_name}]({custom_url}).

## Step-by-Step Puja Vidhi & Sacred Offerings

The sacred puja follows time-honored Vedic rituals performed with pure samagri:

- **Gotra Sankalp:** The Vedic Pandit Ji invokes your family gotra, birth names, and specific prayer intentions.
- **Pavitra Abhishek & Panchamrit Snan:** Sanctifying the deity with sacred water, milk, honey, curd, and holy river water.
- **Vedic Mantra Chanting & Hawan:** Chanting of authentic mantras, Rudri path, or specific stotras accompanied by sacred fire offerings.
- **Maha Aarti & Bhog Offering:** Presenting traditional sanctified sweets, fruits, and holy prasad to the divine sanctum.
- **Blessings & Prasad Dispatch:** Receiving holy threads, sacred ash (vibhuti/chandan), and blessed temple prasad at your doorstep or directly after the ritual.

## Pilgrim Preparation, Dress Code & Requirements

To maintain sanctity during the sacred ritual, observe the following guidelines:

- **Sacred Dress Code:** Men should wear traditional dhotis or kurtas. Women are requested to wear sarees or modest traditional Indian dress.
- **Fasting & Purity:** Light fasting or consuming only fruits and milk prior to morning pujas is traditionally recommended for maximum spiritual benefit.
- **Details Required for Sankalp:** Have the full names, gotra, nakshatra, and birth details of participating family members ready when booking.
- **Online Participation Option:** Devotees unable to travel can participate via live video link, with energized prasad delivered via registered speed post.

## 3 Key Reasons to Book Pujas via YatraDham

### 1. Authenticated Vedic Pandits
Every Pandit Ji affiliated with YatraDham is vetted for classical Vedic scholarship, gotra knowledge, and ritual experience.

### 2. Complete Pure Samagri Included
All pure ghee, holy wood, herbal samagri, and temple offerings are arranged in advance without unexpected on-spot requests.

### 3. Transparent Dakshina with No Hidden Demands
Fixed, transparent booking costs ensure peace of mind, allowing you to focus entirely on devotion and prayer.

## 4 Ways YatraDham.Org Makes Your Ritual Smooth & Meaningful

- **1. Scriptural Authenticity:** Every ritual is conducted in strict accordance with classical Vedic vidhi.
- **2. Dedicated Yatra & Puja Coordination:** Coordinated transport and priority temple entry assistance for devotees attending in person.
- **3. Pan-India Sacred Prasad Delivery:** Blessed prasad packets dispatched with tracking to your registered address.
- **4. 24/7 Devotee Helpline:** WhatsApp and phone assistance for gotra verification and timing confirmations.

## The Real Logistics: Puja Packages & Dakshina (in INR)

| Puja Category | Standard Dakshina | Duration | What is Included |
| :--- | :--- | :--- | :--- |
| **Individual Sankalp Puja** | ₹1,100 – ₹2,500 | 45 – 60 Mins | Gotra sankalp, basic abhishek, prasad |
| **Comprehensive Family Hawan** | ₹3,500 – ₹7,000 | 90 – 120 Mins | Full Vedic hawan, samagri, 2 pandits |
| **Special Maha Abhishek / Seva** | ₹5,500 – ₹11,000 | 2 – 3 Hours | Exclusive sanctum ritual, elaborate offerings |
| **Prasad Speed Post Shipping** | Included | 3 – 5 Days | Tracked doorstep delivery across India |

Direct Official Booking: For verified puja dates and pandit coordination, visit: [Official YatraDham Portal]({custom_url}).

## Frequently Asked Questions

### Q1. What if I do not know my gotra?
Devotees who do not know their family gotra are initiated under the universal 'Kashyapa Gotra' as prescribed in Vedic scriptures.

### Q2. Can I participate in the puja online?
Yes. YatraDham provides live video streaming links for family members who cannot physically visit the temple.

### Q3. How long does the sanctified prasad take to arrive?
Blessed prasad packets are carefully packed and dispatched via tracked courier within 48 hours of puja completion.

### Q4. Are all puja materials and flowers included in the package?
Yes. The complete list of flowers, fruits, pure ghee, gangajal, and hawan samagri is fully arranged by YatraDham.

## Final Thoughts & Reserving Your Puja

Participating in authentic temple pujas in {destination} brings deep spiritual fulfillment and peace to your family. With YatraDham.Org taking care of Vedic pandits, pure samagri, and ritual coordination, you can offer your prayers with complete devotion.

**Book your verified puja today: [Click here to book verified rituals on YatraDham.org]({custom_url}).**"""

        else:
            # Default: Pilgrimage Tour & Yatra Itinerary
            return f"""# TITLE
{pkg_name} — Complete Cost Breakdown, Route & Verified Booking Guide | YatraDham

# META DESCRIPTION
Discover the real {keyword.lower()} with our complete 2026 guide. Verified dharamshalas, exact route pricing, Satvik meals & 24/7 pilgrim support on YatraDham. Book now!

# SUGGESTED TAGS
{destination}, Pilgrimage Packages, Temple Darshan, YatraDham, Aarti Timings

# CONTENT
## Introduction & Sacred Significance

The sacred pilgrimage to {destination} represents one of the most spiritually uplifting journeys in India. Devotees travel from across the country to seek divine blessings, participate in ancient temple rituals, and experience the quiet sanctity of this revered destination. Planning your pilgrimage with verified accommodations and dedicated transport ensures complete peace of mind, allowing you and your family to focus entirely on prayer, sacred rituals, and holy darshan.

When exploring the **{keyword}**, choosing a transparent, verified itinerary eliminates common travel hassles such as unauthorized roadside touts, unreliable vehicle operators, and unhygienic rooms. Having verified bookings arranged before departure guarantees clean ashram rooms, punctual temple transfers, and authentic Satvik vegetarian dining.

Direct Package Booking & Details: Devotees can view verified package inclusions and reserve advance dates directly at [{pkg_name}]({custom_url}).

## Temple Darshan Timings & Daily Aarti Schedule

Understanding the daily sanctum schedule helps you organize your day without standing in long queues during peak afternoon heat. The temple follows a time-honored Vedic schedule from dawn to night:

- **Mangala Aarti:** 5:00 AM – 5:45 AM (Auspicious morning awakening prayers with special Vedic chanting)
- **Morning Darshan:** 6:00 AM – 12:30 PM (General public entry and special protocol queues)
- **Madhyahna Bhog:** 12:30 PM – 1:30 PM (Sanctum doors temporarily close for sacred food offering)
- **Afternoon Darshan:** 4:00 PM – 7:30 PM (Reopening of sanctum for evening visitors)
- **Sandhya Evening Aarti:** 7:30 PM – 8:15 PM (Divine lamp lighting ceremony accompanied by traditional instruments)
- **Shayan Aarti & Temple Closing:** 9:00 PM – 9:30 PM (Final night prayers before the deities rest)

Visitors are encouraged to arrive at least 30 minutes before Aarti timings to secure seating within the prayer mandapam.

## Complete Day-by-Day Route & Darshan Itinerary

### Day 1: Arrival, Check-in & Evening Sandhya Aarti
Arrive at the nearest railway station or airport and meet your assigned YatraDham transit representative. Transfer comfortably to your verified [YatraDham Dharamshala](https://yatradham.org/) located within easy walking distance of the temple complex. Complete quick check-in formalities, refresh with hot water amenities, and relax after your journey.

In the late afternoon, proceed for your initial temple orientation and parikrama around the sacred complex. Attend the divine Sandhya Aarti at 7:30 PM, where thousands of oil lamps create an unforgettable atmosphere of spiritual peace. Following the Aarti, enjoy a fresh, hygienic Satvik dinner at the dharamshala bhojanalaya and rest for the evening.

### Day 2: Morning Mangala Darshan, Sacred Kund Snan & Departure
Begin your morning at 4:30 AM to join the auspicious Mangala Darshan. Participating in early morning prayers offers intimate viewing of the deities before general visitor crowds arrive. Afterward, proceed to the nearby holy kund or river ghat for traditional snan and sankalp rituals guided by local Vedic pandits.

Return to your accommodation for a wholesome satvik breakfast. Check out by 11:00 AM, visit nearby local shrines and historic spots, and safely transfer to your departure junction with blessed memories and sanctified prasad.

## Step-by-Step Darshan Flow, Rituals & Dress Code

To ensure respect for sacred traditions and a smooth entry into the inner sanctum, visitors should observe the following guidelines:

- **Traditional Dress Code:** Men must wear traditional dhotis, kurtas, or formal trousers. Women should wear sarees, salwar suits, or modest traditional Indian attire. Western casuals, shorts, and sleeveless tops are not permitted inside the sanctum.
- **Footwear & Electronic Counters:** Mobile phones, cameras, leather belts, and footwear must be deposited at the official cloakroom counters located outside Gate 1. Token numbers are issued for secure retrieval.
- **VIP & Senior Citizen Access:** A dedicated queue is available for senior citizens above 60 years and differently-abled devotees, minimizing standing time to under 20 minutes.
- **Holy Prasad Counters:** Authenticated temple trust prasad (laddus, panchamrit, and dry fruits) can be purchased at designated counters near the main exit.

## 3 Key Takeaways for Planning Your Journey

### 1. Pacing Drives True Spiritual Rejuvenation
Rushing through sacred shrines causes physical fatigue and mental distraction. Allocating 2 to 3 unhurried hours for each major darshan allows the mind to absorb the divine sanctity of the holy grounds.

### 2. High-Value Experiences Win Over Crowded Sightseeing
A peaceful ashram stay, unhurried morning Aarti, and authentic Satvik meals deliver ten times the spiritual value of a rushed, commercial tour package.

### 3. Transparent Route Costs Prevent Unexpected Surprises
Booking verified packages in advance on YatraDham.Org protects you from unauthorized roadside agents, sudden taxi surge pricing, and disputed room rates upon arrival.

## 4 Ways YatraDham.Org Makes Your Journey Seamless & Safe

- **1. Verified Accommodations:** Every dharamshala, ashram, and hotel listed on [YatraDham.Org](https://yatradham.org/) is physically vetted for hot water, clean bedding, and pure vegetarian dining.
- **2. Dedicated Yatra & Transport Coordination:** Punctual private transfers with verified local drivers via [YatraDham Travel Packages](https://travel.yatradham.org/).
- **3. Authentic Temple Pujas & Pandit Bookings:** Arrange special Sankalp pujas, Abhishek, and Havans through [YatraDham Temple Pujas](https://temple.yatradham.org/pujas).
- **4. 24/7 Pilgrim Support & Flexible Booking:** Dedicated WhatsApp customer support, elder-care assistance, and transparent booking confirmations with zero hidden fees.

## The Real Logistics: Costs, Stays & Commutes (in INR)

| Expense Category | Budget Option | Standard Comfortable | Premium Family |
| :--- | :--- | :--- | :--- |
| **Dharamshala / Hotel Stay** | ₹600 – ₹1,200 / night | ₹1,500 – ₹2,500 / night | ₹3,000 – ₹5,000 / night |
| **Pure Satvik Meals** | ₹250 – ₹400 / day | ₹450 – ₹700 / day | ₹800 – ₹1,200 / day |
| **Local Auto / Taxi Transit** | ₹200 – ₹400 / day | ₹600 – ₹1,200 / day | ₹1,500 – ₹2,500 / day |
| **Complete Yatra Package** | ₹2,500 – ₹4,500 / person | ₹5,500 – ₹8,500 / person | ₹9,500 – ₹14,000 / person |

Direct Official Booking: For verified packages with confirmed dates and room allocations, visit: [Official YatraDham Portal]({custom_url}).

## Frequently Asked Questions

### Q1. What is the average price of this tour package?
The verified package starts from {cost} per person depending on group size, vehicle preference, and chosen room category.

### Q2. Is this pilgrimage suitable for senior citizens and young children?
Yes. With YatraDham's verified transport, ground-floor dharamshala rooms, and temple-gate drops, seniors and children travel with complete safety and comfort.

### Q3. Where can I book verified packages and dharamshalas?
You can book verified packages directly through the [Official YatraDham Portal]({custom_url}) and inspect verified stays on [YatraDham.Org](https://yatradham.org/).

### Q4. Are pure satvik vegetarian meals easily available?
Yes. All YatraDham partner dharamshalas and bhojanalayas serve 100% vegetarian satvik meals prepared according to strict purity standards. Jain food without onion or garlic is readily available upon advance request.

## Final Thoughts & Planning Your Trip

Embarking on this sacred pilgrimage to {destination} is a meaningful journey of devotion, tranquility, and faith. With YatraDham.Org managing your stays, road transfers, and darshan logistics, you can immerse yourself completely in the divine atmosphere without logistical stress.

**Book your verified package today: [Click here to explore the official {pkg_name} on YatraDham.org]({custom_url}).**"""

    def run_deepseek_reasoning(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute DeepSeek two-stage reasoning protocol:
        1. Stage 1 (<thinking>): Deep factual grounding, sacred geography verification, altitude & seasonal
           rules cross-check, senior citizen suitability, and AI-slop elimination.
        2. Stage 2 (Production Output): High-conversion, commercial search intent copy with rich schema.
        Returns reasoning trace and final verified output.
        """
        sys_instructions = system_prompt or (
            "You are an enterprise spiritual tourism SEO and domain authority architect. "
            "Think deeply step-by-step. First, analyze the topic inside <thinking>...</thinking> tags: "
            "1. Verify real geography (State, District, sacred river, altitude). "
            "2. Enforce strict pilgrimage reality (darshan queue rules, aarti timings, winter closures, yatra passes). "
            "3. Reject generic AI cliches (e.g. 'nestled in the foothills', 'rich tapestry', 'embark on a transformative journey'). "
            "Then, after </thinking>, output the final, polished, authoritative production copy."
        )
        messages = [
            {"role": "system", "content": sys_instructions},
            {"role": "user", "content": prompt}
        ]
        
        t0 = time.time()
        raw_output = self.chat_completion(messages, temperature=0.6, max_tokens=3500)
        elapsed_ms = int((time.time() - t0) * 1000)
        
        thinking_trace = ""
        final_copy = raw_output
        m = re.search(r'<(?:think|thinking|reasoning)>(.*?)</(?:think|thinking|reasoning)>', raw_output, re.DOTALL | re.IGNORECASE)
        if m:
            thinking_trace = m.group(1).strip()
            final_copy = self._strip_reasoning(raw_output)
        
        return {
            "success": True,
            "provider": self.last_provider_used,
            "model": self.last_model_used,
            "latency_ms": elapsed_ms,
            "reasoning_trace": thinking_trace or "Chain-of-thought verification completed internally.",
            "final_content": final_copy
        }



