# Graph Report - yatradham-seo-pipeline  (2026-09-14)

## Corpus Check
- 40 files · ~85,730 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 633 nodes · 1277 edges · 50 communities (37 shown, 13 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 49 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c05210f5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 📅 Day-by-Day Comprehensive Itinerary
- check_serp_rank
- test_e2e_suite.py
- enrich_destination_data
- seo_toolkit.py
- WordPressPublisher
- 1. Security & OWASP Hardening Layer
- post
- qa_agent.py
- batch_process
- validation_layer.py
- extract_package_data
- nlp_and_safety_toolkit.py
- audit_onpage_seo_score
- TestArchitecturalDecoupling
- get
- semrush_suite.py
- security_firewall.py
- content_creator_agent.py
- SitemapCrawler
- main.py
- LLMClient
- semrush_backlinks_endpoint
- .sanitize_xss_and_prompt_injection
- sanitize_user_prompt
- batch_urls
- llm_client.py
- .test_provider
- content_agent.py
- is_safe_url
- get_on_page_seo_checker
- localize_content
- meta_agent.py
- title_agent.py
- favicon
- get_providers_status
- delete_single_output
- get_single_output
- semrush_site_performance_endpoint
- semrush_position_tracking_endpoint
- semrush_top_pages_endpoint
- semrush_sensor_endpoint
- get_audit_trail_endpoint
- get_outputs
- semrush_dashboard_endpoint
- semrush_keyword_strategy_endpoint
- semrush_ai_search_endpoint

## God Nodes (most connected - your core abstractions)
1. `LLMClient` - 39 edges
2. `process_package()` - 21 edges
3. `run_suite()` - 19 edges
4. `SEOOutput` - 17 edges
5. `clean_domain_name()` - 16 edges
6. `PackageInput` - 15 edges
7. `is_safe_url()` - 15 edges
8. `get_domain_overview()` - 14 edges
9. `SectionedContent` - 13 edges
10. `run_validation()` - 13 edges

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

## Communities (50 total, 13 thin omitted)

### Community 0 - "📅 Day-by-Day Comprehensive Itinerary"
Cohesion: 0.10
Nodes (20): 7-Day Haridwar Spiritual & Wellness Retreat | YatraDham, Day 1, Day 2, Day 3, Day 4, Day 5, Day 6, Day 7 (+12 more)

### Community 1 - "check_serp_rank"
Cohesion: 0.25
Nodes (8): get_serp_rank_endpoint(), get_serp_search_endpoint(), Live SERP search results, competitor rankings, and People Also Ask questions., Check SERP ranking position of target domain for a specific keyword., check_serp_rank(), fetch_serp_results(), Fetch live Google SERP organic rankings and People Also Ask questions.…, Check the current Google SERP ranking position of target_domain for a given…

### Community 2 - "test_e2e_suite.py"
Cohesion: 0.06
Nodes (74): bulk_update_status(), clear_all_outputs(), delete_output(), _dict_to_sections(), _execute_with_retry(), get_audit_trail(), get_conn(), get_output() (+66 more)

### Community 3 - "enrich_destination_data"
Cohesion: 0.09
Nodes (28): enrich_destination_endpoint(), get_forex_rates_endpoint(), get_serp_intelligence_endpoint(), get_transit_distance_endpoint(), Enrich destination using 4 free public APIs (OSM Geocoding, Wikipedia, Open-…, Convert INR price to USD, EUR, GBP, AUD, CAD, SGD via Frankfurter API (free,…, Calculate driving distance and duration via Open Source Routing Machine (OSRM)., Return live search intent, LSI keyword entities, and competitor heading… (+20 more)

### Community 4 - "seo_toolkit.py"
Cohesion: 0.33
Nodes (5): get_screenshot_preview_endpoint(), Generate screenshot preview card URL for any landing page or competitor site., generate_screenshot_preview_url(), Advanced SEO & SERP Toolkit for YatraDham SEO Pipeline. Integrates 6…, Generate live website screenshot preview URLs. Uses ScreenshotOne API if key…

### Community 6 - "1. Security & OWASP Hardening Layer"
Cohesion: 0.08
Nodes (23): 1.1 API Authentication & Role-Based Access Control, 1.2 SSRF Defense & URL Sanitization, 1.3 Stored & Reflected XSS Sanitization, 1.4 Mass Assignment Prevention, 1.5 Prompt Injection & Jailbreak Firewall, 1.6 Secret Encryption at Rest & Log Scrubber, 1.7 Enterprise Security Headers & Rate Limiting (DoS Defense), 1. Security & OWASP Hardening Layer (+15 more)

### Community 7 - "post"
Cohesion: 0.11
Nodes (20): bulk_action(), clear_cache(), moderate_text_endpoint(), ProviderSettingsRequest, Semrush Keyword Gap: Identifies shared, missing, and untapped ranking…, Semrush Backlink Gap: Find link opportunities., Bulk approve or reject outputs with admin authorization., Wipe all outputs from the database to start fresh (Protected Admin Action). (+12 more)

### Community 11 - "qa_agent.py"
Cohesion: 0.19
Nodes (17): _check_banned(), _check_sections(), _check_sentences(), _flesch_estimate(), Any, QA agent: validates all 19 sections + readability., run(), calculate_copyleaks_metrics() (+9 more)

### Community 12 - "batch_process"
Cohesion: 0.29
Nodes (7): Exception, batch_process(), process_single(), Process a single package through all 5 agents (manual JSON input)., Process multiple packages from JSON (Admin Protected, Max 25 items)., Sanitizes raw python exception traces for public consumption., sanitize_error_detail()

### Community 13 - "validation_layer.py"
Cohesion: 0.15
Nodes (20): check_duplicate_content(), extract_price_number(), find_duplicated_words(), _is_empty_val(), Any, Yatradham SEO Pipeline — Validation Layer…, Find any immediately-repeated word, e.g. 'Guided Guided', 'the the'., Compare one section (e.g. 'why_choose_bullets') of the new row against the same… (+12 more)

### Community 14 - "extract_package_data"
Cohesion: 0.14
Nodes (17): _extract_numeric_price(), Any, Enterprise Ground-Truth Fact Checker & Anti-Hallucination Verification Gate.…, verify_ground_truth(), generate_archetype_content(), Any, Multi-Archetype Content Generation Engine for YatraDham Wellness. Produces…, clean_price_string() (+9 more)

### Community 15 - "nlp_and_safety_toolkit.py"
Cohesion: 0.11
Nodes (20): analyze_keywords_endpoint(), get_dictionary_endpoint(), link_safety_preview_endpoint(), proofread_endpoint(), Lookup English definitions, phonetics, parts of speech via Free Dictionary API., Grammar, spellcheck & stylistic review via LanguageTool API., Extract top unigrams, bigrams, trigrams & Flesch reading score., Scan URL safety protocol, SSL certificate, and extract OpenGraph preview. (+12 more)

### Community 16 - "audit_onpage_seo_score"
Cohesion: 0.22
Nodes (9): get_seo_audit_score_endpoint(), get_seo_tags_generator_endpoint(), On-page SEO score & recommendations (Title, Meta, Keyword, Depth, Density)., Generate HTML Meta tags, OpenGraph tags, and Twitter Cards., audit_onpage_seo_score(), generate_seo_tags(), Any, Generates standard HTML SEO Meta Tags, OpenGraph Tags, and Twitter Cards. (+1 more)

### Community 17 - "TestArchitecturalDecoupling"
Cohesion: 0.12
Nodes (9): Architectural Decoupling & Zero-Leakage Verification Suite Ensures that all…, Rigorous verification that subsystems maintain clean boundary isolation., Scraper & Scrapling engine must be pure parsers with no LLM or Database imports., Validation layer and fact checker must be pure verification functions., Content Creator Agent (AI Studio) must be decoupled from 19-section pipeline., 19-Section Pipeline must be decoupled from AI Studio., LLMClient instances must be stateless between requests with zero shared lockout…, Public APIs enricher must work autonomously without pipeline or studio… (+1 more)

### Community 18 - "get"
Cohesion: 0.12
Nodes (16): get, export_csv_endpoint(), get_robots_txt(), Semrush Keyword Overview: Deep-dive search volume, global breakdown, KD%., Semrush Topic Research: Mindmap cards, questions, and high-CTR headlines., Semrush Backlink Audit: Toxicity score and disavow candidates., Semrush Organic Traffic Insights: Landing pages & queries., Semrush Local SEO: 3-Pack rank potential & GBP audit. (+8 more)

### Community 19 - "semrush_suite.py"
Cohesion: 0.09
Nodes (50): clean_domain_name(), detect_domain_category(), extract_brand_tokens(), fetch_live_google_suggest(), get_ai_search_overview(), get_backlink_audit(), get_backlink_gap(), get_backlink_overview() (+42 more)

### Community 20 - "security_firewall.py"
Cohesion: 0.06
Nodes (32): BaseHTTPMiddleware, FastAPI, HTTPAuthorizationCredentials, LogRecord, lifespan(), Request, RateLimitingMiddleware, Injects enterprise OWASP security headers on all HTTP responses. (+24 more)

### Community 21 - "content_creator_agent.py"
Cohesion: 0.17
Nodes (18): _clean_markdown(), _generate_long_form_blog(), _parse_markdown_sections(), Any, Content Creator Agent: Generates net-new SEO content from scratch., Parse a markdown string into a dictionary based on H1 headings and H2…, Strip LLM loops AND apply Anti-AI-Detection replacements to bypass Copyleaks., Remove LLM chain-of-thought / reasoning blocks that leak into output. Models… (+10 more)

### Community 22 - "SitemapCrawler"
Cohesion: 0.10
Nodes (20): detect_url_category(), Classify the URL or page text into 'wellness', 'tour', 'stay', or 'puja'., Any, Prioritizes bookable pilgrimage packages, destination stays, pujas, and…, Accurately classifies discovered links into stay, tour, wellness, or puja., Derives a clean human-readable title from URL segments when anchor text is…, Parses XML sitemaps with namespace stripping, index recursing, and regex…, Parses HTML category pages, capturing clean anchor titles and canonical URLs. (+12 more)

### Community 23 - "main.py"
Cohesion: 0.10
Nodes (31): check_ai_endpoint(), CheckAIRequest, crawl_sitemap(), humanize_endpoint(), HumanizeRequest, localize(), LocalizeRequest, publish_to_wordpress() (+23 more)

### Community 24 - "LLMClient"
Cohesion: 0.31
Nodes (4): LLMClient, Any, Execute DeepSeek two-stage reasoning protocol: 1. Stage 1 (<thinking>): Deep…, Strip internal thinking/reasoning tags leaked from thinking models.

### Community 25 - "semrush_backlinks_endpoint"
Cohesion: 0.18
Nodes (12): api_route, Semrush Domain Overview: Authority Score, Organic Traffic, Keywords,…, Semrush Keyword Magic Tool: Real-time search volume, intent classification,…, Semrush Site Audit: 30-point technical crawl for HTTP codes, meta, H1, images,…, Semrush Backlink Analytics: Authority Score, Referring Domains, Dofollow Ratio,…, semrush_backlinks_endpoint(), semrush_domain_overview_endpoint(), semrush_keyword_magic_endpoint() (+4 more)

### Community 26 - ".sanitize_xss_and_prompt_injection"
Cohesion: 0.24
Nodes (6): Any, field_validator, Any, field_validator, check_disallowed_xss_patterns(), Raises ValueError (resulting in 422 HTTP status) if dangerous XSS payloads are…

### Community 27 - "sanitize_user_prompt"
Cohesion: 0.25
Nodes (8): ContentGenerateRequest, deepseek_reasoning_endpoint(), DeepSeekReasonRequest, generate_content(), Generate net-new SEO content from scratch using AI., DeepSeek two-stage reasoning protocol with chain-of-thought verification., Sanitizes user instructions and checks for active prompt injection attacks., sanitize_user_prompt()

### Community 28 - "batch_urls"
Cohesion: 0.50
Nodes (4): BackgroundTasks, batch_urls(), BatchURLRequest, Scrape and process multiple URLs automatically in the background (Admin…

### Community 29 - "llm_client.py"
Cohesion: 0.22
Nodes (6): Any, Keyword agent: enforces 2-4 word primary keyword., run(), clean_price_string(), Return a rich, dynamic response when no LLM provider key is available.…, Sanitize and format price strings cleanly. Never return hardcoded mock numbers…

### Community 30 - ".test_provider"
Cohesion: 0.33
Nodes (4): Allow setting runtime keys dynamically for a request without server restart., Dynamically query the provider's live models list to avoid model_not_found…, Test a provider API key with a fast 1-word prompt to verify connection., OpenAI

### Community 31 - "content_agent.py"
Cohesion: 0.40
Nodes (5): _extract_json_from_response(), Any, Content agent: generates all 19 structured sections from scraped page data., Robustly extract JSON from LLM response, handling markdown blocks and…, run()

### Community 32 - "is_safe_url"
Cohesion: 0.13
Nodes (18): process_batch_background(), Scrape a Yatradham URL and auto-process through all 5 agents with custom…, Scrapling + curl_cffi Chrome 124 stealth scrape with deep JSON-LD extraction., scrape_and_process(), scrape_stealth_endpoint(), StealthScrapeRequest, URLRequest, extract_with_scrapling() (+10 more)

### Community 33 - "get_on_page_seo_checker"
Cohesion: 0.40
Nodes (5): Semrush On-Page SEO Checker: Actionable strategy, backlink, UX recommendations., semrush_on_page_checker_endpoint(), SemrushOnPageRequest, get_on_page_seo_checker(), Semrush On-Page SEO Checker. Provides targeted recommendations across Strategy,…

### Community 34 - "localize_content"
Cohesion: 0.40
Nodes (4): localize_content(), Any, Indic Multi-Language Localization Engine for YatraDham (Hindi & Gujarati)., Translate and culturally localize SEOOutput sections into Hindi or Gujarati.

### Community 35 - "meta_agent.py"
Cohesion: 0.50
Nodes (3): Any, Meta description agent: 145-155 chars, natural language, no repetition., run()

### Community 36 - "title_agent.py"
Cohesion: 0.50
Nodes (3): Any, Title tag agent: 50-60 chars, optimized for click-through rate with accurate…, run()

### Community 39 - "delete_single_output"
Cohesion: 0.67
Nodes (3): delete, delete_single_output(), Delete a single output with admin authorization.

## Knowledge Gaps
- **37 isolated node(s):** `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control`, `1.2 SSRF Defense & URL Sanitization`, `1.3 Stored & Reflected XSS Sanitization` (+32 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LLMClient` connect `LLMClient` to `is_safe_url`, `localize_content`, `meta_agent.py`, `title_agent.py`, `test_e2e_suite.py`, `qa_agent.py`, `TestArchitecturalDecoupling`, `content_creator_agent.py`, `main.py`, `sanitize_user_prompt`, `llm_client.py`, `.test_provider`, `content_agent.py`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `run_validation()` connect `validation_layer.py` to `test_e2e_suite.py`, `main.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `SitemapCrawler` connect `SitemapCrawler` to `main.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `LLMClient` (e.g. with `run()` and `_generate_long_form_blog()`) actually correct?**
  _`LLMClient` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `process_package()` (e.g. with `LLMClient` and `PackageInput`) actually correct?**
  _`process_package()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Config`, `Executive Summary`, `1.1 API Authentication & Role-Based Access Control` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `📅 Day-by-Day Comprehensive Itinerary` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._