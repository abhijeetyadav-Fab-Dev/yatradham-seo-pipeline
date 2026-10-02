# Graph Report - yatradham-seo-pipeline  (2026-10-01)

## Corpus Check
- 48 files · ~111,221 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 806 nodes · 1639 edges · 52 communities (38 shown, 14 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2076a892`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- security_firewall.py
- test_e2e_suite.py
- enrich_destination_data
- TestVoiceProfiles
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- anti_ai_guardrails.py
- simulate_ai_search_response
- validation_layer.py
- extract_package_data
- nlp_and_safety_toolkit.py
- content_agent.py
- content_creator_agent.py
- get
- semrush_suite.py
- ProviderSettingsRequest
- pipeline.py
- SitemapCrawler
- BaseModel
- LLMClient
- api_route
- de_slop_and_humanize
- TestArchitecturalDecoupling
- check_serp_rank
- TestDeSlopAndHumanize
- generate_content
- run_seo_linter
- batch_urls
- batch_process
- seo_toolkit.py
- get_output_serp_audit
- check_disallowed_xss_patterns
- semrush_backlink_audit_endpoint
- localize
- generate_json_ld
- main.py
- semrush_top_pages_endpoint
- semrush_ai_search_endpoint
- favicon
- get_humanizer_patterns
- get_providers_status
- get_robots_txt
- semrush_dashboard_endpoint
- semrush_position_tracking_endpoint
- semrush_topic_research_endpoint
- semrush_sensor_endpoint
- semrush_local_seo_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 50 edges
2. `process_package()` - 28 edges
3. `de_slop_and_humanize()` - 25 edges
4. `PackageInput` - 19 edges
5. `run_suite()` - 19 edges
6. `run_ai_seo_audit()` - 18 edges
7. `detect_55_patterns()` - 18 edges
8. `SEOOutput` - 17 edges
9. `clean_domain_name()` - 16 edges
10. `run()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_agent.py → llm_client.py
- `_generate_long_form_blog()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/content_creator_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/keyword_agent.py → llm_client.py
- `run()` --uses--> `LLMClient`  [INFERRED]
  agents/meta_agent.py → llm_client.py

## Import Cycles
- None detected.

## Communities (52 total, 14 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "security_firewall.py"
Cohesion: 0.06
Nodes (30): BaseHTTPMiddleware, HTTPAuthorizationCredentials, LogRecord, Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses., Enforces token-bucket rate limiting per IP across all endpoints (returns HTTP…, root() (+22 more)

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.06
Nodes (70): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+62 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Destination intelligence fusing OSM Nominatim, Wikipedia, Open-Meteo, Sunrise-…, Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, Calculate driving distance and duration via Open Source Routing Machine (OSRM). (+20 more)

### Community 4 - "TestVoiceProfiles"
Cohesion: 0.17
Nodes (7): Verify that the 5 distinct voice profiles apply their characteristics., Casual voice introduces natural contractions and conversational tone., Blunt voice strips hedging and fluff., Technical voice preserves facts and strips flowery praise., Warm voice maintains compassionate, pilgrim-friendly atmosphere., Professional voice ensures clear, authoritative prose without corporate jargon., TestVoiceProfiles

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.11
Nodes (20): clear_cache(), crawl_sitemap(), Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities., Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., Wipe all outputs from the database to start fresh (Protected Admin Action)., Crawl an XML Sitemap or Category Landing Page to extract package links with… (+12 more)

### Community 11 - "anti_ai_guardrails.py"
Cohesion: 0.05
Nodes (48): _check_banned(), _check_sections(), _check_sentences(), _extract_prose_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., Extract natural sentences from sections dictionary, skipping JSON syntax. (+40 more)

### Community 12 - "simulate_ai_search_response"
Cohesion: 0.40
Nodes (4): Any, AI Visibility & Generative Engine Optimization (GEO / AEO) Module. Inspired by…, Simulates how an AI search engine (Perplexity / ChatGPT Search / SGE)…, simulate_ai_search_response()

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (19): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Extract the numeric ₹ amount from a string like 'Starting From ₹ 13,125.00 Per…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'. (+11 more)

### Community 14 - "extract_package_data"
Cohesion: 0.11
Nodes (22): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+14 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.11
Nodes (20): get_dictionary_endpoint(), link_safety_preview_endpoint(), moderate_text_endpoint(), proofread_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Grammar, spellcheck & stylistic review via LanguageTool API., Evaluate tone sentiment, spiritual reverence, and toxicity., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+12 more)

### Community 16 - "content_agent.py"
Cohesion: 0.29
Nodes (9): _extract_json_from_response(), get_category_aware_fallback(), Any, Content agent: generates all 19 structured sections from scraped page data., Generates complete, enterprise-grade 19 sections strictly adhering to category…, Robustly extract JSON from LLM response, handling markdown blocks and…, run(), humanize_data() (+1 more)

### Community 17 - "content_creator_agent.py"
Cohesion: 0.10
Nodes (31): _clean_markdown(), _detect_blog_intent(), _generate_long_form_blog(), _get_intent_structure(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2… (+23 more)

### Community 18 - "get"
Cohesion: 0.11
Nodes (18): get, export_csv_endpoint(), get_audit_trail_endpoint(), get_outputs(), get_single_output(), Semrush Site Performance & Core Web Vitals., Semrush Keyword Overview: Deep-dive search volume, global breakdown, KD%., Semrush Keyword Strategy Builder: Topic clusters & pillar architecture. (+10 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.05
Nodes (75): process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, scrape_and_process(), fetch_url_html(), Scrapling-Powered Modern Scraping & DOM Parsing Engine for YatraDham SEO…, Fetch URL with SSRF protection, browser TLS fingerprint spoofing (curl_cffi…, clean_domain_name(), detect_domain_category() (+67 more)

### Community 20 - "ProviderSettingsRequest"
Cohesion: 0.40
Nodes (5): ProviderSettingsRequest, Dynamically configure LLM providers (Groq, Gemini, OpenRouter) at runtime…, Test a provider API key live and return latency & status (Admin Protected)., test_provider_endpoint(), update_provider_settings()

### Community 21 - "pipeline.py"
Cohesion: 0.09
Nodes (25): Any, Keyword agent: enforces 2-4 word primary keyword., run(), Any, Meta description agent: 145-155 chars, natural language, no repetition., run(), Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate… (+17 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.09
Nodes (21): detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs. (+13 more)

### Community 23 - "BaseModel"
Cohesion: 0.17
Nodes (12): analyze_serp_endpoint(), CheckAIRequest, HumanizeRequest, BaseModel, Semrush Compare Domains (Multi-domain benchmark)., Semrush SEO Writing Assistant: Readability, SEO score, tone of voice., Native SERP Competitor & Information Gain Analyzer endpoint. Scrapes live SERP…, semrush_compare_domains_endpoint() (+4 more)

### Community 24 - "LLMClient"
Cohesion: 0.12
Nodes (13): Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., clean_price_string(), LLMClient, Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection. (+5 more)

### Community 25 - "api_route"
Cohesion: 0.14
Nodes (15): api_route, AIAuditRequest, get_ai_seo_audit_endpoint(), Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, 15-Point Automated AI-SEO-Audit Gate (marketplace/actions/ai-seo-audit +… (+7 more)

### Community 26 - "de_slop_and_humanize"
Cohesion: 0.11
Nodes (28): auto_heal_content(), calculate_burstiness_variance(), calculate_readability_metrics(), extract_clean_prose(), Any, AI SEO Audit & Autonomous Quality Gate Engine…, Executes the comprehensive 15-Point AI-SEO-Audit Gate. Returns: - score (0 -…, Extract readable prose from nested dicts, lists, or markdown strings, skipping… (+20 more)

### Community 27 - "TestArchitecturalDecoupling"
Cohesion: 0.14
Nodes (8): Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio…, TestArchitecturalDecoupling

### Community 28 - "check_serp_rank"
Cohesion: 0.17
Nodes (13): get_seo_audit_score_endpoint(), get_serp_rank_endpoint(), get_serp_search_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., audit_onpage_seo_score(), check_serp_rank() (+5 more)

### Community 29 - "TestDeSlopAndHumanize"
Cohesion: 0.17
Nodes (7): Key AI buzzwords must be replaced with clean plain English., Markdown tables, URLs, and code blocks must not be corrupted., Smart curly quotes must be normalized to straight ASCII quotes., Verify deterministic de-slopping, em-dash removal, and replacements., Em dashes must be replaced with commas, colons, or clean punctuation., not only X, but also Y' should be transformed to natural 'X and Y'., TestDeSlopAndHumanize

### Community 30 - "generate_content"
Cohesion: 0.25
Nodes (8): ContentGenerateRequest, deepseek_reasoning_endpoint(), DeepSeekReasonRequest, generate_content(), DeepSeek two-stage reasoning protocol with chain-of-thought verification., Generate net-new SEO content from scratch using AI., Sanitizes user instructions and checks for active prompt injection attacks., sanitize_user_prompt()

### Community 31 - "run_seo_linter"
Cohesion: 0.50
Nodes (4): calculate_flesch_reading_ease(), Any, Real-Time Dynamic SEO & GEO Linter for YatraDham. Performs rigorous, non-…, run_seo_linter()

### Community 32 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 35 - "batch_process"
Cohesion: 0.12
Nodes (13): Exception, fixture, batch_process(), get_ai_visibility_simulation_endpoint(), Process multiple packages from JSON (Admin Protected, Max 25 items)., Autonomous AI Search Simulation & Citation Checker. Simulates how an AI engine…, Sanitizes raw python exception traces for public consumption., sanitize_error_detail() (+5 more)

### Community 36 - "seo_toolkit.py"
Cohesion: 0.20
Nodes (9): get_screenshot_preview_endpoint(), get_seo_tags_generator_endpoint(), Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), generate_seo_tags(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 39 - "check_disallowed_xss_patterns"
Cohesion: 0.25
Nodes (7): analyze_keywords_endpoint(), Any, field_validator, Extract top unigrams, bigrams, trigrams & Flesch reading score., URLRequest, check_disallowed_xss_patterns(), Raises ValueError (resulting in 422 HTTP status) if dangerous XSS payloads are…

### Community 41 - "localize"
Cohesion: 0.33
Nodes (6): localize_content(), Any, Translate and culturally localize SEOOutput sections into Hindi or Gujarati., localize(), LocalizeRequest, Translate and localize generated SEO content into Hindi or Gujarati.

### Community 42 - "generate_json_ld"
Cohesion: 0.28
Nodes (8): generate_blog_json_ld(), generate_json_ld(), Any, Schema.org JSON-LD Structured Data Generator for YatraDham Packages., Generates standalone BlogPosting + FAQPage + Organization JSON-LD for AI…, Generate comprehensive stacked Schema.org JSON-LD for Google Rich Results, SGE…, Verify JSON-LD schema generation for both packages and blog articles., test_blog_and_package_schema_validity()

### Community 45 - "main.py"
Cohesion: 0.13
Nodes (18): FastAPI, AIVisibilityRequest, get_ai_visibility_audit_endpoint(), lifespan(), publish_to_wordpress(), quality_audit_endpoint(), QualityAuditRequest, FastAPI server with .env auto-loading, URL auto-scraping, batch processing,… (+10 more)

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `test_e2e_suite.py`, `localize`, `anti_ai_guardrails.py`, `simulate_ai_search_response`, `main.py`, `content_agent.py`, `content_creator_agent.py`, `semrush_suite.py`, `pipeline.py`, `TestArchitecturalDecoupling`, `generate_content`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `de_slop_and_humanize()` connect `de_slop_and_humanize` to `test_e2e_suite.py`, `TestVoiceProfiles`, `anti_ai_guardrails.py`, `main.py`, `content_agent.py`, `content_creator_agent.py`, `TestDeSlopAndHumanize`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `detect_55_patterns()` connect `anti_ai_guardrails.py` to `de_slop_and_humanize`, `main.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._