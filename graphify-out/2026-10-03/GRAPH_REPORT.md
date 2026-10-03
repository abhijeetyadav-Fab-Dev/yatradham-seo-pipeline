# Graph Report - yatradham-seo-pipeline  (2026-10-03)

## Corpus Check
- 51 files · ~116,996 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 857 nodes · 1733 edges · 65 communities (50 shown, 15 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e4163089`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- security_firewall.py
- test_e2e_suite.py
- enrich_destination_data
- de_slop_and_humanize
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- anti_ai_guardrails.py
- audit_google_genai_compliance
- validation_layer.py
- scraper.py
- nlp_and_safety_toolkit.py
- TestHumanizer55Patterns
- run
- get
- semrush_suite.py
- ProviderSettingsRequest
- process_package
- SitemapCrawler
- BaseModel
- LLMClient
- api_route
- content_creator_agent.py
- TestArchitecturalDecoupling
- check_serp_rank
- models.py
- generate_content
- pipeline.py
- batch_urls
- qa_agent.py
- TestBurstinessMetrics
- .client
- seo_toolkit.py
- sanitize_user_prompt
- get_output_serp_audit
- RateLimitingMiddleware
- semrush_backlink_audit_endpoint
- localize_content
- test_ai_seo_audit_integration.py
- test_semrush_suite_endpoints.py
- batch_process
- main.py
- enforce_rate_limit
- analyze_keywords_endpoint
- export_csv_endpoint
- get_audit_trail_endpoint
- semrush_top_pages_endpoint
- get_single_output
- semrush_traffic_insights_endpoint
- get_smart_internal_links
- semrush_ai_search_endpoint
- SensitiveDataScrubberFilter
- semrush_site_audit_endpoint
- analyze_serp_endpoint
- inject_google_disclosure_endpoint
- OutputUpdateRequest
- get_providers_status
- get_robots_txt
- semrush_position_tracking_endpoint
- semrush_topic_research_endpoint
- semrush_local_seo_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 50 edges
2. `process_package()` - 28 edges
3. `de_slop_and_humanize()` - 25 edges
4. `run_ai_seo_audit()` - 19 edges
5. `PackageInput` - 19 edges
6. `run_suite()` - 19 edges
7. `detect_55_patterns()` - 18 edges
8. `audit_google_genai_compliance()` - 17 edges
9. `SEOOutput` - 17 edges
10. `clean_domain_name()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_agent.py → llm_client.py
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/meta_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/qa_agent.py → llm_client.py

## Import Cycles
- None detected.

## Communities (65 total, 15 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "security_firewall.py"
Cohesion: 0.16
Nodes (11): decrypt_secret(), _derive_key(), encrypt_secret(), InMemoryRateLimiter, mask_secret(), Enterprise Security Firewall & Hardening Layer for YatraDham SEO Pipeline.…, Token-bucket rate limiter enforcing max requests per window per IP., Return a masked representation of sensitive keys for logs and UI. (+3 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.07
Nodes (58): _parse_markdown_sections(), Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., _sanitize_repetition(), bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections() (+50 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Return live search intent, LSI keyword entities, and competitor heading…, Destination intelligence fusing OSM Nominatim, Wikipedia, Open-Meteo, Sunrise-…, Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,… (+20 more)

### Community 4 - "de_slop_and_humanize"
Cohesion: 0.07
Nodes (24): apply_voice_transformations(), de_slop_and_humanize(), mask_protected_structures(), Masks markdown code blocks, tables, URLs, HTML tags, and template variables so…, Restores all protected structures exactly as they were., blader & Aboudjem Humanizer Rule: Transforms formulaic 'not only X, but also Y'…, Applies style-specific linguistic adjustments for the selected voice profile:…, Deterministic Anti-AI De-Slopper & Humanizer Pipeline: 1. Masks code blocks,… (+16 more)

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.11
Nodes (19): bulk_action(), clear_cache(), crawl_sitemap(), Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities., Semrush SEO Writing Assistant: Readability, SEO score, tone of voice., Bulk approve or reject outputs with admin authorization., Wipe all outputs from the database to start fresh (Protected Admin Action). (+11 more)

### Community 11 - "anti_ai_guardrails.py"
Cohesion: 0.19
Nodes (18): calculate_burstiness_metrics(), calculate_copyleaks_metrics(), check_copyleaks_api(), detect_55_patterns(), detect_ai_isms(), generate_copyleaks_recommendations(), humanize_data(), Any (+10 more)

### Community 12 - "audit_google_genai_compliance"
Cohesion: 0.10
Nodes (31): audit_google_genai_compliance(), check_eeat_firsthand_experience(), check_factual_accuracy_and_hallucinations(), check_humanizer_and_anti_slop(), check_metadata_and_structured_data(), check_scaled_content_abuse(), check_transparency_who_how_why(), extract_plain_text() (+23 more)

### Community 13 - "validation_layer.py"
Cohesion: 0.13
Nodes (21): check_duplicate_content(), compute_objective_qa_score(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Extract the numeric ₹ amount from a string like 'Starting From ₹ 13,125.00 Per… (+13 more)

### Community 14 - "scraper.py"
Cohesion: 0.13
Nodes (17): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+9 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.11
Nodes (20): get_dictionary_endpoint(), link_safety_preview_endpoint(), moderate_text_endpoint(), proofread_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Grammar, spellcheck & stylistic review via LanguageTool API., Evaluate tone sentiment, spiritual reverence, and toxicity., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+12 more)

### Community 16 - "TestHumanizer55Patterns"
Cohesion: 0.12
Nodes (9): Verify that all 55 patterns are defined, detectable, and actionable., Ensure all 55 patterns (P01 through P55) are correctly registered., P01: Detects 'stands as a testament to' and 'pivotal role'., P13: Detects em-dash overuse., P09: Detects 'not only X, but also Y'., P03: Detects trailing -ing phrases., P18: Detects chatbot residue like 'Certainly! Here is a guide'., P20: Detects 'In today's fast-paced world' and 'When it comes to'. (+1 more)

### Community 17 - "run"
Cohesion: 0.11
Nodes (24): _clean_markdown(), _detect_blog_intent(), _generate_long_form_blog(), _get_intent_structure(), Any, Remove LLM chain-of-thought / reasoning blocks that leak into output. Models…, Classify search intent to generate topic-authentic structures rather than…, Return tailored, high-intent outline with calibrated word budgets ensuring 100%… (+16 more)

### Community 18 - "get"
Cohesion: 0.11
Nodes (18): get, favicon(), get_humanizer_patterns(), get_outputs(), Semrush Consolidated Dashboard., Semrush Site Performance & Core Web Vitals., Semrush Keyword Overview: Deep-dive search volume, global breakdown, KD%., Semrush Keyword Strategy Builder: Topic clusters & pillar architecture. (+10 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.05
Nodes (74): fetch_url_html(), Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO…, Fetch URL with SSRF protection, browser TLS fingerprint spoofing (curl_cffi…, clean_domain_name(), detect_domain_category(), extract_brand_tokens(), fetch_live_google_suggest(), get_ai_search_overview() (+66 more)

### Community 20 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 21 - "process_package"
Cohesion: 0.15
Nodes (21): process_batch_background(), process_single(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, Process a single package through all 5 agents (manual JSON input)., scrape_and_process(), PackageInput, parametrize, process_package() (+13 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.09
Nodes (21): detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs. (+13 more)

### Community 23 - "BaseModel"
Cohesion: 0.13
Nodes (15): CheckAIRequest, deepseek_reasoning_endpoint(), DeepSeekReasonRequest, HumanizeRequest, BaseModel, DeepSeek two-stage reasoning protocol with chain-of-thought verification., Semrush Compare Domains (Multi-domain benchmark)., Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations. (+7 more)

### Community 24 - "LLMClient"
Cohesion: 0.13
Nodes (13): Any, run(), clean_price_string(), LLMClient, Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found… (+5 more)

### Community 25 - "api_route"
Cohesion: 0.10
Nodes (21): api_route, AIAuditRequest, AIVisibilityRequest, check_google_genai_endpoint(), get_ai_seo_audit_endpoint(), get_ai_visibility_audit_endpoint(), GoogleGenAIRequest, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,… (+13 more)

### Community 26 - "content_creator_agent.py"
Cohesion: 0.20
Nodes (15): Content Creator Agent: Generates net-new SEO content from scratch., auto_heal_content(), calculate_burstiness_variance(), calculate_readability_metrics(), extract_clean_prose(), Any, AI SEO Audit & Autonomous Quality Gate Engine…, Executes the comprehensive 15-Point AI-SEO-Audit Gate. Returns: - score (0 -… (+7 more)

### Community 27 - "TestArchitecturalDecoupling"
Cohesion: 0.12
Nodes (9): Architectural Decoupling & Zero-Leakage Verification Suite Ensures that all…, Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio… (+1 more)

### Community 28 - "check_serp_rank"
Cohesion: 0.17
Nodes (13): get_seo_audit_score_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., audit_onpage_seo_score(), check_serp_rank() (+5 more)

### Community 29 - "models.py"
Cohesion: 0.31
Nodes (10): BulkActionRequest, FAQItem, ItineraryDay, NearbyLocation, PricingRow, ProgramHighlights, ProgramSession, BaseModel (+2 more)

### Community 30 - "generate_content"
Cohesion: 0.67
Nodes (3): ContentGenerateRequest, generate_content(), Generate net-new SEO content from scratch using AI.

### Community 31 - "pipeline.py"
Cohesion: 0.14
Nodes (15): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), Keyword agent: enforces 2-4 word primary keyword. (+7 more)

### Community 32 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 33 - "qa_agent.py"
Cohesion: 0.36
Nodes (9): _check_banned(), _check_sections(), _check_sentences(), _extract_prose_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., Extract natural sentences from sections dictionary, skipping JSON syntax. (+1 more)

### Community 34 - "TestBurstinessMetrics"
Cohesion: 0.33
Nodes (4): Verify statistical burstiness calculation., Human text with short and long sentences should yield high burstiness., Monotonous text with uniform sentence lengths yields lower burstiness., TestBurstinessMetrics

### Community 35 - ".client"
Cohesion: 0.12
Nodes (12): Any, AI Visibility & Generative Engine Optimization (GEO / AEO) Module. Inspired by…, Simulates how an AI search engine (Perplexity / ChatGPT Search / SGE)…, simulate_ai_search_response(), fixture, get_ai_visibility_simulation_endpoint(), Autonomous AI Search Simulation & Citation Checker. Simulates how an AI engine…, Verify the FastAPI HTTP endpoints for check-ai, humanize, and patterns. (+4 more)

### Community 36 - "seo_toolkit.py"
Cohesion: 0.20
Nodes (9): get_screenshot_preview_endpoint(), get_seo_tags_generator_endpoint(), Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), generate_seo_tags(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 37 - "sanitize_user_prompt"
Cohesion: 0.20
Nodes (9): Any, field_validator, check_disallowed_xss_patterns(), Any, Sanitizes user instructions and checks for active prompt injection attacks., Raises ValueError (resulting in 422 HTTP status) if dangerous XSS payloads are…, Enterprise HTML & Script Sanitizer: Strips all HTML tags, script elements,…, sanitize_user_prompt() (+1 more)

### Community 39 - "RateLimitingMiddleware"
Cohesion: 0.25
Nodes (7): BaseHTTPMiddleware, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, root(), SecurityHeadersMiddleware

### Community 41 - "localize_content"
Cohesion: 0.40
Nodes (4): localize_content(), Any, Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., Translate and culturally localize SEOOutput sections into Hindi or Gujarati.

### Community 42 - "test_ai_seo_audit_integration.py"
Cohesion: 0.11
Nodes (21): calculate_ai_visibility_metrics(), Comprehensive AI Visibility & GEO Audit Engine (topics/ai-visibility).…, humanize_endpoint(), generate_blog_json_ld(), generate_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generates standalone BlogPosting + FAQPage + Organization JSON-LD for AI… (+13 more)

### Community 44 - "batch_process"
Cohesion: 0.33
Nodes (6): Exception, batch_process(), Process multiple packages from JSON (Admin Protected, Max 25 items)., BatchRequest, Sanitizes raw python exception traces for public consumption., sanitize_error_detail()

### Community 45 - "main.py"
Cohesion: 0.13
Nodes (18): FastAPI, lifespan(), localize(), LocalizeRequest, publish_to_wordpress(), quality_audit_endpoint(), QualityAuditRequest, FastAPI server with .env auto-loading, URL auto-scraping, batch processing,… (+10 more)

### Community 46 - "enforce_rate_limit"
Cohesion: 0.33
Nodes (6): HTTPAuthorizationCredentials, enforce_rate_limit(), Request, FastAPI dependency to rate-limit requests by client IP., Verifies that the caller has valid administrative access. Allows request if: -…, verify_admin_access()

### Community 47 - "analyze_keywords_endpoint"
Cohesion: 0.33
Nodes (5): analyze_keywords_endpoint(), Any, field_validator, Extract top unigrams, bigrams, trigrams & Flesch reading score., URLRequest

### Community 53 - "get_smart_internal_links"
Cohesion: 0.50
Nodes (3): get_smart_internal_links(), Intelligent Cross-Domain Internal Linking Engine for YatraDham Ecosystem., Return contextual internal links filtered to avoid linking to the current page…

### Community 55 - "SensitiveDataScrubberFilter"
Cohesion: 0.50
Nodes (3): LogRecord, Logging filter that redacts API keys, passwords, and tokens before writing to…, SensitiveDataScrubberFilter

### Community 56 - "semrush_site_audit_endpoint"
Cohesion: 0.50
Nodes (4): Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Site Audit: 30-point technical SEO diagnostic with DNS ground truth., semrush_site_audit_endpoint(), SemrushSiteAuditRequest

### Community 57 - "analyze_serp_endpoint"
Cohesion: 0.67
Nodes (3): analyze_serp_endpoint(), Native SERP Competitor & Information Gain Analyzer endpoint. Scrapes live SERP…, SERPAnalyzeRequest

### Community 58 - "inject_google_disclosure_endpoint"
Cohesion: 0.67
Nodes (3): inject_google_disclosure_endpoint(), InjectDisclosureRequest, Inject official Google 'Give users context' transparency disclosure into…

### Community 59 - "OutputUpdateRequest"
Cohesion: 0.67
Nodes (3): Config, OutputUpdateRequest, BaseModel

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `qa_agent.py`, `test_e2e_suite.py`, `.client`, `localize_content`, `main.py`, `run`, `process_package`, `BaseModel`, `content_creator_agent.py`, `TestArchitecturalDecoupling`, `pipeline.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `de_slop_and_humanize()` connect `de_slop_and_humanize` to `test_e2e_suite.py`, `anti_ai_guardrails.py`, `main.py`, `content_creator_agent.py`, `pipeline.py`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `detect_55_patterns()` connect `anti_ai_guardrails.py` to `TestHumanizer55Patterns`, `content_creator_agent.py`, `test_ai_seo_audit_integration.py`, `main.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._